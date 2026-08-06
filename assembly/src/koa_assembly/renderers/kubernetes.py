"""Render resolved container plans as deterministic Kubernetes resources."""

from __future__ import annotations

from hashlib import sha256
from typing import Any

from . import (
    RenderError,
    RenderedFile,
    canonical_json_bytes,
    generated_metadata,
    normalize_plan,
    renderer_manifest,
    secret_ref_parts,
    validate_rendered_files,
)

_RENDERER = "kubernetes"


def _dns_name(value: str) -> str:
    normalized = value.lower().replace("_", "-").replace(".", "-")
    normalized = "-".join(part for part in normalized.split("-") if part)
    if len(normalized) <= 63:
        return normalized
    suffix = sha256(value.encode()).hexdigest()[:10]
    return normalized[:52].rstrip("-") + "-" + suffix


def _annotations(metadata: dict[str, Any]) -> dict[str, str]:
    return {
        "koa.io/generator": metadata["generator"],
        "koa.io/authority": metadata["authority"],
        "koa.io/plan-digest": metadata["plan_digest"],
        "koa.io/semantic-digest": metadata["semantic_digest"],
    }


def _quantity_bytes(value: int) -> str:
    return str(value)


def _network_label(network_id: str) -> str:
    return f"koa.io/network-{_dns_name(network_id)}"


def _deployment(plan: dict[str, Any], service: dict[str, Any], namespace: str, annotations: dict[str, str]) -> dict[str, Any]:
    if service["kind"] != "container":
        raise RenderError(f"Kubernetes renderer cannot represent native service {service['id']}")
    name = _dns_name(service["id"])
    env: list[dict[str, Any]] = []
    for key, value in service["environment"].items():
        if value["kind"] == "literal":
            env.append({"name": key, "value": value["value"]})
        else:
            secret, secret_key = secret_ref_parts(value["ref"])
            env.append({
                "name": key,
                "valueFrom": {"secretKeyRef": {"name": _dns_name(secret), "key": secret_key, "optional": False}},
            })
    ports = [
        {
            "name": _dns_name(item["name"])[:15],
            "containerPort": item["target"],
            "protocol": item["protocol"].upper(),
            **({"hostPort": item["published"], "hostIP": item["host_ip"]} if item["published"] is not None else {}),
        }
        for item in service["ports"]
    ]
    mounts = [{"name": _dns_name(item["volume"]), "mountPath": item["target"], "readOnly": item["read_only"]} for item in service["mounts"]]
    volumes = [{"name": _dns_name(item["volume"]), "persistentVolumeClaim": {"claimName": _dns_name(item["volume"])}} for item in service["mounts"]]
    limits: dict[str, str] = {}
    if "cpu_millis" in service["resources"]:
        limits["cpu"] = f"{service['resources']['cpu_millis']}m"
    if "memory_bytes" in service["resources"]:
        limits["memory"] = _quantity_bytes(service["resources"]["memory_bytes"])
    container: dict[str, Any] = {
        "name": name,
        "image": service["image"],
        "imagePullPolicy": "IfNotPresent",
        "securityContext": {
            "allowPrivilegeEscalation": False,
            "readOnlyRootFilesystem": True,
            "capabilities": {
                "drop": ["ALL"],
                "add": [item.removeprefix("CAP_") for item in service["capabilities"]],
            },
        },
    }
    if service["command"]:
        container["command"] = [service["command"][0]]
        if len(service["command"]) > 1:
            container["args"] = service["command"][1:]
    if env:
        container["env"] = env
    if ports:
        container["ports"] = ports
    if mounts:
        container["volumeMounts"] = mounts
    if limits:
        container["resources"] = {"limits": limits, "requests": limits}
    if service["healthcheck"]:
        health = service["healthcheck"]
        probe = {
            "exec": {"command": health["command"]},
            "periodSeconds": health["interval_seconds"],
            "timeoutSeconds": health["timeout_seconds"],
            "failureThreshold": health["retries"],
        }
        container["readinessProbe"] = probe
        container["livenessProbe"] = probe
    pod_spec: dict[str, Any] = {
        "automountServiceAccountToken": False,
        "enableServiceLinks": False,
        "containers": [container],
        "volumes": volumes,
        "securityContext": {"runAsNonRoot": True, "seccompProfile": {"type": "RuntimeDefault"}},
    }
    if service["user"] and service["user"].isdigit():
        pod_spec["securityContext"]["runAsUser"] = int(service["user"])
    labels = {"app.kubernetes.io/name": name, "koa.io/component": service["id"]}
    labels.update({_network_label(network): "true" for network in service["networks"]})
    selector = {"koa.io/component": service["id"]}
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name, "namespace": namespace, "labels": labels, "annotations": annotations},
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": selector},
            "template": {
                "metadata": {"labels": labels, "annotations": annotations},
                "spec": pod_spec,
            },
        },
    }


