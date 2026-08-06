//! Time source used by node-local validation and receipt persistence.

use core::fmt;

/// A monotonic-enough wall-clock reading expressed as Unix seconds.
///
/// Callers remain responsible for comparing the reading with a contract-bound
/// deadline.  The port does not manufacture authorization validity.
pub trait Clock: Send + Sync {
    fn now_unix_seconds(&self) -> Result<u64, ClockError>;
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ClockError {
    code: &'static str,
    detail: String,
}

impl ClockError {
    pub fn new(code: &'static str, detail: impl Into<String>) -> Self {
        Self {
            code,
            detail: detail.into(),
        }
    }

    pub const fn code(&self) -> &'static str {
        self.code
    }

    pub fn detail(&self) -> &str {
        &self.detail
    }
}

impl fmt::Display for ClockError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}: {}", self.code, self.detail)
    }
}

impl std::error::Error for ClockError {}
