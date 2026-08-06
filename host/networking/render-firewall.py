#!/usr/bin/env python3
"""Render a closed-by-default nftables policy for a sovereign Linux node.

The renderer consumes only the static policy files in this directory and a
separate deployment TOML.  The deployment file is intentionally external to
this bundle: addresses, interfaces, ports, providers, and active routes are
owned by the active profile composition and integration contracts.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_VERSION = 1
PROFILE_ID = "sovereign_linux_node"
CANONICAL_ZONES = {
    "public",
    "private",
    "governance",
    "administration",
    "federation",
    "backup",
    "development",
    "external_integration",
    "quarantine",
}
POLICY_FILES = {
    "restricted": "restricted-policy.toml",
    "offline": "offline-policy.toml",
}
IDENTIFIER_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
ROUTE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}$")
INTERFACE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,14}$")
REFERENCE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_./:#@+-]{0,255}$")
LOG_RATE_RE = re.compile(r"^[1-9][0-9]*/(?:second|minute|hour|day)$")
TEMPLATE_MARKERS = {
    "GENERATED_HEADER",
    "TABLE_FAMILY",
    "TABLE_NAME",
    "INPUT_ICMP_RULES",
    "INPUT_RULES",
    "INPUT_TERMINAL",
    "FORWARD_RULES",
    "FORWARD_TERMINAL",
    "OUTPUT_ICMP_RULES",
    "OUTPUT_RULES",
    "OUTPUT_TERMINAL",
}


class ConfigurationError(ValueError):
    """Raised when policy or deployment data is incomplete or unsafe."""


@dataclass(frozen=True)
class Zone:
    zone_id: str
    purpose: str
    profile_permitted: bool
    active_by_default: bool
    requires_explicit_activation: bool
    requires_identity_and_application_authorization: bool


@dataclass(frozen=True)
class Service:
    service_id: str
    owner: str
    zone: str
    direction: str
    transport: str
    local_only: bool
    public_exposure_allowed: bool
    authenticated_encryption_required: bool
    application_authorization_required: bool
    payload_contract_required: bool
    integration_metadata_required: bool
    exact_destination_required: bool
    default_enabled: bool
    failure_behavior: str


@dataclass(frozen=True)
class Policy:
    policy_id: str
    input_default: str
    output_default: str
    forward_default: str
    allow_loopback: bool
    allow_established_related: bool
    allow_icmp: bool
    allow_forwarding: bool
    require_explicit_route: bool
    require_bound_interface: bool
    log_denied_packets: bool
    log_rate: str
    max_ports_per_route: int
    require_non_global_addresses: bool
    allow_wildcard_sources_for: frozenset[str]
    permitted_zones: frozenset[str]
    permitted_services: frozenset[str]
    forbidden_services: frozenset[str]


@dataclass(frozen=True)
class Route:
    route_id: str
    service: Service
    interface: str
    source_identity: str
    destination_identity: str
    operation_class: str
    scope: str
    purpose: str
    data_classification: str
    payload_contract: str
    lifecycle: str
    failure_behavior: str
    contract_ref: str
    sources: tuple[ipaddress.IPv4Network | ipaddress.IPv6Network, ...]
    destinations: tuple[ipaddress.IPv4Network | ipaddress.IPv6Network, ...]
    ports: tuple[int, ...]
    provider: str | None
    retention: str | None
    reuse: str | None
    return_path: str | None


def _load_toml(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError(f"cannot load TOML {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigurationError(f"TOML root must be a table: {path}")
    return data


def _require_keys(table: Mapping[str, Any], required: set[str], context: str) -> None:
    missing = sorted(required - set(table))
    if missing:
        raise ConfigurationError(f"{context} is missing required keys: {', '.join(missing)}")


def _reject_unknown_keys(table: Mapping[str, Any], allowed: set[str], context: str) -> None:
    unknown = sorted(set(table) - allowed)
    if unknown:
        raise ConfigurationError(f"{context} contains unsupported keys: {', '.join(unknown)}")


def _expect_bool(value: Any, context: str) -> bool:
    if type(value) is not bool:
        raise ConfigurationError(f"{context} must be a boolean")
    return value


def _expect_string(value: Any, context: str, *, pattern: re.Pattern[str] | None = None) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{context} must be a non-empty string")
    result = value.strip()
    if "\n" in result or "\r" in result or "\x00" in result:
        raise ConfigurationError(f"{context} contains a prohibited control character")
    if pattern is not None and pattern.fullmatch(result) is None:
        raise ConfigurationError(f"{context} has an unsupported value: {result!r}")
    return result


def _expect_string_list(value: Any, context: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ConfigurationError(f"{context} must be an array of strings")
    return [item.strip() for item in value]


def _validate_common_document(data: Mapping[str, Any], context: str) -> None:
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ConfigurationError(f"{context}.schema_version must equal {SCHEMA_VERSION}")
    if data.get("profile_id") != PROFILE_ID:
        raise ConfigurationError(f"{context}.profile_id must equal {PROFILE_ID!r}")


def _load_zones(path: Path) -> tuple[dict[str, Zone], str, str]:
    data = _load_toml(path)
    _reject_unknown_keys(
        data,
        {
            "schema_version",
            "profile_id",
            "table_family",
            "table_name",
            "physical_colocation_transfers_authority",
            "forwarding_required",
            "zone",
        },
        "zones",
    )
    _validate_common_document(data, "zones")
    table_family = _expect_string(data.get("table_family"), "zones.table_family", pattern=IDENTIFIER_RE)
    table_name = _expect_string(data.get("table_name"), "zones.table_name", pattern=IDENTIFIER_RE)
    if table_family != "inet":
        raise ConfigurationError("zones.table_family must be 'inet' for dual-stack policy")
    if _expect_bool(
        data.get("physical_colocation_transfers_authority"),
        "zones.physical_colocation_transfers_authority",
    ):
        raise ConfigurationError("physical co-location cannot transfer authority")
    if _expect_bool(data.get("forwarding_required"), "zones.forwarding_required"):
        raise ConfigurationError("the sovereign Linux node baseline cannot require IP forwarding")

    entries = data.get("zone")
    if not isinstance(entries, list):
        raise ConfigurationError("zones.zone must be an array of tables")
    zones: dict[str, Zone] = {}
    allowed = {
        "id",
        "purpose",
        "profile_permitted",
        "active_by_default",
        "requires_explicit_activation",
        "requires_identity_and_application_authorization",
    }
    for index, entry in enumerate(entries):
        context = f"zones.zone[{index}]"
        if not isinstance(entry, dict):
            raise ConfigurationError(f"{context} must be a table")
        _reject_unknown_keys(entry, allowed, context)
        _require_keys(entry, allowed, context)
        zone_id = _expect_string(entry["id"], f"{context}.id", pattern=IDENTIFIER_RE)
        if zone_id in zones:
            raise ConfigurationError(f"duplicate zone id: {zone_id}")
        zone = Zone(
            zone_id=zone_id,
            purpose=_expect_string(entry["purpose"], f"{context}.purpose"),
            profile_permitted=_expect_bool(entry["profile_permitted"], f"{context}.profile_permitted"),
            active_by_default=_expect_bool(entry["active_by_default"], f"{context}.active_by_default"),
            requires_explicit_activation=_expect_bool(
                entry["requires_explicit_activation"],
                f"{context}.requires_explicit_activation",
            ),
            requires_identity_and_application_authorization=_expect_bool(
                entry["requires_identity_and_application_authorization"],
                f"{context}.requires_identity_and_application_authorization",
            ),
        )
        if zone.active_by_default:
            raise ConfigurationError(f"zone {zone_id} cannot be active by default")
        if not zone.requires_explicit_activation:
            raise ConfigurationError(f"zone {zone_id} must require explicit activation")
        if not zone.requires_identity_and_application_authorization:
            raise ConfigurationError(f"zone {zone_id} must retain application authorization")
        zones[zone_id] = zone
    if set(zones) != CANONICAL_ZONES:
        missing = sorted(CANONICAL_ZONES - set(zones))
        extra = sorted(set(zones) - CANONICAL_ZONES)
        raise ConfigurationError(f"zone catalog mismatch; missing={missing}, extra={extra}")
    if zones["development"].profile_permitted:
        raise ConfigurationError("development zone must be prohibited by the production profile")
    return zones, table_family, table_name


def _load_services(path: Path, zones: Mapping[str, Zone]) -> dict[str, Service]:
    data = _load_toml(path)
    top_allowed = {
        "schema_version",
        "profile_id",
        "allow_undeclared_services",
        "wildcard_binding_permitted",
        "databases_publicly_exposed",
        "metrics_publicly_exposed",
        "privileged_interfaces_publicly_exposed",
        "service",
    }
    _reject_unknown_keys(data, top_allowed, "service_exposure")
    _validate_common_document(data, "service_exposure")
    for key in (
        "allow_undeclared_services",
        "wildcard_binding_permitted",
        "databases_publicly_exposed",
        "metrics_publicly_exposed",
        "privileged_interfaces_publicly_exposed",
    ):
        if _expect_bool(data.get(key), f"service_exposure.{key}"):
            raise ConfigurationError(f"service_exposure.{key} must remain false")

    entries = data.get("service")
    if not isinstance(entries, list):
        raise ConfigurationError("service_exposure.service must be an array of tables")
    allowed = {
        "id",
        "owner",
        "zone",
        "direction",
        "transport",
        "local_only",
        "public_exposure_allowed",
        "authenticated_encryption_required",
        "application_authorization_required",
        "payload_contract_required",
        "integration_metadata_required",
        "exact_destination_required",
        "default_enabled",
        "failure_behavior",
    }
    services: dict[str, Service] = {}
    for index, entry in enumerate(entries):
        context = f"service_exposure.service[{index}]"
        if not isinstance(entry, dict):
            raise ConfigurationError(f"{context} must be a table")
        _reject_unknown_keys(entry, allowed, context)
        _require_keys(entry, allowed, context)
        service_id = _expect_string(entry["id"], f"{context}.id", pattern=IDENTIFIER_RE)
        if service_id in services:
            raise ConfigurationError(f"duplicate service id: {service_id}")
        zone_id = _expect_string(entry["zone"], f"{context}.zone", pattern=IDENTIFIER_RE)
        if zone_id not in zones:
            raise ConfigurationError(f"service {service_id} uses unknown zone {zone_id}")
        direction = _expect_string(entry["direction"], f"{context}.direction")
        transport = _expect_string(entry["transport"], f"{context}.transport")
        if direction not in {"inbound", "outbound", "local_only"}:
            raise ConfigurationError(f"service {service_id} has unsupported direction {direction}")
        if transport not in {"tcp", "udp", "unix"}:
            raise ConfigurationError(f"service {service_id} has unsupported transport {transport}")
        local_only = _expect_bool(entry["local_only"], f"{context}.local_only")
        if local_only != (direction == "local_only"):
            raise ConfigurationError(f"service {service_id} has inconsistent local_only/direction")
        if local_only and transport != "unix":
            raise ConfigurationError(f"local-only service {service_id} must use a Unix socket")
        if not local_only and transport == "unix":
            raise ConfigurationError(f"network service {service_id} cannot use Unix transport")
        service = Service(
            service_id=service_id,
            owner=_expect_string(entry["owner"], f"{context}.owner", pattern=IDENTIFIER_RE),
            zone=zone_id,
            direction=direction,
            transport=transport,
            local_only=local_only,
            public_exposure_allowed=_expect_bool(
                entry["public_exposure_allowed"],
                f"{context}.public_exposure_allowed",
            ),
            authenticated_encryption_required=_expect_bool(
                entry["authenticated_encryption_required"],
                f"{context}.authenticated_encryption_required",
            ),
            application_authorization_required=_expect_bool(
                entry["application_authorization_required"],
                f"{context}.application_authorization_required",
            ),
            payload_contract_required=_expect_bool(
                entry["payload_contract_required"],
                f"{context}.payload_contract_required",
            ),
            integration_metadata_required=_expect_bool(
                entry["integration_metadata_required"],
                f"{context}.integration_metadata_required",
            ),
            exact_destination_required=_expect_bool(
                entry["exact_destination_required"],
                f"{context}.exact_destination_required",
            ),
            default_enabled=_expect_bool(entry["default_enabled"], f"{context}.default_enabled"),
            failure_behavior=_expect_string(
                entry["failure_behavior"],
                f"{context}.failure_behavior",
                pattern=IDENTIFIER_RE,
            ),
        )
        if service.default_enabled:
            raise ConfigurationError(f"service {service_id} cannot be enabled by default")
        if service.public_exposure_allowed != (service.zone == "public"):
            raise ConfigurationError(
                f"service {service_id} has an invalid public_exposure_allowed setting"
            )
        if service.zone == "development":
            raise ConfigurationError("production service catalog cannot expose the development zone")
        services[service_id] = service
    return services


def _load_policy(path: Path, expected_id: str, zones: Mapping[str, Zone], services: Mapping[str, Service]) -> Policy:
    data = _load_toml(path)
    allowed = {
        "schema_version",
        "policy_id",
        "profile_id",
        "input_default",
        "output_default",
        "forward_default",
        "allow_loopback",
        "allow_established_related",
        "allow_icmp",
        "allow_forwarding",
        "require_explicit_route",
        "require_bound_interface",
        "log_denied_packets",
        "log_rate",
        "max_ports_per_route",
        "require_non_global_addresses",
        "allow_wildcard_sources_for",
        "permitted_zones",
        "permitted_services",
        "forbidden_services",
    }
    _reject_unknown_keys(data, allowed, f"policy.{expected_id}")
    _require_keys(data, allowed, f"policy.{expected_id}")
    _validate_common_document(data, f"policy.{expected_id}")
    policy_id = _expect_string(data["policy_id"], f"policy.{expected_id}.policy_id", pattern=IDENTIFIER_RE)
    if policy_id != expected_id:
        raise ConfigurationError(f"policy id {policy_id!r} does not match {expected_id!r}")
    defaults = [data["input_default"], data["output_default"], data["forward_default"]]
    if defaults != ["drop", "drop", "drop"]:
        raise ConfigurationError(f"policy {expected_id} must default-drop input, output, and forward")
    if not _expect_bool(data["allow_loopback"], f"policy.{expected_id}.allow_loopback"):
        raise ConfigurationError(f"policy {expected_id} must retain loopback")
    if not _expect_bool(
        data["allow_established_related"],
        f"policy.{expected_id}.allow_established_related",
    ):
        raise ConfigurationError(f"policy {expected_id} must permit established/related traffic")
    if _expect_bool(data["allow_forwarding"], f"policy.{expected_id}.allow_forwarding"):
        raise ConfigurationError(f"policy {expected_id} cannot enable forwarding")
    if not _expect_bool(
        data["require_explicit_route"],
        f"policy.{expected_id}.require_explicit_route",
    ):
        raise ConfigurationError(f"policy {expected_id} must require explicit routes")
    if not _expect_bool(
        data["require_bound_interface"],
        f"policy.{expected_id}.require_bound_interface",
    ):
        raise ConfigurationError(f"policy {expected_id} must require bound interfaces")
    log_rate = _expect_string(data["log_rate"], f"policy.{expected_id}.log_rate")
    if LOG_RATE_RE.fullmatch(log_rate) is None:
        raise ConfigurationError(f"policy {expected_id} has invalid log_rate {log_rate!r}")
    max_ports = data["max_ports_per_route"]
    if type(max_ports) is not int or not 1 <= max_ports <= 32:
        raise ConfigurationError(f"policy {expected_id}.max_ports_per_route must be 1..32")
    permitted_zones = frozenset(_expect_string_list(data["permitted_zones"], f"policy.{expected_id}.permitted_zones"))
    permitted_services = frozenset(
        _expect_string_list(data["permitted_services"], f"policy.{expected_id}.permitted_services")
    )
    forbidden_services = frozenset(
        _expect_string_list(data["forbidden_services"], f"policy.{expected_id}.forbidden_services")
    )
    if not permitted_zones <= set(zones):
        raise ConfigurationError(f"policy {expected_id} contains unknown zones")
    if any(not zones[zone].profile_permitted for zone in permitted_zones):
        raise ConfigurationError(f"policy {expected_id} permits a profile-prohibited zone")
    if not permitted_services <= set(services) or not forbidden_services <= set(services):
        raise ConfigurationError(f"policy {expected_id} contains unknown services")
    if permitted_services & forbidden_services:
        raise ConfigurationError(f"policy {expected_id} both permits and forbids a service")
    if permitted_services | forbidden_services != set(services):
        missing = sorted(set(services) - permitted_services - forbidden_services)
        raise ConfigurationError(f"policy {expected_id} does not classify services: {missing}")
    if any(services[item].zone not in permitted_zones for item in permitted_services):
        bad = sorted(item for item in permitted_services if services[item].zone not in permitted_zones)
        raise ConfigurationError(f"policy {expected_id} permits services in prohibited zones: {bad}")
    wildcard_services = frozenset(
        _expect_string_list(
            data["allow_wildcard_sources_for"],
            f"policy.{expected_id}.allow_wildcard_sources_for",
        )
    )
    if not wildcard_services <= permitted_services:
        raise ConfigurationError(f"policy {expected_id} permits wildcard sources for an unavailable service")
    if wildcard_services - {"public_web"}:
        raise ConfigurationError("only the declared public web service may use wildcard source ranges")
    return Policy(
        policy_id=policy_id,
        input_default="drop",
        output_default="drop",
        forward_default="drop",
        allow_loopback=True,
        allow_established_related=True,
        allow_icmp=_expect_bool(data["allow_icmp"], f"policy.{expected_id}.allow_icmp"),
        allow_forwarding=False,
        require_explicit_route=True,
        require_bound_interface=True,
        log_denied_packets=_expect_bool(
            data["log_denied_packets"],
            f"policy.{expected_id}.log_denied_packets",
        ),
        log_rate=log_rate,
        max_ports_per_route=max_ports,
        require_non_global_addresses=_expect_bool(
            data["require_non_global_addresses"],
            f"policy.{expected_id}.require_non_global_addresses",
        ),
        allow_wildcard_sources_for=wildcard_services,
        permitted_zones=permitted_zones,
        permitted_services=permitted_services,
        forbidden_services=forbidden_services,
    )


def _load_template(path: Path) -> str:
    try:
        template = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigurationError(f"cannot read template {path}: {exc}") from exc
    found = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", template))
    if found != TEMPLATE_MARKERS:
        raise ConfigurationError(
            f"firewall template markers mismatch; missing={sorted(TEMPLATE_MARKERS - found)}, "
            f"extra={sorted(found - TEMPLATE_MARKERS)}"
        )
    return template


def _parse_networks(value: Any, context: str) -> tuple[ipaddress.IPv4Network | ipaddress.IPv6Network, ...]:
    values = _expect_string_list(value, context)
    networks: set[ipaddress.IPv4Network | ipaddress.IPv6Network] = set()
    for item in values:
        try:
            network = ipaddress.ip_network(item, strict=True)
        except ValueError as exc:
            raise ConfigurationError(f"{context} contains invalid CIDR {item!r}: {exc}") from exc
        networks.add(network)
    return tuple(sorted(networks, key=lambda net: (net.version, int(net.network_address), net.prefixlen)))


def _parse_ports(value: Any, context: str, maximum: int) -> tuple[int, ...]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ConfigurationError(f"{context} must be an array of integer ports")
    ports = tuple(sorted(set(value)))
    if not ports or len(ports) > maximum or any(not 1 <= port <= 65535 for port in ports):
        raise ConfigurationError(f"{context} must contain 1..{maximum} unique ports in 1..65535")
    return ports


def _is_wildcard(network: ipaddress.IPv4Network | ipaddress.IPv6Network) -> bool:
    return network.prefixlen == 0


def _is_non_global(network: ipaddress.IPv4Network | ipaddress.IPv6Network) -> bool:
    addresses = (network.network_address, network.broadcast_address)
    return all(not address.is_global for address in addresses)


def _load_deployment(
    path: Path,
    policy: Policy,
    zones: Mapping[str, Zone],
    services: Mapping[str, Service],
) -> tuple[dict[str, tuple[str, ...]], tuple[Route, ...]]:
    data = _load_toml(path)
    allowed_top = {"schema_version", "profile_id", "policy_id", "zones", "routes"}
    _reject_unknown_keys(data, allowed_top, "deployment")
    _require_keys(data, allowed_top, "deployment")
    _validate_common_document(data, "deployment")
    if data["policy_id"] != policy.policy_id:
        raise ConfigurationError(
            f"deployment.policy_id must equal selected policy {policy.policy_id!r}"
        )
    zone_data = data["zones"]
    if not isinstance(zone_data, dict):
        raise ConfigurationError("deployment.zones must be a table")
    if not set(zone_data) <= policy.permitted_zones:
        raise ConfigurationError("deployment contains a zone not permitted by the selected policy")
    zone_interfaces: dict[str, tuple[str, ...]] = {}
    seen_interfaces: dict[str, str] = {}
    for zone_id, raw_interfaces in zone_data.items():
        if zone_id not in zones:
            raise ConfigurationError(f"deployment uses unknown zone {zone_id}")
        interfaces = _expect_string_list(raw_interfaces, f"deployment.zones.{zone_id}")
        if not interfaces:
            raise ConfigurationError(f"deployment.zones.{zone_id} cannot be empty")
        normalized: list[str] = []
        for interface in interfaces:
            checked = _expect_string(
                interface,
                f"deployment.zones.{zone_id}",
                pattern=INTERFACE_RE,
            )
            other_zone = seen_interfaces.get(checked)
            if other_zone is not None and other_zone != zone_id:
                raise ConfigurationError(
                    f"interface {checked!r} is assigned to both {other_zone} and {zone_id}; "
                    "physical co-location requires distinct logical interfaces or an external "
                    "profile-approved mapping"
                )
            seen_interfaces[checked] = zone_id
            normalized.append(checked)
        zone_interfaces[zone_id] = tuple(sorted(set(normalized)))

    raw_routes = data["routes"]
    if not isinstance(raw_routes, list):
        raise ConfigurationError("deployment.routes must be an array of tables")
    route_allowed = {
        "route_id",
        "service_id",
        "enabled",
        "interface",
        "source_identity",
        "destination_identity",
        "operation_class",
        "scope",
        "purpose",
        "data_classification",
        "payload_contract",
        "lifecycle",
        "failure_behavior",
        "contract_ref",
        "sources",
        "destinations",
        "ports",
        "provider",
        "retention",
        "reuse",
        "return_path",
    }
    required = {
        "route_id",
        "service_id",
        "enabled",
        "interface",
        "source_identity",
        "destination_identity",
        "operation_class",
        "scope",
        "purpose",
        "data_classification",
        "payload_contract",
        "lifecycle",
        "failure_behavior",
        "contract_ref",
        "sources",
        "destinations",
        "ports",
    }
    routes: list[Route] = []
    seen_route_ids: set[str] = set()
    for index, entry in enumerate(raw_routes):
        context = f"deployment.routes[{index}]"
        if not isinstance(entry, dict):
            raise ConfigurationError(f"{context} must be a table")
        _reject_unknown_keys(entry, route_allowed, context)
        _require_keys(entry, required, context)
        enabled = _expect_bool(entry["enabled"], f"{context}.enabled")
        if not enabled:
            continue
        route_id = _expect_string(entry["route_id"], f"{context}.route_id", pattern=ROUTE_ID_RE)
        if route_id in seen_route_ids:
            raise ConfigurationError(f"duplicate active route id: {route_id}")
        seen_route_ids.add(route_id)
        service_id = _expect_string(entry["service_id"], f"{context}.service_id", pattern=IDENTIFIER_RE)
        if service_id not in services:
            raise ConfigurationError(f"route {route_id} uses undeclared service {service_id}")
        if service_id not in policy.permitted_services:
            raise ConfigurationError(f"route {route_id} uses policy-prohibited service {service_id}")
        service = services[service_id]
        if service.local_only:
            raise ConfigurationError(
                f"route {route_id} attempts to render local-only service {service_id}; "
                "Unix-socket access is not a firewall route"
            )
        if service.zone not in zone_interfaces:
            raise ConfigurationError(f"route {route_id} has no declared interface for zone {service.zone}")
        interface = _expect_string(entry["interface"], f"{context}.interface", pattern=INTERFACE_RE)
        if interface not in zone_interfaces[service.zone]:
            raise ConfigurationError(
                f"route {route_id} interface {interface!r} is not assigned to zone {service.zone}"
            )
        sources = _parse_networks(entry["sources"], f"{context}.sources")
        destinations = _parse_networks(entry["destinations"], f"{context}.destinations")
        ports = _parse_ports(entry["ports"], f"{context}.ports", policy.max_ports_per_route)
        if service.direction == "inbound":
            if not sources or destinations:
                raise ConfigurationError(
                    f"inbound route {route_id} requires sources and prohibits destinations"
                )
            wildcards = [network for network in sources if _is_wildcard(network)]
            if wildcards and service_id not in policy.allow_wildcard_sources_for:
                raise ConfigurationError(f"route {route_id} uses a prohibited wildcard source")
        elif service.direction == "outbound":
            if not destinations or sources:
                raise ConfigurationError(
                    f"outbound route {route_id} requires destinations and prohibits sources"
                )
            if any(_is_wildcard(network) for network in destinations):
                raise ConfigurationError(f"route {route_id} cannot use a wildcard destination")
            if service.exact_destination_required and any(
                network.prefixlen != network.max_prefixlen for network in destinations
            ):
                raise ConfigurationError(f"route {route_id} requires exact destination addresses")
        if policy.require_non_global_addresses:
            all_networks = (*sources, *destinations)
            if any(not _is_non_global(network) for network in all_networks):
                raise ConfigurationError(
                    f"offline route {route_id} contains a globally routable address"
                )
        provider = entry.get("provider")
        retention = entry.get("retention")
        reuse = entry.get("reuse")
        return_path = entry.get("return_path")
        if service.integration_metadata_required:
            for key, value in (
                ("provider", provider),
                ("retention", retention),
                ("reuse", reuse),
                ("return_path", return_path),
            ):
                _expect_string(value, f"{context}.{key}", pattern=REFERENCE_RE)
        else:
            for key, value in (
                ("provider", provider),
                ("retention", retention),
                ("reuse", reuse),
                ("return_path", return_path),
            ):
                if value is not None:
                    _expect_string(value, f"{context}.{key}", pattern=REFERENCE_RE)
        route = Route(
            route_id=route_id,
            service=service,
            interface=interface,
            source_identity=_expect_string(
                entry["source_identity"], f"{context}.source_identity", pattern=REFERENCE_RE
            ),
            destination_identity=_expect_string(
                entry["destination_identity"],
                f"{context}.destination_identity",
                pattern=REFERENCE_RE,
            ),
            operation_class=_expect_string(
                entry["operation_class"], f"{context}.operation_class", pattern=IDENTIFIER_RE
            ),
            scope=_expect_string(entry["scope"], f"{context}.scope", pattern=REFERENCE_RE),
            purpose=_expect_string(entry["purpose"], f"{context}.purpose", pattern=REFERENCE_RE),
            data_classification=_expect_string(
                entry["data_classification"],
                f"{context}.data_classification",
                pattern=IDENTIFIER_RE,
            ),
            payload_contract=_expect_string(
                entry["payload_contract"],
                f"{context}.payload_contract",
                pattern=REFERENCE_RE,
            ),
            lifecycle=_expect_string(
                entry["lifecycle"], f"{context}.lifecycle", pattern=IDENTIFIER_RE
            ),
            failure_behavior=_expect_string(
                entry["failure_behavior"],
                f"{context}.failure_behavior",
                pattern=IDENTIFIER_RE,
            ),
            contract_ref=_expect_string(
                entry["contract_ref"], f"{context}.contract_ref", pattern=REFERENCE_RE
            ),
            sources=sources,
            destinations=destinations,
            ports=ports,
            provider=provider,
            retention=retention,
            reuse=reuse,
            return_path=return_path,
        )
        if route.failure_behavior != service.failure_behavior:
            raise ConfigurationError(
                f"route {route_id} failure_behavior must preserve the service contract value "
                f"{service.failure_behavior!r}"
            )
        routes.append(route)
    return zone_interfaces, tuple(sorted(routes, key=lambda item: item.route_id))


def _format_addresses(networks: Sequence[ipaddress.IPv4Network | ipaddress.IPv6Network]) -> list[str]:
    return [str(network) for network in networks]


def _format_ports(ports: Sequence[int]) -> str:
    if len(ports) == 1:
        return str(ports[0])
    return "{ " + ", ".join(str(port) for port in ports) + " }"


def _render_route_rules(route: Route) -> list[str]:
    networks = route.sources if route.service.direction == "inbound" else route.destinations
    expression = "saddr" if route.service.direction == "inbound" else "daddr"
    interface_expression = "iifname" if route.service.direction == "inbound" else "oifname"
    family_groups: dict[int, list[str]] = {4: [], 6: []}
    for network in networks:
        family_groups[network.version].append(str(network))
    lines: list[str] = []
    for version in (4, 6):
        values = family_groups[version]
        if not values:
            continue
        family_keyword = "ip" if version == 4 else "ip6"
        address_value = values[0] if len(values) == 1 else "{ " + ", ".join(values) + " }"
        line = (
            f'        {interface_expression} "{route.interface}" '
            f"{family_keyword} {expression} {address_value} "
            f"{route.service.transport} dport {_format_ports(route.ports)} "
            f'accept comment "koa:{route.route_id}"'
        )
        lines.append(line)
    return lines


def _terminal_rule(chain: str, policy: Policy) -> str:
    if policy.log_denied_packets:
        return (
            f'        limit rate {policy.log_rate} counter log prefix '
            f'"koa-{chain}-deny " flags all drop'
        )
    return "        counter drop"


def _render(
    template: str,
    table_family: str,
    table_name: str,
    policy: Policy,
    routes: Sequence[Route],
) -> str:
    input_rules: list[str] = []
    output_rules: list[str] = []
    for route in routes:
        rules = _render_route_rules(route)
        if route.service.direction == "inbound":
            input_rules.extend(rules)
        else:
            output_rules.extend(rules)
    input_icmp = ""
    output_icmp = ""
    if policy.allow_icmp:
        input_icmp = (
            '        ip protocol icmp accept comment "koa:icmpv4"\n'
            '        ip6 nexthdr ipv6-icmp accept comment "koa:icmpv6"'
        )
        output_icmp = input_icmp
    replacements = {
        "GENERATED_HEADER": (
            "# Generated by host/networking/render-firewall.py; do not edit.\n"
            f"# profile={PROFILE_ID} policy={policy.policy_id} routes={len(routes)}"
        ),
        "TABLE_FAMILY": table_family,
        "TABLE_NAME": table_name,
        "INPUT_ICMP_RULES": input_icmp,
        "INPUT_RULES": "\n".join(input_rules),
        "INPUT_TERMINAL": _terminal_rule("input", policy),
        "FORWARD_RULES": "",
        "FORWARD_TERMINAL": _terminal_rule("forward", policy),
        "OUTPUT_ICMP_RULES": output_icmp,
        "OUTPUT_RULES": "\n".join(output_rules),
        "OUTPUT_TERMINAL": _terminal_rule("output", policy),
    }
    rendered = template
    for marker, value in replacements.items():
        rendered = rendered.replace("{{" + marker + "}}", value)
    if re.search(r"\{\{[A-Z0-9_]+\}\}", rendered):
        raise ConfigurationError("unresolved firewall template marker")
    return rendered.rstrip() + "\n"


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            temporary_name = ""
        raise


def _summary(
    zones: Mapping[str, Zone],
    services: Mapping[str, Service],
    policy: Policy,
    routes: Sequence[Route] | None,
) -> str:
    result = {
        "profile_id": PROFILE_ID,
        "policy_id": policy.policy_id,
        "zone_count": len(zones),
        "service_count": len(services),
        "network_service_count": sum(not service.local_only for service in services.values()),
        "local_only_service_count": sum(service.local_only for service in services.values()),
        "active_route_count": None if routes is None else len(routes),
        "default_input": policy.input_default,
        "default_output": policy.output_default,
        "default_forward": policy.forward_default,
        "forwarding": policy.allow_forwarding,
    }
    return json.dumps(result, sort_keys=True, indent=2) + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and render the kOA sovereign-node nftables policy.",
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="directory containing zones, exposure, policy, and template files",
    )
    parser.add_argument(
        "--policy",
        choices=sorted(POLICY_FILES),
        default="restricted",
        help="policy mode to validate or render",
    )
    parser.add_argument(
        "--deployment",
        type=Path,
        help="deployment TOML containing explicit interfaces and active routes",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="write the rendered nftables candidate atomically instead of stdout",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate inputs and print a deterministic JSON summary",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    config_dir = args.config_dir.resolve()
    try:
        zones, table_family, table_name = _load_zones(config_dir / "zones.toml")
        services = _load_services(config_dir / "service-exposure.toml", zones)
        policy = _load_policy(
            config_dir / POLICY_FILES[args.policy],
            args.policy,
            zones,
            services,
        )
        template = _load_template(config_dir / "firewall.nft.in")
        routes: tuple[Route, ...] | None = None
        if args.deployment is not None:
            _, routes = _load_deployment(args.deployment.resolve(), policy, zones, services)
        if args.check:
            sys.stdout.write(_summary(zones, services, policy, routes))
            return 0
        if routes is None:
            raise ConfigurationError("--deployment is required when rendering a firewall")
        rendered = _render(template, table_family, table_name, policy, routes)
        if args.output is None:
            sys.stdout.write(rendered)
        else:
            _atomic_write(args.output.resolve(), rendered)
        return 0
    except ConfigurationError as exc:
        print(f"render-firewall: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"render-firewall: operating-system error: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
