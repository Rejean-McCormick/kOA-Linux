# Boot, Session, and Recovery

## 1. Boot sequence

```text
Firmware / Secure Boot
        ↓
Signed bootloader and kernel
        ↓
Immutable OS image
        ↓
Storage unlock and integrity checks
        ↓
koa-node.target
        ↓
policy runtime, audit broker, node agent
        ↓
koa-services.target
        ↓
Konnaxion, Orgo, Kristal Runtime
        ↓
koa-graphical.target
        ↓
koa-session-shell
```

A failed optional application service MUST NOT prevent recovery access. A failed trust or policy foundation MUST prevent sensitive activation and expose an actionable diagnostic state.

## 2. Session startup

The shell authenticates the user, resolves tenant and role context, displays node and synchronization status, and offers Konnaxion and Orgo as principal workspaces. It MUST NOT grant direct shell or root access as part of ordinary use.

## 3. Watchdog and health

Critical node services SHOULD use systemd watchdogs or equivalent supervision. Readiness MUST distinguish process existence from ability to satisfy the service's critical contract.

## 4. Recovery entry

Recovery MAY be entered through:

- automatic boot fallback after repeated failure;
- signed operator request;
- physical recovery gesture;
- verified removable media;
- remote management only under a declared high-assurance policy.

## 5. Recovery capabilities

Recovery SHOULD provide:

- booted image and Release Set inspection;
- previous image rollback;
- policy and Runtime Pack rollback;
- storage and filesystem diagnostics;
- trusted time and trust-root repair;
- encrypted backup restore;
- Sovereignty Bundle import;
- audit export;
- factory reset with explicit data handling.

Recovery MUST NOT silently erase tenant data or replace trust roots.

## 6. Break-glass operations

Break-glass operations MUST:

- be narrowly defined;
- require stronger authentication than ordinary administration;
- state duration and scope;
- emit a tamper-evident receipt;
- trigger review;
- expire automatically where possible.

## 7. Boot success criteria

A new OS image is considered successful only after required node, policy, storage, Kristal, and session checks pass within a bounded interval. Otherwise the system SHOULD return to the last-known-good image.
