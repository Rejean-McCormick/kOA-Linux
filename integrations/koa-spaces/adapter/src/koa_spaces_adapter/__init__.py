"""Public API for the kOA-owned Koali Spaces integration adapter."""
from .bootstrap import AdapterConfig,KoaSpacesAdapter,bootstrap_adapter,build_adapter
from .capabilities import CapabilityResolver,CapabilitySnapshot,CapabilityState
from .client import BoundaryResponseError,SpacesClient,SpacesClientError,SpacesTransport,SubsystemUnavailable
from .health import HealthChecker,HealthReport,HealthState
from .host_bridge import HostBridge,HostBridgeError,HostLifecyclePort
from .interface_assets import AssetManifestValidationError,ValidatedAssetManifest,validate_asset_manifest
from .interface_theme import ThemeValidationError,ValidatedTheme,validate_theme
from .module_manifest import ManifestValidationError,ValidatedManifest,validate_manifest
from .receipts import ReceiptValidationError,artifact_digest,build_receipt,validate_receipt
from .route_bridge import RouteBridge,RouteCompositionError,RouteDecision,RouteState,RouteTable
from .shell_state import ShellState,ShellStateReader
from .space_activation import ActivationResult,AdmissionResult,SpaceActivationError,SpaceActivator,admit_space
from .unix_transport import UnixHttpTransport
__all__=[name for name in globals() if not name.startswith("_")]
