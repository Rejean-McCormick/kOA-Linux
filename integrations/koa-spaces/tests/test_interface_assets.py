from koa_spaces_adapter.interface_assets import validate_asset_manifest, AssetManifestValidationError

def test_remote_runtime_dependency_is_rejected():
    doc={"bundle_id":"test.bundle","version":"1.0.0","owner_kind":"koa_spaces_shell","owner_id":"koa_spaces","entrypoints":["index.js"],"assets":[{"path":"index.js","media_type":"text/javascript","sha256":"0"*64,"offline_required":True}],"remote_runtime_dependencies":["https://cdn.example/x.js"],"offline_policy":{"local_assets_complete":True,"public_cdn_required":False,"remote_fonts_required":False,"internet_required_for_shell":False},"authority_boundary":{"presentation_assets_only":True,"contains_business_authority":False,"contains_credentials":False}}
    try: validate_asset_manifest(doc)
    except AssetManifestValidationError: return
    raise AssertionError("remote dependency accepted")
