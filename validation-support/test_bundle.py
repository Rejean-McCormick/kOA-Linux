from datetime import UTC, datetime
import json
import os
import subprocess
import sys

import pytest

from koa_kristal_runtime import (
    ConfigurationError,
    DependencySnapshot,
    DependencyState,
    EvidencePolicy,
    KristalReceiptFactory,
    KristalRuntimeConfig,
    ReceiptOutcome,
    RuntimeState,
    bootstrap,
)

NOW = datetime(2026, 8, 6, 14, 0, tzinfo=UTC)
DIGEST = 'sha256:' + 'a' * 64


def base_receipt():
    return dict(
        request_id='KRVER-12345678',
        correlation_id='CORR-12345678',
        outcome=ReceiptOutcome.VERIFIED,
        artifact_identity='runtime-pack:test',
        artifact_version='1.2.3',
        artifact_digest=DIGEST,
        actor_ref='component:test',
        occurred_at=NOW,
        verification_result_refs=('verify:schema', 'verify:digest'),
        candidate_runtime_pack_ref='runtime-pack:test@1.2.3',
    )


def test_default_configuration_is_canonical_and_public():
    cfg = KristalRuntimeConfig()
    data = cfg.as_public_dict()
    assert data['component_id'] == 'kristal_runtime'
    assert data['release_channel'] == 'knowledge'
    assert data['state_directory'] == '/var/lib/koa/kristal'
    assert 'secret' not in json.dumps(data).lower()


def test_unknown_environment_key_fails_closed():
    with pytest.raises(ConfigurationError, match='unknown configuration keys'):
        KristalRuntimeConfig.from_environment({'KOA_KRISTAL_RUNTIME_MAGIC': '1'})


def test_wrong_release_channel_is_rejected():
    with pytest.raises(ConfigurationError, match="release_channel must be 'knowledge'"):
        KristalRuntimeConfig(release_channel='system')


def test_parent_traversal_and_relative_paths_are_rejected():
    with pytest.raises(ConfigurationError):
        KristalRuntimeConfig(state_directory=__import__('pathlib').Path('../state'))


def test_unavailable_dependencies_are_blocked_not_ready():
    runtime = bootstrap(environment={}, dependencies=DependencySnapshot.unavailable())
    snapshot = runtime.health.snapshot()
    assert not snapshot.ready
    assert snapshot.runtime_state is RuntimeState.FAILED
    assert 'runtime_pack_activation' in snapshot.blocked_capabilities
    assert 'runtime_status_query' in snapshot.blocked_capabilities
    assert 'required_trust_unavailable' in snapshot.reasons


def test_ready_probe_exposes_declared_capabilities_only():
    runtime = bootstrap(environment={}, dependencies=DependencySnapshot.ready_for_local_probe())
    snapshot = runtime.health.snapshot()
    assert snapshot.ready
    assert snapshot.runtime_state is RuntimeState.ACTIVE
    assert set(snapshot.available_capabilities) >= {
        'kristal_identity_resolution',
        'runtime_pack_validation',
        'runtime_pack_activation',
        'runtime_pack_rollback',
        'runtime_status_query',
    }
    assert not snapshot.blocked_capabilities


def test_missing_policy_blocks_activation_but_not_identity_resolution():
    dep = DependencySnapshot.ready_for_local_probe()
    dep = dep.__class__(**{**{f: getattr(dep, f) for f in dep.__dataclass_fields__}, 'governance_policy_runtime': DependencyState.UNAVAILABLE})
    snap = bootstrap(environment={}, dependencies=dep).health.snapshot()
    assert 'kristal_identity_resolution' in snap.available_capabilities
    assert 'runtime_pack_activation' in snap.blocked_capabilities
    assert 'required_governance_authority_unavailable' in snap.reasons


