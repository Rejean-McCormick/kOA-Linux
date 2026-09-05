from koa_spaces_adapter.unix_transport import UnixHttpTransport, _OPERATION_MAP


def test_transport_uses_canonical_socket_by_default():
    assert UnixHttpTransport().socket_path == "/run/koa/sockets/koa-spaces.sock"


def test_capability_projection_update_uses_explicit_control_route():
    assert _OPERATION_MAP["capabilities.update"] == ("POST", "/capabilities/update")
