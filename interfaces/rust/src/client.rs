use crate::{ClientError, EventEnvelope, error::ErrorEnvelope};
use serde::{Deserialize, Serialize, de::DeserializeOwned};

/// Delivery mechanism only. Implementations must not infer authorization or
/// business acceptance from successful byte delivery.
pub trait Transport {
    fn exchange(&self, request: &[u8]) -> Result<Vec<u8>, crate::TransportError>;
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ResponseDisposition {
    Completed,
    AcceptedForDeferredWork,
    Rejected,
    Blocked,
    Expired,
    Cancelled,
    Failed,
    Indeterminate,
}

/// Wire-neutral response wrapper used by the minimal client.
#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ResponseEnvelope<T> {
    pub request_id: String,
    pub correlation_id: String,
    pub disposition: ResponseDisposition,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub payload: Option<T>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<ErrorEnvelope>,
}

impl<T> ResponseEnvelope<T> {
    fn validate_shape(&self) -> Result<(), ClientError> {
        match self.disposition {
            ResponseDisposition::Completed | ResponseDisposition::AcceptedForDeferredWork => {
                if self.payload.is_some() && self.error.is_none() {
                    Ok(())
                } else {
                    Err(ClientError::InvalidResponse(
                        "successful or deferred response must contain payload and no error"
                            .to_owned(),
                    ))
                }
            },
            ResponseDisposition::Rejected
            | ResponseDisposition::Blocked
            | ResponseDisposition::Expired
            | ResponseDisposition::Cancelled
            | ResponseDisposition::Failed
            | ResponseDisposition::Indeterminate => {
                if self.payload.is_none() && self.error.is_some() {
                    Ok(())
                } else {
                    Err(ClientError::InvalidResponse(
                        "non-completed response must contain one error and no payload".to_owned(),
                    ))
                }
            },
        }
    }
}

/// Minimal synchronous client over a caller-supplied transport.
pub struct InterfaceClient<T> {
    transport: T,
}

impl<T> InterfaceClient<T>
where
    T: Transport,
{
    #[must_use]
    pub fn new(transport: T) -> Self {
        Self { transport }
    }

    #[must_use]
    pub fn transport(&self) -> &T {
        &self.transport
    }

    pub fn send<P, R>(&self, request: &EventEnvelope<P>) -> Result<ResponseEnvelope<R>, ClientError>
    where
        P: Serialize,
        R: DeserializeOwned,
    {
        request.validate_metadata()?;
        let request_bytes = serde_json::to_vec(request)?;
        let response_bytes = self.transport.exchange(&request_bytes)?;
        let response: ResponseEnvelope<R> = serde_json::from_slice(&response_bytes)?;

        if response.request_id != request.correlation.request_id {
            return Err(ClientError::InvalidResponse(
                "response request_id does not match request".to_owned(),
            ));
        }
        if response.correlation_id != request.correlation.correlation_id {
            return Err(ClientError::InvalidResponse(
                "response correlation_id does not match request".to_owned(),
            ));
        }
        response.validate_shape()?;
        if let Some(error) = &response.error {
            error.validate()?;
            if error.correlation.correlation_id != request.correlation.correlation_id
                || error
                    .correlation
                    .request_id
                    .as_deref()
                    .is_some_and(|request_id| request_id != request.correlation.request_id.as_str())
            {
                return Err(ClientError::InvalidResponse(
                    "remote error correlation does not match request".to_owned(),
                ));
            }
        }
        Ok(response)
    }

    pub fn execute<P, R>(&self, request: &EventEnvelope<P>) -> Result<R, ClientError>
    where
        P: Serialize,
        R: DeserializeOwned,
    {
        let response = self.send(request)?;
        match response.disposition {
            ResponseDisposition::Completed => response.payload.ok_or_else(|| {
                ClientError::InvalidResponse(
                    "completed response is missing its validated payload".to_owned(),
                )
            }),
            ResponseDisposition::AcceptedForDeferredWork => Err(ClientError::InvalidResponse(
                "deferred response must be resolved through the job status interface".to_owned(),
            )),
            ResponseDisposition::Rejected
            | ResponseDisposition::Blocked
            | ResponseDisposition::Expired
            | ResponseDisposition::Cancelled
            | ResponseDisposition::Failed
            | ResponseDisposition::Indeterminate => {
                let error = response.error.ok_or_else(|| {
                    ClientError::InvalidResponse(
                        "non-completed response is missing its validated error".to_owned(),
                    )
                })?;
                Err(ClientError::Remote(error))
            },
        }
    }
}
