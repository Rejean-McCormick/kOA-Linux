from koa_spaces_adapter.shell_state import ShellStateReader
class C:
    def read_shell_state(self): return {"state":"offline","active_space_id":"default_space","active_module_id":"space_home","active_route_id":"space_home.home","network_state":"offline","reason":None}
def test_shell_state_projection():
    state=ShellStateReader(C()).read(); assert state.state=="offline"; assert state.network_state=="offline"
