from __future__ import annotations

import sys
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_governance_policy_runtime.domain import (  # noqa: E402
    AllExpression,
    AnyExpression,
    CompareExpression,
    CompareOperator,
    ContainsExpression,
    ContextClassification,
    DecisionClass,
    DecisionDiagnostic,
    DecisionResult,
    DiagnosticSeverity,
    DomainValidationError,
    EvaluationContext,
    ExistsExpression,
    MatchesExpression,
    MissingContextFact,
    NotExpression,
    ObligationType,
    Operand,
    PolicyBundle,
    PolicyBundleStatus,
    PolicyDecision,
    PolicyDomain,
    PolicyModule,
    PolicyObligation,
    PolicyRule,
    PolicySet,
    PolicySetState,
    RuleDecision,
    RuleOutcome,
    VerifiedContextFact,
)

UTC = timezone.utc
T0 = datetime(2026, 8, 6, 12, 0, tzinfo=UTC)


def make_fact(name: str, value: object, **overrides: object) -> VerifiedContextFact:
    values: dict[str, object] = {
        "name": name,
        "value": value,
        "source_authority_ref": f"authority:{name}",
        "evidence_ref": f"evidence:{name}",
        "verified_at": T0 - timedelta(minutes=1),
        "valid_until": T0 + timedelta(hours=1),
        "classification": ContextClassification.RESTRICTED,
    }
    values.update(overrides)
    return VerifiedContextFact(**values)  # type: ignore[arg-type]


def authorization_facts() -> tuple[VerifiedContextFact, ...]:
    return (
        make_fact("fact.verified_requester", "actor:alice"),
        make_fact("fact.registered_action", "action:publish"),
        make_fact("fact.target", "resource:record-1"),
        make_fact("fact.scope", ("tenant:a", "record:1")),
        make_fact("fact.component_authority", "component:publication_gateway"),
        make_fact("fact.profile_applicability", True),
        make_fact("fact.assurance_level", 3),
        make_fact("fact.roles", ("publisher", "reviewer")),
        make_fact("fact.destination", "urn:koa:destination.public"),
    )


def make_context(**overrides: object) -> EvaluationContext:
    required = EvaluationContext.required_fact_names(DecisionClass.AUTHORIZATION)
    values: dict[str, object] = {
        "request_id": "POLREQ-ABCDEF12",
        "correlation_id": "CORR-ABCDEF12",
        "decision_class": DecisionClass.AUTHORIZATION,
        "requester_ref": "actor:alice",
        "action_ref": "action:publish",
        "target_ref": "resource:record-1",
        "scope_refs": ("record:1", "tenant:a"),
        "policy_set_ref": "policy-set:active-v1",
        "authority_version": "1.2.0",
        "requested_at": T0,
        "allowed_fact_names": frozenset(
            set(required) | {"fact.assurance_level", "fact.roles", "fact.destination"}
        ),
        "facts": authorization_facts(),
        "exception_ids": ("EXC-GOV-001",),
        "prior_receipt_refs": ("receipt:prior-1",),
    }
    values.update(overrides)
    return EvaluationContext(**values)  # type: ignore[arg-type]


def make_rule(
    *,
    rule_id: str = "policy-rule.authorization.publish",
    priority: int = 100,
    outcome: RuleOutcome = RuleOutcome.ALLOW,
    when: object | None = None,
) -> PolicyRule:
    expression = when or AllExpression(
        (
            CompareExpression(
                Operand(fact_ref="fact.profile_applicability"),
                CompareOperator.EQ,
                Operand(literal=True),
            ),
            CompareExpression(
                Operand(fact_ref="fact.assurance_level"),
                CompareOperator.GTE,
                Operand(literal=2),
            ),
        )
    )
    review_id = "review.security" if outcome is RuleOutcome.REQUIRE_REVIEW else None
    return PolicyRule(
        rule_id=rule_id,
        version="1.0.0",
        title="Authorize governed publication",
        description="Permits the exact registered action under verified context.",
        priority=priority,
        when=expression,  # type: ignore[arg-type]
        decision=RuleDecision(
            outcome=outcome,
            reason_codes=("policy_rule_matched",),
            obligation_ids=("obligation.retain_receipt",),
            review_requirement_id=review_id,
            decision_validity_seconds=60,
        ),
        enabled=True,
        effective_from=T0 - timedelta(days=1),
        expires_at=T0 + timedelta(days=1),
        evidence_requirement_refs=("EVID-SYS-GOV-001",),
        tags=("authorization", "publication"),
    )