def render(plan: Any) -> tuple[RenderedFile, ...]:
    normalized = normalize_plan(plan)
    metadata = generated_metadata(_RENDERER, normalized)
    annotations = _annotations(metadata)
    namespace = _dns_name(f"koa-{normalized['profile_id']}")
    items: list[dict[str, Any]] = [
        {
            "apiVersion": "v1",
            "kind": "Namespace",
            "metadata": {"name": namespace, "labels": {"koa.io/profile": normalized["profile_id"]}, "annotations": annotations},
        },
        {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {"name": "koa-generation-manifest", "namespace": namespace, "annotations": annotations},
            "immutable": True,
            "data": {"manifest.json": canonical_json_bytes(metadata).decode("utf-8")},
        },
        {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {"name": "default-deny", "namespace": namespace, "annotations": annotations},
            "spec": {"podSelector": {}, "policyTypes": ["Ingress", "Egress"]},
        },
    ]
    for network in normalized["networks"]:
        network_selector = {"matchLabels": {_network_label(network["id"]): "true"}}
        egress = [
            {"to": [{"podSelector": network_selector}]},
            {
                "to": [{"namespaceSelector": {"matchLabels": {"kubernetes.io/metadata.name": "kube-system"}}}],
                "ports": [{"protocol": "UDP", "port": 53}, {"protocol": "TCP", "port": 53}],
            },
        ]
        if not network["internal"]:
            egress.append({"to": [{"ipBlock": {"cidr": "0.0.0.0/0"}}, {"ipBlock": {"cidr": "::/0"}}]})
        items.append({
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {"name": f"allow-{_dns_name(network['id'])}", "namespace": namespace, "annotations": annotations},
            "spec": {
                "podSelector": network_selector,
                "policyTypes": ["Ingress", "Egress"],
                "ingress": [{"from": [{"podSelector": network_selector}]}],
                "egress": egress,
            },
        })
    for volume in normalized["volumes"]:
        if volume["persistent"]:
            if volume["size_bytes"] is None:
                raise RenderError(f"Kubernetes volume {volume['id']} requires size_bytes")
            items.append({
                "apiVersion": "v1",
                "kind": "PersistentVolumeClaim",
                "metadata": {"name": _dns_name(volume["id"]), "namespace": namespace, "labels": {"koa.io/owner": volume["owner"]}, "annotations": annotations},
                "spec": {
                    "accessModes": ["ReadOnlyMany" if volume["read_only"] else "ReadWriteOnce"],
                    "resources": {"requests": {"storage": _quantity_bytes(volume["size_bytes"])}},
                },
            })
    for service in normalized["services"]:
        if not service["enabled"]:
            continue
        items.append(_deployment(normalized, service, namespace, annotations))
        if service["ports"]:
            items.append({
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {"name": _dns_name(service["id"]), "namespace": namespace, "annotations": annotations},
                "spec": {
                    "type": "ClusterIP",
                    "selector": {"koa.io/component": service["id"]},
                    "ports": [
                        {"name": _dns_name(item["name"])[:15], "port": item["target"], "targetPort": item["target"], "protocol": item["protocol"].upper()}
                        for item in service["ports"]
                    ],
                },
            })
    document = {"apiVersion": "v1", "kind": "List", "metadata": {"annotations": annotations}, "items": items}
    manifest = RenderedFile("kubernetes/manifests.yaml", canonical_json_bytes(document), "application/yaml")
    files = [manifest]
    files.append(renderer_manifest(_RENDERER, normalized, files))
    return validate_rendered_files(files)
