# Component — `koa-session-shell`

## 1. Purpose

`koa-session-shell` is the minimal native product shell for a kOA endpoint. It owns session lifecycle and workspace composition; it is not Konnaxion itself and it does not implement Orgo business logic.

## 2. Responsibilities

The shell MUST provide:

- user authentication handoff and session lock;
- tenant and workspace selection;
- principal entry points to Konnaxion and Orgo;
- global notifications and search entry points;
- local, offline, synchronization, and trust status;
- safe import/export entry points;
- accessibility and localization integration;
- recovery and support entry points when policy permits;
- an explicit indication when the node is degraded, stale, or running a fallback release.

## 3. Non-responsibilities

The shell MUST NOT:

- execute arbitrary system commands;
- own product domain data;
- interpret Kristal semantics independently;
- store signing keys;
- silently switch tenants;
- make governance decisions;
- hide verification or synchronization failures.

## 4. Process model

The shell SHOULD run as an unprivileged system or user service under a dedicated identity. It communicates through authenticated local APIs:

```text
koa-session-shell
├── Konnaxion local gateway
├── Orgo local gateway
├── Kristal query/status API
├── policy decision API
└── node status/operation API
```

The shell receives no direct write access to `/var/lib/koa` product stores.

## 5. Workspace model

```text
Home
├── Konnaxion
├── Orgo
├── Kristal Library
├── Global Search
├── Notifications
├── Sync and Node Status
└── Session and Accessibility
```

Deployments MAY visually emphasize one workspace, but both principal planes remain addressable when installed and authorized.

## 6. Failure behavior

- Konnaxion unavailable: Orgo, Kristal Library, and node status remain available when healthy.
- Orgo unavailable: Konnaxion and approved public knowledge remain available.
- network unavailable: local capability envelope remains accessible.
- policy runtime unavailable: read-only safe surfaces MAY remain, but sensitive operations are denied.
- active Runtime Pack invalid: affected knowledge views are blocked or labeled according to capability policy.

## 7. Security requirements

The shell MUST use origin and navigation restrictions for embedded web content. External links MUST open through an explicit policy-controlled handoff. File pickers MUST stage imported content into quarantine rather than exposing arbitrary host paths.

## 8. Conformance evidence

A shell implementation MUST demonstrate:

- no root or unrestricted D-Bus dependency;
- correct tenant separation;
- visible degraded-state indicators;
- functional offline session startup;
- workspace isolation after one workspace crashes;
- keyboard, screen-reader, and locale support for declared profiles.