def make_module(
    *,
    module_id: str = "policy-module.authorization",
    order: int = 10,
    dependencies: tuple[str, ...] = (),
    rules: tuple[PolicyRule, ...] | None = None,
) -> PolicyModule:
    return PolicyModule(
        module_id=module_id,
        version="1.0.0",
        title="Authorization module",
        description="Deterministic authorization policy.",
        domain=PolicyDomain.AUTHORIZATION,
        evaluation_order=order,
        dependencies=dependencies,
        exports=("authorization_decision",),
        rules=rules if rules is not None else (make_rule(),),
        required_fact_ids=("fact.assurance_level", "fact.profile_applicability"),
        compatibility_refs=("contracts/components/governance-policy-runtime.component.json",),
    )


def make_bundle(**overrides: object) -> PolicyBundle:
    values: dict[str, object] = {
        "artifact_id": "policy-bundle.sovereign-core",
        "version": "1.0.0",
        "status": PolicyBundleStatus.VALIDATED,
        "issued_at": T0,
        "policy_namespace": "sovereign.core",
        "target_profiles": ("sovereign_hub", "sovereign_linux_node"),
        "minimum_runtime_version": "1.0.0",
        "maximum_runtime_version": "2.0.0",
        "modules": (make_module(),),
        "compatibility_refs": (
            "contracts/components/governance-policy-runtime.component.json",
        ),
        "required_test_refs": ("TEST-SYS-GOV-001",),
        "evidence_refs": ("EVID-SYS-GOV-001",),
        "signature_refs": ("signature:governance-approval-1",),
        "provenance_ref": "provenance:policy-bundle-1",
        "recovery_ref": "recovery:last-known-good-1",
    }
    values.update(overrides)
    return PolicyBundle(**values)  # type: ignore[arg-type]


def test_policy_decision_is_bounded_immutable_and_deterministic() -> None:
    obligation = PolicyObligation(
        obligation_id="obligation.retain_receipt",
        obligation_type=ObligationType.RECEIPT_LINKAGE,
        enforcement_owner="component:publication_gateway",
        description="Link execution evidence to the policy receipt.",
        parameters={"required": True, "classes": ["publication", "audit"]},
        evidence_requirement_refs=("EVID-SYS-GOV-001",),
    )
    decision = PolicyDecision(
        request_id="POLREQ-ABCDEF12",
        correlation_id="CORR-ABCDEF12",
        decision_class=DecisionClass.AUTHORIZATION,
        result=DecisionResult.ALLOW,
        policy_set_ref="policy-set:active-v1",
        authority_version="1.0.0",
        evaluated_at=T0,
        evaluator_identity="component:governance_policy_runtime",
        evaluator_version="1.0.0",
        rule_ids=("policy-rule.z", "policy-rule.a"),
        reason_codes=("policy_rule_matched",),
        obligations=(obligation,),
        verified_context_refs=("evidence:z", "evidence:a"),
    )

    assert decision.permits_execution
    assert decision.rule_ids == ("policy-rule.a", "policy-rule.z")
    assert decision.as_dict()["verified_context_refs"] == ["evidence:a", "evidence:z"]
    assert "credential" not in decision.as_dict()
    with pytest.raises(FrozenInstanceError):
        decision.result = DecisionResult.DENY  # type: ignore[misc]


def test_policy_decision_rejects_ambiguous_or_unjustified_results() -> None:
    base = dict(
        request_id="POLREQ-ABCDEF12",
        correlation_id="CORR-ABCDEF12",
        decision_class=DecisionClass.AUTHORIZATION,
        result=DecisionResult.BLOCKED,
        policy_set_ref="policy-set:active-v1",
        authority_version="1.0.0",
        evaluated_at=T0,
        evaluator_identity="component:governance_policy_runtime",
        evaluator_version="1.0.0",
        rule_ids=("policy-rule.authorization.publish",),
        reason_codes=("required_context_missing",),
    )
    with pytest.raises(DomainValidationError, match="blocked requires"):
        PolicyDecision(**base)

    blocked = PolicyDecision(
        **base,
        diagnostics=(
            DecisionDiagnostic(
                code="required_context_missing",
                severity=DiagnosticSeverity.ERROR,
                message="Required verified context is unavailable.",
            ),
        ),
    )
    assert not blocked.permits_execution

    with pytest.raises(DomainValidationError, match="allow must not"):
        replace(blocked, result=DecisionResult.ALLOW, review_requirement_ids=("review:1",))