def test_bounded_queue_is_explicit_degradation_not_silent_success():
    dep = DependencySnapshot.ready_for_local_probe()
    dep = dep.__class__(**{**{f: getattr(dep, f) for f in dep.__dataclass_fields__}, 'audit_broker': DependencyState.UNAVAILABLE})
    env = {'KOA_KRISTAL_RUNTIME_AUDIT_EVIDENCE_POLICY': EvidencePolicy.BOUNDED_QUEUE.value}
    snap = bootstrap(environment=env, dependencies=dep).health.snapshot()
    assert snap.ready
    assert 'evidence_forwarding_queued_within_bound' in snap.reasons


def test_verification_receipt_is_deterministic():
    factory = KristalReceiptFactory(runtime_version='0.1.0')
    one = factory.verification(**base_receipt())
    two = factory.verification(**base_receipt())
    assert one == two
    assert one.receipt_id.startswith('KRREC-')
    assert one.receipt_is_credential is False
    assert one.receipt_transfers_authority is False
    assert one.canonical_json() == two.canonical_json()


def test_activation_receipt_requires_all_preconditions():
    factory = KristalReceiptFactory(runtime_version='0.1.0')
    with pytest.raises(ValueError, match='successful activation requires'):
        factory.activation(
            request_id='KRACT-12345678', correlation_id='CORR-12345678',
            outcome=ReceiptOutcome.ACTIVATED, artifact_identity='runtime-pack:test',
            artifact_version='1.2.3', artifact_digest=DIGEST, actor_ref='component:test',
            occurred_at=NOW, candidate_runtime_pack_ref='runtime-pack:test@1.2.3',
        )
    receipt = factory.activation(
        request_id='KRACT-12345678', correlation_id='CORR-12345678',
        outcome=ReceiptOutcome.ACTIVATED, artifact_identity='runtime-pack:test',
        artifact_version='1.2.3', artifact_digest=DIGEST, actor_ref='component:test',
        occurred_at=NOW, verification_result_refs=('verify:all',),
        authorization_ref='decision:activate', resource_grant_ref='grant:resource',
        previous_runtime_pack_ref='runtime-pack:old@1.0.0',
        candidate_runtime_pack_ref='runtime-pack:test@1.2.3',
        active_runtime_pack_ref='runtime-pack:test@1.2.3', evidence_ref='evidence:activation',
    )
    assert receipt.atomic_transition
    assert not receipt.partial_activation
    assert receipt.last_valid_state_retained_until_success


def test_failure_receipt_requires_preserved_state_and_reason():
    factory = KristalReceiptFactory(runtime_version='0.1.0')
    with pytest.raises(ValueError):
        factory.failure(
            request_id='KRFAIL-12345678', correlation_id='CORR-12345678',
            outcome=ReceiptOutcome.FAILED, artifact_identity='runtime-pack:test',
            artifact_version='1.2.3', artifact_digest=DIGEST, actor_ref='component:test',
            occurred_at=NOW,
        )
    receipt = factory.failure(
        request_id='KRFAIL-12345678', correlation_id='CORR-12345678',
        outcome=ReceiptOutcome.FAILED, artifact_identity='runtime-pack:test',
        artifact_version='1.2.3', artifact_digest=DIGEST, actor_ref='component:test',
        occurred_at=NOW, reason_codes=('ACTIVATION_FAILED',),
        preserved_state_ref='runtime-pack:old@1.0.0',
    )
    assert receipt.preserved_state_ref == 'runtime-pack:old@1.0.0'


def test_cli_defaults_blocked_and_explicit_probe_ready(tmp_path):
    env = {**os.environ, 'PYTHONPATH': os.environ['PYTHONPATH']}
    blocked = subprocess.run([sys.executable, '-m', 'koa_kristal_runtime', 'health'], env=env, text=True, capture_output=True)
    assert blocked.returncode == 2
    ready = subprocess.run([sys.executable, '-m', 'koa_kristal_runtime', 'health', '--assume-local-prerequisites-ready'], env=env, text=True, capture_output=True)
    assert ready.returncode == 0
    assert json.loads(ready.stdout)['ready'] is True
