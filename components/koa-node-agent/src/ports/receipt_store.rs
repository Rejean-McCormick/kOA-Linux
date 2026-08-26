//! Immutable receipt persistence port.

use core::fmt;

pub const MAX_RECEIPT_BYTES: usize = 1024 * 1024;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ReceiptRecord {
    pub receipt_id: String,
    pub request_id: String,
    pub body: Vec<u8>,
}

impl ReceiptRecord {
    pub fn new(
        receipt_id: impl Into<String>,
        request_id: impl Into<String>,
        body: Vec<u8>,
    ) -> Result<Self, ReceiptStoreError> {
        let record = Self {
            receipt_id: receipt_id.into(),
            request_id: request_id.into(),
            body,
        };
        record.validate()?;
        Ok(record)
    }

    pub fn validate(&self) -> Result<(), ReceiptStoreError> {
        validate_identifier("receipt_id", &self.receipt_id)?;
        validate_identifier("request_id", &self.request_id)?;
        if self.body.is_empty() {
            return Err(ReceiptStoreError::invalid("receipt body must not be empty"));
        }
        if self.body.len() > MAX_RECEIPT_BYTES {
            return Err(ReceiptStoreError::invalid(
                "receipt body exceeds the bounded storage limit",
            ));
        }
        if std::str::from_utf8(&self.body).is_err() {
            return Err(ReceiptStoreError::invalid(
                "receipt body must have a deterministic UTF-8 representation",
            ));
        }
        Ok(())
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ReceiptWriteDisposition {
    Created,
    EquivalentReplay,
}

pub trait ReceiptStore: Send + Sync {
    fn append(&self, record: &ReceiptRecord) -> Result<ReceiptWriteDisposition, ReceiptStoreError>;

    fn read(&self, receipt_id: &str) -> Result<Option<ReceiptRecord>, ReceiptStoreError>;
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ReceiptStoreErrorCode {
    InvalidRecord,
    Unavailable,
    Conflict,
    CorruptRecord,
    UnsafePath,
}

impl ReceiptStoreErrorCode {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::InvalidRecord => "invalid_record",
            Self::Unavailable => "unavailable",
            Self::Conflict => "conflict",
            Self::CorruptRecord => "corrupt_record",
            Self::UnsafePath => "unsafe_path",
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ReceiptStoreError {
    code: ReceiptStoreErrorCode,
    detail: String,
}

impl ReceiptStoreError {
    pub fn new(code: ReceiptStoreErrorCode, detail: impl Into<String>) -> Self {
        Self {
            code,
            detail: detail.into(),
        }
    }

    fn invalid(detail: impl Into<String>) -> Self {
        Self::new(ReceiptStoreErrorCode::InvalidRecord, detail)
    }

    pub const fn code(&self) -> ReceiptStoreErrorCode {
        self.code
    }

    pub fn detail(&self) -> &str {
        &self.detail
    }
}

impl fmt::Display for ReceiptStoreError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}: {}", self.code.as_str(), self.detail)
    }
}

impl std::error::Error for ReceiptStoreError {}

pub(crate) fn validate_identifier(name: &str, value: &str) -> Result<(), ReceiptStoreError> {
    if value.is_empty() || value.len() > 256 {
        return Err(ReceiptStoreError::invalid(format!(
            "{name} must be a non-empty identifier no longer than 256 bytes"
        )));
    }
    if !value
        .bytes()
        .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_' | b'.' | b':'))
    {
        return Err(ReceiptStoreError::invalid(format!(
            "{name} contains a character outside the closed identifier alphabet"
        )));
    }
    Ok(())
}