def test_evaluation_context_is_minimized_verified_and_deterministic() -> None:
    context = make_context()

    assert context.fact("fact.assurance_level").value == 3
    assert context.verified_context_refs == tuple(
        sorted(f"evidence:{fact.name}" for fact in authorization_facts())
    )
    assert context.as_dict()["scope_refs"] == ["record:1", "tenant:a"]
    assert context.as_dict()["facts"][0]["name"] == "fact.assurance_level"  # type: ignore[index]


def test_evaluation_context_rejects_missing_undeclared_duplicate_and_stale_facts() -> None:
    facts = authorization_facts()
    with pytest.raises(DomainValidationError, match="missing required"):
        make_context(facts=tuple(fact for fact in facts if fact.name != "fact.verified_requester"))
    with pytest.raises(DomainValidationError, match="undeclared"):
        make_context(
            allowed_fact_names=EvaluationContext.required_fact_names(
                DecisionClass.AUTHORIZATION
            ),
            facts=facts,
        )
    with pytest.raises(DomainValidationError, match="duplicate"):
        make_context(facts=facts + (facts[0],))
    stale = replace(facts[0], valid_until=T0 - timedelta(seconds=1))
    with pytest.raises(DomainValidationError, match="stale"):
        make_context(facts=(stale,) + facts[1:])
    with pytest.raises(MissingContextFact):
        make_context().fact("fact.not_declared")


def test_expression_language_is_deterministic_and_side_effect_free() -> None:
    context = make_context()
    expression = AllExpression(
        (
            ExistsExpression("fact.verified_requester"),
            CompareExpression(
                Operand(fact_ref="fact.assurance_level"),
                CompareOperator.GTE,
                Operand(literal=3),
            ),
            ContainsExpression(
                Operand(fact_ref="fact.roles"),
                Operand(literal="publisher"),
            ),
            MatchesExpression(
                Operand(fact_ref="fact.destination"),
                r"^urn:koa:destination\.",
            ),
            NotExpression(
                CompareExpression(
                    Operand(fact_ref="fact.profile_applicability"),
                    CompareOperator.EQ,
                    Operand(literal=False),
                )
            ),
            AnyExpression(
                (
                    CompareExpression(
                        Operand(fact_ref="fact.assurance_level"),
                        CompareOperator.EQ,
                        Operand(literal=3),
                    ),
                    CompareExpression(
                        Operand(fact_ref="fact.assurance_level"),
                        CompareOperator.GT,
                        Operand(literal=3),
                    ),
                )
            ),
        )
    )

    assert expression.evaluate(context)
    assert expression.as_dict()["all"]
    assert not ExistsExpression("fact.missing_fact").evaluate(context)
    with pytest.raises(DomainValidationError, match="exactly one"):
        Operand(fact_ref="fact.scope", literal="bad")


def test_policy_rule_requires_registered_review_and_explicit_validity() -> None:
    context = make_context()
    rule = make_rule(outcome=RuleOutcome.REQUIRE_REVIEW)

    assert rule.matches(context)
    assert rule.decision.outcome.runtime_result is DecisionResult.BLOCKED
    assert rule.decision.review_requirement_id == "review.security"
    assert not replace(rule, enabled=False).matches(context)
    assert not rule.matches(context, at=T0 + timedelta(days=2))

    with pytest.raises(DomainValidationError, match="requires review_requirement_id"):
        RuleDecision(
            outcome=RuleOutcome.REQUIRE_REVIEW,
            reason_codes=("review_required",),
        )
    with pytest.raises(DomainValidationError, match="non-negative"):
        replace(rule, priority=-1)


