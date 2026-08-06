"""Public API boundary for the Identity and Trust component."""

from .models import (
    API_VERSION,
    COMPONENT_ID,
    CONTRACT_VERSION,
    EXPECTED_FAILURE_CODES,
    OPERATIONS,
    OPERATIONS_BY_PATH,
    ApiBoundaryError,
    ApiResponse,
    IdentityResult,
    OperationKind,
    OperationSpec,
    RequestContext,
    TrustResult,
)
from .routes import (
    ROUTES,
    ComponentFailure,
    HttpResult,
    IdentityAndTrustRouter,
    IdentityAndTrustService,
    RouteDefinition,
    build_router,
)

__all__ = [
    "API_VERSION",
    "COMPONENT_ID",
    "CONTRACT_VERSION",
    "EXPECTED_FAILURE_CODES",
    "OPERATIONS",
    "OPERATIONS_BY_PATH",
    "ROUTES",
    "ApiBoundaryError",
    "ApiResponse",
    "ComponentFailure",
    "HttpResult",
    "IdentityAndTrustRouter",
    "IdentityAndTrustService",
    "IdentityResult",
    "OperationKind",
    "OperationSpec",
    "RequestContext",
    "RouteDefinition",
    "TrustResult",
    "build_router",
]
