from __future__ import annotations
from pathlib import Path
import ast, json, sys, tomllib, subprocess

root=Path(sys.argv[1]).resolve()
docs=Path(sys.argv[2]).resolve()
base=root/'components/kristal-runtime'
allowed={
'components/kristal-runtime/README.md',
'components/kristal-runtime/component.toml',
'components/kristal-runtime/pyproject.toml',
'components/kristal-runtime/src/koa_kristal_runtime/__init__.py',
'components/kristal-runtime/src/koa_kristal_runtime/__main__.py',
'components/kristal-runtime/src/koa_kristal_runtime/bootstrap.py',
'components/kristal-runtime/src/koa_kristal_runtime/config.py',
'components/kristal-runtime/src/koa_kristal_runtime/health.py',
'components/kristal-runtime/src/koa_kristal_runtime/receipts.py',
}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}
assert actual==allowed, f'allowlist mismatch missing={sorted(allowed-actual)} extra={sorted(actual-allowed)}'
for rel in sorted(allowed):
    p=root/rel
    assert p.stat().st_size>0, f'empty file {rel}'
    assert '\r' not in p.read_text(encoding='utf-8'), f'CRLF in {rel}'

component=tomllib.loads((base/'component.toml').read_text())
project=tomllib.loads((base/'pyproject.toml').read_text())
contract=json.loads((docs/'docs/contracts/components/kristal-runtime.component.json').read_text())
json.loads((docs/'docs/contracts/artifact-contracts/kristal-artifact.schema.json').read_text())
json.loads((docs/'docs/contracts/artifact-contracts/runtime-pack.schema.json').read_text())
assert component['component']['id']==contract['component_id']=='kristal_runtime'
assert component['component']['contract_version']==contract['version']=='1.0.0'
assert component['component']['component_kind']==contract['classification']['component_kind']
assert component['component']['system_role']==contract['classification']['system_role']
assert [x['id'] for x in component['interfaces']['provided']]==[x['interface_id'] for x in contract['interfaces']]
assert [x['id'] for x in component['dependencies']['consumed']]==[x['dependency_id'] for x in contract['dependencies']]
assert component['health']['exposed_states']==contract['observability']['exposed_states']
assert sorted(component['receipts']['critical_types'])==sorted(contract['observability']['critical_receipts'])
assert component['artifacts']['release_channel']=='knowledge'
assert project['project']['name']=='koa-kristal-runtime'
assert project['project']['version']=='0.1.0'
assert project['project']['dependencies']==[]

for p in sorted((base/'src').rglob('*.py')):
    tree=ast.parse(p.read_text(), filename=str(p))
    for node in ast.walk(tree):
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            assert not (len(node.body)==1 and isinstance(node.body[0],(ast.Pass,ast.Expr)) and (isinstance(node.body[0],ast.Pass) or (isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and node.body[0].value.value is Ellipsis))), f'empty body in {p}:{node.lineno}'
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            names=[]
            if isinstance(node,ast.Import): names=[a.name for a in node.names]
            elif node.module: names=[node.module]
            for name in names:
                assert not name.startswith(('koa_audit_broker','koa_governance_policy_runtime','koa_identity_and_trust','koa_resource_governor','koa_node_agent')), f'private/cross component import {name}'

readme=(base/'README.md').read_text()
for phrase in ('atomic','knowledge','known-good','does not'):
    assert phrase.lower() in readme.lower()
print(json.dumps({'status':'pass','files':len(actual),'interfaces':len(contract['interfaces']),'dependencies':len(contract['dependencies']),'states':len(contract['observability']['exposed_states']),'receipts':len(contract['observability']['critical_receipts'])},sort_keys=True))
