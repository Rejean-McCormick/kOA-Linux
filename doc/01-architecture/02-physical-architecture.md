# Physical Architecture

## 1. Appliance layers

```text
┌──────────────────────────────────────────────────────────────┐
│                    User Experience                           │
│ koa-session-shell • Konnaxion • Orgo • Kristal Library      │
├──────────────────────────────────────────────────────────────┤
│                    Application Services                      │
│ Konnaxion Core • Orgo Core • Kristal Runtime • adapters     │
├──────────────────────────────────────────────────────────────┤
│                    Governance Services                       │
│ policy runtime • audit broker • publication gateway         │
├──────────────────────────────────────────────────────────────┤
│                    Node Services                             │
│ node agent • release manager • sync • export • recovery     │
├──────────────────────────────────────────────────────────────┤
│                    Container Boundary                        │
│ rootless Podman • Quadlet • namespaces • cgroups • seccomp  │
├──────────────────────────────────────────────────────────────┤
│                    Immutable Linux                           │
│ kernel • systemd • LSM • storage • networking • Wayland     │
├──────────────────────────────────────────────────────────────┤
│                    Hardware / Firmware                       │
└──────────────────────────────────────────────────────────────┘
```

## 2. Host operating system

The host SHOULD contain only components required to:

- boot and verify the image;
- unlock and mount approved storage;
- establish networking and local time;
- start node and governance services;
- launch the minimal graphical session;
- operate containers;
- perform update, rollback, export, and recovery.

Development tools, compilers, arbitrary package managers, and user-installed system daemons SHOULD be excluded from production endpoint images.

## 3. Container placement

Application services SHOULD run as rootless containers under dedicated system identities. The host MUST reserve privileged services for operations that cannot be safely delegated, such as measured identity, device management, encrypted-volume lifecycle, signed activation, and controlled recovery.

## 4. Data placement

- immutable binaries: image-managed `/usr` or equivalent;
- host policy and declared configuration: `/etc/koa`;
- durable service state: `/var/lib/koa/<domain>`;
- runtime state: `/run/koa`;
- signed installed artifacts: `/var/lib/koa/artifacts`;
- audit receipts: `/var/lib/koa/audit` with class-specific protection;
- removable/offline import staging: quarantined path not directly executable.

## 5. Graphical stack

The endpoint SHOULD use a maintained minimal Wayland compositor and a tested embedded web engine or browser runtime. GNOME is not part of the product shell. Standard Linux services may still be used when they provide maintained device, accessibility, media, or network functionality.

## 6. Hardware assurance profiles

### Baseline

- UEFI Secure Boot when supported;
- encrypted durable storage;
- signed OS and artifacts;
- recovery key procedure;
- no assumption of TPM availability.

### Enhanced

- TPM-backed node keys;
- measured boot evidence;
- sealed storage keys;
- remote or local attestation;
- tamper-evident audit anchoring.

### High assurance

- split key custody;
- hardware security module or threshold signing;
- dual-control recovery;
- physically protected build/signing nodes;
- controlled media transfer.

A node profile MUST declare which assurance level it implements.
