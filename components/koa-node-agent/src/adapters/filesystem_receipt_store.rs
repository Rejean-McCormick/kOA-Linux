//! Immutable filesystem receipt store confined to one declared root.

use std::fs::{self, File, OpenOptions};
use std::io::{Read, Write};
use std::path::{Path, PathBuf};

use crate::ports::receipt_store::validate_identifier;
use crate::ports::{
    ReceiptRecord, ReceiptStore, ReceiptStoreError, ReceiptStoreErrorCode,
    ReceiptWriteDisposition, MAX_RECEIPT_BYTES,
};

#[derive(Clone, Debug)]
pub struct FilesystemReceiptStore {
    root: PathBuf,
}

impl FilesystemReceiptStore {
    pub fn open(root: impl Into<PathBuf>) -> Result<Self, ReceiptStoreError> {
        let root = root.into();
        validate_root(&root)?;
        Ok(Self { root })
    }

    pub fn root(&self) -> &Path {
        &self.root
    }

    fn final_path(&self, receipt_id: &str) -> Result<PathBuf, ReceiptStoreError> {
        validate_identifier("receipt_id", receipt_id)?;
        Ok(self.root.join(format!("{receipt_id}.json")))
    }

    fn pending_path(&self, receipt_id: &str) -> Result<PathBuf, ReceiptStoreError> {
        validate_identifier("receipt_id", receipt_id)?;
        Ok(self.root.join(format!(".{receipt_id}.pending")))
    }
}

impl ReceiptStore for FilesystemReceiptStore {
    fn append(
        &self,
        record: &ReceiptRecord,
    ) -> Result<ReceiptWriteDisposition, ReceiptStoreError> {
        record.validate()?;
        validate_root(&self.root)?;
        let final_path = self.final_path(&record.receipt_id)?;
        if final_path.exists() {
            return compare_existing(&final_path, record);
        }

        let pending_path = self.pending_path(&record.receipt_id)?;
        let mut pending = OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&pending_path)
            .map_err(|error| {
                ReceiptStoreError::new(
                    ReceiptStoreErrorCode::Unavailable,
                    format!("cannot create pending receipt: {error}"),
                )
            })?;

        let write_result = (|| {
            pending.write_all(record.request_id.as_bytes())?;
            pending.write_all(b"\n")?;
            pending.write_all(&record.body)?;
            pending.sync_all()?;
            fs::hard_link(&pending_path, &final_path)?;
            sync_directory(&self.root)?;
            fs::remove_file(&pending_path)?;
            Ok::<(), std::io::Error>(())
        })();

        if let Err(error) = write_result {
            let _ = fs::remove_file(&pending_path);
            if final_path.exists() {
                return compare_existing(&final_path, record);
            }
            return Err(ReceiptStoreError::new(
                ReceiptStoreErrorCode::Unavailable,
                format!("cannot commit immutable receipt: {error}"),
            ));
        }
        Ok(ReceiptWriteDisposition::Created)
    }

    fn read(&self, receipt_id: &str) -> Result<Option<ReceiptRecord>, ReceiptStoreError> {
        validate_root(&self.root)?;
        let path = self.final_path(receipt_id)?;
        if !path.exists() {
            return Ok(None);
        }
        let metadata = fs::symlink_metadata(&path).map_err(unavailable)?;
        if metadata.file_type().is_symlink() || !metadata.is_file() {
            return Err(ReceiptStoreError::new(
                ReceiptStoreErrorCode::UnsafePath,
                "receipt path is not a regular non-symlink file",
            ));
        }
        let (request_id, body) = read_record_bytes(&path)?;
        ReceiptRecord::new(receipt_id.to_owned(), request_id, body).map(Some)
    }
}

fn validate_root(root: &Path) -> Result<(), ReceiptStoreError> {
    if !root.is_absolute() || root == Path::new("/") {
        return Err(ReceiptStoreError::new(
            ReceiptStoreErrorCode::UnsafePath,
            "receipt root must be an absolute bounded directory",
        ));
    }
    let metadata = fs::symlink_metadata(root).map_err(unavailable)?;
    if metadata.file_type().is_symlink() || !metadata.is_dir() {
        return Err(ReceiptStoreError::new(
            ReceiptStoreErrorCode::UnsafePath,
            "receipt root must be an existing non-symlink directory",
        ));
    }
    Ok(())
}

fn compare_existing(
    path: &Path,
    record: &ReceiptRecord,
) -> Result<ReceiptWriteDisposition, ReceiptStoreError> {
    let metadata = fs::symlink_metadata(path).map_err(unavailable)?;
    if metadata.file_type().is_symlink() || !metadata.is_file() {
        return Err(ReceiptStoreError::new(
            ReceiptStoreErrorCode::UnsafePath,
            "existing receipt is not a regular non-symlink file",
        ));
    }
    let (request_id, body) = read_record_bytes(path)?;
    if request_id == record.request_id && body == record.body {
        Ok(ReceiptWriteDisposition::EquivalentReplay)
    } else {
        Err(ReceiptStoreError::new(
            ReceiptStoreErrorCode::Conflict,
            "receipt identity is already bound to different content",
        ))
    }
}

fn read_record_bytes(path: &Path) -> Result<(String, Vec<u8>), ReceiptStoreError> {
    let mut file = File::open(path).map_err(unavailable)?;
    let maximum = MAX_RECEIPT_BYTES + 257;
    let mut bytes = Vec::new();
    file.by_ref()
        .take(maximum as u64 + 1)
        .read_to_end(&mut bytes)
        .map_err(unavailable)?;
    if bytes.len() > maximum {
        return Err(ReceiptStoreError::new(
            ReceiptStoreErrorCode::CorruptRecord,
            "stored receipt exceeds the bounded record size",
        ));
    }
    let separator = bytes.iter().position(|byte| *byte == b'\n').ok_or_else(|| {
        ReceiptStoreError::new(
            ReceiptStoreErrorCode::CorruptRecord,
            "stored receipt is missing its request identity header",
        )
    })?;
    let request_id = std::str::from_utf8(&bytes[..separator])
        .map_err(|_| {
            ReceiptStoreError::new(
                ReceiptStoreErrorCode::CorruptRecord,
                "stored request identity is not UTF-8",
            )
        })?
        .to_owned();
    validate_identifier("request_id", &request_id)?;
    Ok((request_id, bytes[separator + 1..].to_vec()))
}

fn sync_directory(path: &Path) -> std::io::Result<()> {
    File::open(path)?.sync_all()
}

fn unavailable(error: std::io::Error) -> ReceiptStoreError {
    ReceiptStoreError::new(ReceiptStoreErrorCode::Unavailable, error.to_string())
}