def test_policy_module_has_closed_mode_and_non_ambiguous_precedence() -> None:
    first = make_rule(rule_id="policy-rule.authorization.first", priority=200)
    second = make_rule(rule_id="policy-rule.authorization.second", priority=100)
    module = make_module(rules=(second, first))

    assert [rule.rule_id for rule in module.rules] == [
        "policy-rule.authorization.first",
        "policy-rule.authorization.second",
    ]
    assert module.as_dict()["rules"]

    with pytest.raises(DomainValidationError, match="unique priorities"):
        make_module(rules=(first, replace(second, priority=200)))
    with pytest.raises(DomainValidationError, match="either inline"):
        replace(module, module_artifact_ref="artifact:module", entrypoint="evaluate")
    external = PolicyModule(
        module_id="policy-module.external",
        version="1.0.0",
        title="Compiled module",
        description="Deterministic compiled module.",
        domain=PolicyDomain.AUTHORIZATION,
        evaluation_order=20,
        module_artifact_ref="artifact:compiled-policy",
        entrypoint="evaluate",
    )
    assert external.as_dict()["entrypoint"] == "evaluate"


def test_policy_bundle_resolves_dependencies_and_runtime_range() -> None:
    base = make_module(module_id="policy-module.base", order=10)
    dependent = make_module(
        module_id="policy-module.dependent",
        order=20,
        dependencies=(base.module_id,),
        rules=(make_rule(rule_id="policy-rule.authorization.dependent", priority=50),),
    )
    bundle = make_bundle(modules=(dependent, base))

    assert [module.module_id for module in bundle.modules] == [
        "policy-module.base",
        "policy-module.dependent",
    ]
    assert bundle.supports_runtime("1.5.0")
    assert not bundle.supports_runtime("2.1.0")
    assert bundle.as_dict()["partial_activation_permitted"] is False


def test_policy_bundle_fails_closed_on_dependencies_signatures_and_partial_state() -> None:
    unresolved = make_module(dependencies=("policy-module.missing",))
    with pytest.raises(DomainValidationError, match="unresolved dependencies"):
        make_bundle(modules=(unresolved,))
    with pytest.raises(DomainValidationError, match="requires signatures"):
        make_bundle(signature_refs=())
    with pytest.raises(DomainValidationError, match="partial policy activation"):
        make_bundle(partial_activation_permitted=True)
    with pytest.raises(DomainValidationError, match="must not exceed"):
        make_bundle(minimum_runtime_version="3.0.0", maximum_runtime_version="2.0.0")


def test_policy_set_uses_only_canonical_atomic_transitions() -> None:
    candidate = make_bundle(status=PolicyBundleStatus.CANDIDATE, signature_refs=())
    policy_set = PolicySet(
        policy_set_ref="policy-set:candidate-v1",
        bundles=(candidate,),
        state=PolicySetState.STAGED,
    )

    validating = policy_set.transition(
        PolicySetState.VALIDATING,
        trigger="begin_policy_validation",
    )
    assert validating.state is PolicySetState.VALIDATING
    assert PolicySet.transition_identity(
        PolicySetState.STAGED,
        PolicySetState.VALIDATING,
    ) == "TRANSITION-GOV-POL-002"
    with pytest.raises(DomainValidationError, match="requires trigger"):
        policy_set.transition(PolicySetState.VALIDATING, trigger="file_order")
    with pytest.raises(DomainValidationError, match="not canonical"):
        policy_set.transition(PolicySetState.ACTIVE, trigger="skip_validation")

    active_bundle = make_bundle(status=PolicyBundleStatus.ACTIVE)
    validated = PolicySet(
        policy_set_ref="policy-set:validated-v1",
        bundles=(make_bundle(status=PolicyBundleStatus.VALIDATED),),
        state=PolicySetState.VALIDATED,
    )
    activated = validated.transition(
        PolicySetState.ACTIVE,
        trigger="atomic_activation_authorized",
        bundles=(active_bundle,),
        previous_valid_policy_set_ref="policy-set:previous-v1",
    )
    assert activated.state is PolicySetState.ACTIVE

    active = PolicySet(
        policy_set_ref="policy-set:active-v1",
        bundles=(active_bundle,),
        state=PolicySetState.ACTIVE,
        previous_valid_policy_set_ref="policy-set:previous-v1",
    )
    assert active.state is PolicySetState.ACTIVE
    with pytest.raises(DomainValidationError, match="previous valid"):
        replace(active, previous_valid_policy_set_ref=None)
