# Profile implementation settings

This directory contains implementation selectors for the ten canonical kOA profiles. The files are inputs to the future assembly engine; they are not canonical profile definitions.

## Authority

Each TOML file points to exactly one profile contract under `docs/contracts/profiles/`. Component membership, capabilities, authority, security, resource rules, lifecycle behavior, offline behavior, integration admission, inheritance, and overlay compatibility remain owned by that contract.

These files may select an implementation already admitted by the owning contract. They must not:

- copy or fork component source trees;
- redefine component or capability membership;
- weaken a global, profile, security, lifecycle, or data-ownership rule;
- activate an overlay implicitly;
- infer inheritance from deployment prevalence;
- add an external integration, privilege, fallback, or substitution;
- treat generated profile plans as normative authority.

## Strict loading contract

A loader must reject:

- an unknown top-level table or key;
- a missing profile contract;
- a profile identifier or version mismatch;
- a setting not permitted by the referenced contract;
- an unresolved composition conflict;
- an overlay without an explicitly selected compatible primary profile;
- a profile-specific implementation source tree.

The `authority` table deliberately points all semantic membership and policy decisions back to the canonical contract. The `source_layout` table fixes a shared repository source tree and a deterministic generated-output root.

## Composition

The presence of a settings file only makes that profile available for explicit selection; it never activates the profile. Primary profiles are independently selected. Overlays are explicitly selected and resolved using the compatibility and ordering rules in their contracts. No overlay may broaden authority, data ownership, external integrations, or privilege. Unresolved conflicts fail closed.

## Files

| File | Canonical profile |
| --- | --- |
| `user-lightweight.toml` | `user_lightweight` |
| `developer-linux-workstation.toml` | `developer_linux_workstation` |
| `developer-windows-wsl.toml` | `developer_windows_wsl` |
| `sovereign-linux-node.toml` | `sovereign_linux_node` |
| `sovereign-hub.toml` | `sovereign_hub` |
| `build-farm.toml` | `build_farm` |
| `control-plane.toml` | `control_plane` |
| `high-assurance.toml` | `high_assurance` overlay |
| `sovereign-offline.toml` | `sovereign_offline` overlay |
| `appliance-shell.toml` | `appliance_shell` overlay |

## Validation

At minimum, parse every TOML file, verify its profile identifier and version against its contract, reject unknown keys, verify that every implementation value is admitted by the contract, and run the repository architecture, profile-inheritance, profile-composition, generated-content, and documentation validators.
