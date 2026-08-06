//! System clock adapter.

use std::time::{SystemTime, UNIX_EPOCH};

use crate::ports::{Clock, ClockError};

#[derive(Clone, Copy, Debug, Default)]
pub struct SystemClock;

impl Clock for SystemClock {
    fn now_unix_seconds(&self) -> Result<u64, ClockError> {
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|duration| duration.as_secs())
            .map_err(|error| {
                ClockError::new(
                    "system_clock_before_unix_epoch",
                    format!("system clock cannot be represented as Unix time: {error}"),
                )
            })
    }
}
