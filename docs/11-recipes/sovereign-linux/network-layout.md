<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "RECIPE-SOVEREIGN-LINUX-NETWORK-LAYOUT",
  "document_class": "recipe",
  "status": "active",
  "authority_participation": "non_authoritative",
  "language": "en",
  "layer": "implementation",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/document-index.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-002",
    "DOC-GOV-009"
  ],
  "tags": [
    "implementation",
    "recipe",
    "network",
    "layout"
  ],
  "edit_policy": "manual"
}
KOA:DOC-META:END -->

# Network Layout

> **Recipe status:** Active, non-authoritative implementation guidance.
> **Canonical boundary:** This recipe does not define profile membership, network authority, component interfaces, tenant boundaries, trust, consent, publication authority, firewall policy, or service ownership. Resolve those facts from the active `sovereign_linux_node` profile, component contracts, integration contracts, network-boundary policy, Release Set, and deployment records before applying any command.

## 1. Purpose

This recipe provides a cautious reference procedure for implementing a sovereign Linux node network layout with:

- explicit logical zones;
- default-deny ingress and forwarding;
- bounded egress;
- service binding to the intended address or local socket;
- separate administration, backup, federation, and external-integration paths;
- local operation without Internet or public DNS;
- protected rollback access;
- testable failure containment;
- no assumption that network location establishes trust.

The recipe uses Linux routing, optional VLANs or bridges, `systemd-networkd` examples, and a dedicated `nftables` table. Equivalent implementations can use NetworkManager, another Linux network manager, a hardware firewall, or another profile-approved mechanism when they preserve the same active contracts.

The procedure does not require containers, Kubernetes, a service mesh, external AI, a remote control plane, or unrestricted Internet access.

## 2. Intended Result

The completed layout has these properties:

1. Every active interface and address has one recorded purpose.
2. Every exposed service binds only to an approved address, socket, or interface.
3. The node accepts no undeclared inbound route.
4. Forwarding is disabled unless the node has an explicitly approved routing role.
5. Egress is limited to declared local infrastructure, update, backup, federation, or external-integration destinations.
6. Public, private, governance, administration, federation, backup, quarantine, and external-integration traffic remain logically distinguishable when those zones are active.
7. Component databases, queues, object stores, and local administrative sockets remain unexposed.
8. Publication Gateway, UCKK Publication Bridge, and UCKK Import Bridge use separate application contracts even when they share a physical interface.
9. Internet loss does not break minimum local operation.
10. A failed candidate firewall or network configuration can be rolled back through local console access.

## 3. Safety Boundaries

Apply these boundaries throughout the procedure:

1. Use direct console, out-of-band console, or a separately verified local recovery path before changing remote administration networking.
2. Do not apply this recipe from an SSH session unless an automatic rollback has been armed and tested.
3. Do not use `nft flush ruleset`; manage only the dedicated kOA table created by this recipe.
4. Do not rename or readdress the only recovery interface without a tested alternate path.
5. Do not assign one address to several authority purposes merely to simplify firewall rules.
6. Do not infer trust from loopback, a private address, a VLAN, a bridge, a container network, or the same host.
7. Do not expose component databases, queues, object stores, metrics endpoints, debug ports, or privileged local interfaces publicly.
8. Do not permit unrestricted outbound HTTPS as a substitute for destination-specific egress.
9. Do not configure a federation peer, backup target, time source, DNS server, package mirror, or external provider by name alone; bind it to the active integration and trust records.
10. Do not enable IP forwarding unless the node contract assigns a routing function.
11. Do not copy sample addresses unchanged into a production deployment.
12. Keep the last validated configuration and a local rollback command outside the files being replaced.
13. Treat incomplete ownership, addressing, trust, or route information as a blocked deployment state.
14. Preserve unrelated host firewall tables and rules.
15. Keep the network layout usable when public DNS, Internet access, federation, or an external provider is unavailable.

## 4. Preconditions

Confirm these conditions before configuration:

- the deployment is assigned to the active `sovereign_linux_node` profile;
- the profile contract is materialized and validated;
- selected overlays are explicit;
- the active Release Set is known;
- required and optional components are known;
- active integrations are known;
- every service has an owner and declared interface;
- every physical interface is inventoried;
- the address plan is approved;
- the administration source network is known;
- backup, federation, update, DNS, and time destinations are known;
- local console access works;
- another operator or recovery procedure can restore networking;
- the existing firewall is backed up;
- service owners can verify their bindings;
- component-owned data remains reachable through declared interfaces after segmentation.

When any prerequisite is unavailable, collect the missing canonical information before applying the layout.

## 5. Choose the Active Zones

Use only zones required by the active profile composition.

| Zone | Typical purpose | Typical exposure | Default direction |
| --- | --- | --- | --- |
| `public` | Approved public Konnaxion endpoints or another explicitly public service. | Internet, guest network, or public LAN according to deployment authority. | Inbound only to declared public ports; bounded outbound replies. |
| `private` | Orgo, protected user workflows, tenant services, and internal application interfaces. | Authenticated private LAN or local service network. | Inbound only from declared private clients and components. |
| `governance` | Identity, trust, policy, audit, consent, and publication-decision interfaces. | Local host or protected service network. | Narrow component-to-governance calls. |
| `administration` | Operator access, maintenance, health, recovery, and bounded host operations. | Dedicated management network, local console, or approved access broker. | Inbound only from declared administrator sources. |
| `federation` | Explicit peer synchronization and artifact exchange. | Named and trusted peers only. | Bidirectional only for declared peer protocols. |
| `backup` | Backup transfer, verification, and restore coordination. | Dedicated target network or named backup endpoint. | Outbound by default; inbound only when the backup contract requires it. |
| `quarantine` | Inspection of imports or untrusted candidate artifacts. | Isolated local namespace, bridge, or service network. | No direct path to authoritative stores. |
| `external_integration` | Approved provider calls, package mirrors, or external adapters. | Destination-specific egress. | Outbound only unless the integration contract declares a callback. |

A single physical interface can carry several logical zones through VLANs or address and policy separation. The active deployment record must explain how equivalent isolation, identity, observability, and failure containment are achieved.

## 6. Select a Physical Pattern

Choose one pattern and record it.

### 6.1 Pattern A — Dedicated interfaces

Use separate physical interfaces when available.

| Interface role | Example variable | Typical zone |
| --- | --- | --- |
| Public or service-facing | `IF_PUBLIC` | `public` |
| Protected LAN | `IF_PRIVATE` | `private` |
| Management | `IF_ADMIN` | `administration` |
| Backup | `IF_BACKUP` | `backup` |
| Federation | `IF_FEDERATION` | `federation` |

This pattern provides clear failure and cable-level separation but increases hardware and switch configuration requirements.

### 6.2 Pattern B — VLAN trunk plus recovery interface

Use one tagged trunk for logical zones and one untagged or dedicated recovery interface.

Example logical interfaces:

`text
eno1.110 public
eno1.120 private
eno1.130 administration
eno1.140 federation
eno1.150 backup
eno2 local recovery
`

This pattern requires switch, VLAN, and recovery-path validation.

### 6.3 Pattern C — Single interface with address and policy separation

Use one interface only when the profile and threat model accept logical separation on one link.

This pattern requires:

- separate service bindings;
- separate addresses where practical;
- strict firewall sets;
- no assumption that one subnet is trusted;
- stronger application identity checks;
- explicit documentation of reduced physical containment.

### 6.4 Pattern D — Offline isolated node

Use a protected LAN and local administration or console path. Omit public, federation, and external-integration zones unless explicitly activated.

An air-gapped cable state does not replace firewall, service binding, local identity, or recovery validation.

## 7. Record Deployment Inputs

Create a protected local working directory and record operator-supplied values.

`bash
export NETWORK_CHANGE_ID='network-change-id-from-local-change-record'
export WORK_DIR="/var/lib/koa/network-changes/$NETWORK_CHANGE_ID"
export APPLY_CHANGES='0' # 0 = inspect and generate only; 1 = apply after review

sudo install -d -m 0700 -o root -g root -- "$WORK_DIR"
sudo sh -c "printf '%s\n' '$NETWORK_CHANGE_ID' > '$WORK_DIR/change_id.txt'"
date -u +'%Y-%m-%dT%H:%M:%SZ' \
 | sudo tee "$WORK_DIR/started_at.txt" >/dev/null
`

Set values from the approved deployment record. The following values are examples only:

`bash
export IF_PUBLIC='eno1.110'
export IF_PRIVATE='eno1.120'
export IF_ADMIN='eno1.130'
export IF_FEDERATION='eno1.140'
export IF_BACKUP='eno1.150'
export IF_RECOVERY='eno2'

export ADDR_PUBLIC='192.0.2.10/24'
export ADDR_PRIVATE='10.77.20.10/24'
export ADDR_ADMIN='10.77.30.10/24'
export ADDR_FEDERATION='10.77.40.10/24'
export ADDR_BACKUP='10.77.50.10/24'
export ADDR_RECOVERY='169.254.77.1/30'

export NET_PRIVATE='10.77.20.0/24'
export NET_ADMIN='10.77.30.0/24'
export NET_FEDERATION='10.77.40.0/24'
export NET_BACKUP='10.77.50.0/24'

export LOCAL_DNS_IP='10.77.20.53'
export LOCAL_TIME_IP='10.77.20.123'
export LOCAL_UPDATE_MIRROR_IP='10.77.20.80'
export BACKUP_TARGET_IP='10.77.50.20'
export FEDERATION_PEER_IP='10.77.40.20'
`

`192.0.2.0/24` is used above as documentation space. Replace every sample value with the approved deployment address.

Record the values without secret material:

`bash
env \
 | grep -E '^(NETWORK_CHANGE_ID|IF_|ADDR_|NET_|LOCAL_|BACKUP_TARGET_IP|FEDERATION_PEER_IP)=' \
 | sort \
 | sudo tee "$WORK_DIR/operator_inputs.txt" >/dev/null
`

## 8. Inventory the Existing Node

### 8.1 Interfaces, addresses, and routes

`bash
ip -brief link \
 | sudo tee "$WORK_DIR/ip_link_before.txt" >/dev/null

ip -brief address \
 | sudo tee "$WORK_DIR/ip_address_before.txt" >/dev/null

ip route show table all \
 | sudo tee "$WORK_DIR/ip_route_before.txt" >/dev/null

ip -6 route show table all \
 | sudo tee "$WORK_DIR/ip6_route_before.txt" >/dev/null

networkctl list 2>/dev/null \
 | sudo tee "$WORK_DIR/networkctl_before.txt" >/dev/null || true
`

### 8.2 Listening services

`bash
ss -lntup \
 | sudo tee "$WORK_DIR/listening_sockets_before.txt" >/dev/null

systemctl --type=service --state=running --no-pager \
 | sudo tee "$WORK_DIR/running_services_before.txt" >/dev/null
`

Review every wildcard binding such as `0.0.0.0`, `[::]`, or an address assigned to the wrong zone.

### 8.3 Existing firewall

`bash
sudo nft list ruleset \
 | sudo tee "$WORK_DIR/nft_ruleset_before.nft" >/dev/null

sudo nft list tables \
 | sudo tee "$WORK_DIR/nft_tables_before.txt" >/dev/null
`

Do not overwrite a distribution, hypervisor, container, VPN, or security-tool table.

### 8.4 Kernel forwarding and reverse-path settings

`bash
sysctl net.ipv4.ip_forward \
 | sudo tee "$WORK_DIR/ip_forward_before.txt" >/dev/null

sysctl net.ipv6.conf.all.forwarding \
 | sudo tee "$WORK_DIR/ip6_forward_before.txt" >/dev/null

sysctl net.ipv4.conf.all.rp_filter \
 | sudo tee "$WORK_DIR/rp_filter_before.txt" >/dev/null
`

### 8.5 Container and namespace networking

When applicable:

`bash
podman network ls \
 | sudo tee "$WORK_DIR/podman_networks_before.txt" >/dev/null 2>&1 || true

ip netns list \
 | sudo tee "$WORK_DIR/network_namespaces_before.txt" >/dev/null
`

A container network does not define component authority. Record the component and workspace owner of every writable network namespace.

## 9. Build the Service Exposure Matrix

Create a deployment-specific matrix before writing firewall rules.

| Service | Owning component | Zone | Bind address or socket | Source scope | Port or protocol | External dependency | Failure behavior |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Public web | Konnaxion or declared public component | `public` | Public address | Approved audience | `tcp/443` and optional `tcp/80` redirect | None for local service | Keep private services unavailable publicly. |
| Private workflow | Orgo or declared private component | `private` | Private address or local proxy | Private clients | Contract-defined | None for minimum local operation | Preserve local private operation. |
| Governance API | Governance owner | `governance` | Loopback, Unix socket, or protected address | Declared components | Contract-defined | None for local decisions | Block new governed operations when unavailable. |
| Administration | Node Agent, SSH, or approved broker | `administration` | Admin or recovery address | Named admin sources | Contract-defined | None | Preserve console recovery. |
| Federation | Federation adapter | `federation` | Federation address | Named peer | Contract-defined | Peer only | Queue eligible work without automatic release. |
| Backup | Backup component | `backup` | Backup address | Named target or source | Contract-defined | Backup target | Preserve local data and retry according to contract. |
| Metrics | Owning component or local collector | Local or admin only | Loopback, Unix socket, or admin address | Local collector | Contract-defined | None | Continue local buffering where approved. |
| Database | Owning component | Local or protected service network | Unix socket, loopback, or component-only address | Owning component | Engine-specific | None | Never expose publicly. |

Do not proceed until every active listener has a row or a documented reason for local-only operation.

## 10. Create the Address and Route Plan

Record:

- interface name;
- media or VLAN;
- address;
- prefix;
- gateway;
- route metric;
- DNS source;
- time source;
- service owners;
- failure behavior.

Use no default gateway on zones that do not require one.

Prefer:

- one default route through the approved egress zone;
- explicit host or subnet routes for backup and federation;
- no route between public and private zones unless a declared gateway service mediates the application flow;
- no route from quarantine to authoritative storage;
- no direct public route to governance or administration.

Example route intent:

| Source zone | Destination | Route intent |
| --- | --- | --- |
| `private` | local governance services | Local protected route only. |
| `public` | private database | No route and no firewall permission. |
| `administration` | node administration endpoint | Allowed from named administrator sources. |
| `federation` | named peer | Host or peer-subnet route only. |
| `backup` | named backup target | Host or backup-subnet route only. |
| `quarantine` | validation service | Local bounded route; no authoritative-store path. |
| local components | public DNS | Not required for minimum local operation. |

## 11. Optional VLAN Configuration with systemd-networkd

This section demonstrates one implementation. Skip it when the active network manager uses another format.

### 11.1 VLAN devices

Create one `.netdev` file per selected VLAN.

`ini
# /etc/systemd/network/20-koa-public.netdev
[NetDev]
Name=eno1.110
Kind=vlan

[VLAN]
Id=110
`

`ini
# /etc/systemd/network/20-koa-private.netdev
[NetDev]
Name=eno1.120
Kind=vlan

[VLAN]
Id=120
`

`ini
# /etc/systemd/network/20-koa-admin.netdev
[NetDev]
Name=eno1.130
Kind=vlan

[VLAN]
Id=130
`

Add federation and backup VLAN files only when those zones are active.

### 11.2 Trunk interface

`ini
# /etc/systemd/network/20-koa-trunk.network
[Match]
Name=eno1

[Network]
VLAN=eno1.110
VLAN=eno1.120
VLAN=eno1.130
VLAN=eno1.140
VLAN=eno1.150
LinkLocalAddressing=no
IPv6AcceptRA=no
DHCP=no
`

Remove inactive VLAN entries instead of leaving unused interfaces configured.

### 11.3 Zone addresses

`ini
# /etc/systemd/network/30-koa-private.network
[Match]
Name=eno1.120

[Network]
Address=10.77.20.10/24
DNS=10.77.20.53
Domains=~koa.local
IPv6AcceptRA=no
DHCP=no
`

`ini
# /etc/systemd/network/30-koa-admin.network
[Match]
Name=eno1.130

[Network]
Address=10.77.30.10/24
IPv6AcceptRA=no
DHCP=no
`

Provide a default route only on the approved egress interface:

`ini
# /etc/systemd/network/30-koa-public.network
[Match]
Name=eno1.110

[Network]
Address=192.0.2.10/24
Gateway=192.0.2.1
IPv6AcceptRA=no
DHCP=no
`

When IPv6 is active, configure explicit IPv6 addresses, routes, DNS, neighbor discovery, and firewall policy. Do not disable or ignore IPv6 while services continue to bind to it.

### 11.4 Validate networkd files

`bash
sudo networkctl cat eno1 2>/dev/null || true
sudo systemd-analyze verify \
 /etc/systemd/network/*.network \
 /etc/systemd/network/*.netdev
`

Use a maintenance window and console access before restarting the network manager.

## 12. Bind Services to Their Intended Interfaces

A firewall is not a substitute for correct service binding.

For each service:

1. identify the owning component;
2. select a Unix socket, loopback address, or zone address;
3. disable wildcard binding unless the contract requires it;
4. configure the component-owned authentication;
5. configure application authorization;
6. restart only the affected service;
7. verify the listener;
8. verify an unauthorized source is denied.

Examples of preferred binding:

`text
database Unix socket or owning-component network only
governance API Unix socket, loopback, or protected governance address
local metrics loopback or local collector socket
administrator API administration address or protected local socket
public web public address
private workflow private address
federation adapter federation address
backup agent backup address or outbound-only connection
`

Verify after each change:

`bash
ss -lntup
`

Keep a before-and-after service-binding record in the change directory.

## 13. Generate a Dedicated nftables Candidate

Create a candidate table without altering unrelated tables.

`bash
sudo tee "$WORK_DIR/koa-node.nft" >/dev/null <<'NFT'
table inet koa_node {
 set admin_ipv4_sources {
 type ipv4_addr
 flags interval
 elements = { 10.77.30.0/24 }
 }

 set private_ipv4_sources {
 type ipv4_addr
 flags interval
 elements = { 10.77.20.0/24 }
 }

 set federation_ipv4_peers {
 type ipv4_addr
 elements = { 10.77.40.20 }
 }

 set backup_ipv4_targets {
 type ipv4_addr
 elements = { 10.77.50.20 }
 }

 set local_infrastructure_ipv4 {
 type ipv4_addr
 elements = {
 10.77.20.53,
 10.77.20.123,
 10.77.20.80
 }
 }

 chain input {
 type filter hook input priority 0; policy drop;

 iifname "lo" accept
 ct state invalid drop
 ct state established,related accept

 ip protocol icmp accept
 ip6 nexthdr ipv6-icmp accept

 iifname "eno1.130" ip saddr @admin_ipv4_sources tcp dport 22 accept

 iifname "eno1.110" tcp dport { 80, 443 } accept

 iifname "eno1.120" ip saddr @private_ipv4_sources tcp dport {
 443
 } accept

 iifname "eno1.140" ip saddr @federation_ipv4_peers tcp dport {
 7443
 } accept

 iifname "eno1.150" ip saddr @backup_ipv4_targets tcp dport {
 9443
 } accept

 counter log prefix "koa-node-input-deny " flags all limit rate 10/minute drop
 }

 chain forward {
 type filter hook forward priority 0; policy drop;

 ct state invalid drop
 ct state established,related accept

 counter log prefix "koa-node-forward-deny " flags all limit rate 10/minute drop
 }

 chain output {
 type filter hook output priority 0; policy drop;

 oifname "lo" accept
 ct state invalid drop
 ct state established,related accept

 ip protocol icmp accept
 ip6 nexthdr ipv6-icmp accept

 ip daddr 10.77.20.53 udp dport 53 accept
 ip daddr 10.77.20.53 tcp dport 53 accept
 ip daddr 10.77.20.123 udp dport 123 accept

 ip daddr 10.77.20.80 tcp dport 443 accept

 ip daddr @backup_ipv4_targets tcp dport 9443 accept
 ip daddr @federation_ipv4_peers tcp dport 7443 accept

 counter log prefix "koa-node-output-deny " flags all limit rate 10/minute drop
 }
}
NFT
`

This example intentionally permits only illustrative ports and addresses. Replace them from active component and integration contracts.

Do not add:

- unrestricted `tcp dport 443` egress;
- broad private-range trust;
- public access to databases or metrics;
- forwarding between zones;
- permanent debug ports;
- provider addresses not owned by an active integration.

## 14. Validate the Firewall Candidate

Check syntax without applying:

`bash
sudo nft --check --file "$WORK_DIR/koa-node.nft"
`

Inspect the candidate:

`bash
sudo sed -n '1,260p' "$WORK_DIR/koa-node.nft"
`

Confirm:

- every interface exists or will exist;
- every set element is approved;
- every port maps to a service owner;
- IPv6 policy is complete;
- administration remains reachable;
- DNS and time remain local or explicitly declared;
- backup and federation use named destinations;
- forwarding remains disabled unless explicitly required;
- the log rate is bounded;
- no unrelated table is modified.

Record review approval in the local change record before applying.

## 15. Prepare Automatic Rollback

Create a rollback script using the previously captured ruleset.

`bash
sudo tee "$WORK_DIR/rollback-network.sh" >/dev/null <<EOF
#!/bin/sh
set -eu
nft delete table inet koa_node 2>/dev/null || true
nft -f '$WORK_DIR/nft_ruleset_before.nft'
EOF

sudo chmod 0700 "$WORK_DIR/rollback-network.sh"
`

Review the script and test it in a controlled environment.

Arm a short rollback timer immediately before applying:

`bash
sudo systemd-run \
 --unit="koa-network-rollback-$NETWORK_CHANGE_ID" \
 --on-active=3m \
 --property=Type=oneshot \
 "$WORK_DIR/rollback-network.sh"
`

Record the generated unit name:

`bash
printf '%s\n' "koa-network-rollback-$NETWORK_CHANGE_ID.service" \
 | sudo tee "$WORK_DIR/rollback_unit.txt" >/dev/null
`

Do not cancel the timer until local and remote validation succeeds.

## 16. Apply the Candidate

The default remains inspection-only.

`bash
if [ "$APPLY_CHANGES" != '1' ]; then
 printf '%s\n' 'Inspection complete. No network changes applied.'
 exit 0
fi
`

Apply only the dedicated table:

`bash
sudo nft delete table inet koa_node 2>/dev/null || true
sudo nft --file "$WORK_DIR/koa-node.nft"
`

Persist the table through the distribution’s active `nftables` configuration only after live validation. Do not assume `/etc/nftables.conf` already includes `/etc/nftables.d/`.

When network interface files changed, activate them according to the selected network manager and maintenance procedure. Avoid a broad network restart when a bounded reload is supported.

## 17. Administration Boundary

Administration access should use one of these patterns:

1. direct local console;
2. dedicated management interface;
3. dedicated management VLAN;
4. approved access broker;
5. time-bounded recovery interface.

Administration controls include:

- strong human identity;
- narrow source set;
- short-lived credentials where available;
- no shared generic account;
- bounded privileged operations;
- audit evidence;
- session expiry;
- revocation;
- separate application authorization.

SSH guidance for this reference layout:

- bind to the administration and recovery addresses only;
- disable password authentication when the active security contract permits key or hardware-backed authentication;
- disable root login;
- restrict users or groups;
- use a local firewall source allowlist;
- keep a console recovery path;
- do not expose SSH on the public address merely for convenience.

Verify the actual bind addresses rather than relying only on firewall denial.

## 18. Governance and Component Boundaries

Keep governance and component traffic narrow.

Recommended placement:

| Interface type | Preferred transport |
| --- | --- |
| Same-host privileged operation | Unix socket with operating-system access controls. |
| Same-host component API | Unix socket or loopback with component identity and authorization. |
| Cross-host governance API | Authenticated encrypted transport on a protected service network. |
| Component database | Unix socket, loopback, or owning-component-only network. |
| Audit evidence submission | Bounded application interface with evidence references. |
| Publication request | Publication Gateway interface only. |
| UCKK import | UCKK Import Bridge interface and quarantine path only. |

Do not create a broad “trusted internal services” subnet that bypasses application authentication.

## 19. Federation Boundary

Enable federation only when the active integration declares:

- peer identity;
- trust roots;
- tenant and authority scope;
- direction;
- artifact classes;
- capabilities;
- protocol and port;
- destination addresses;
- bandwidth and queue limits;
- quarantine;
- retry and expiry;
- reconciliation;
- removal.

Use a peer-specific firewall set.

Do not permit an entire remote private range when only one peer is authorized.

When the peer is unavailable:

- preserve local operation;
- queue only eligible work;
- retain cancellation;
- expose backlog state;
- revalidate before release after reconnection.

## 20. Backup Boundary

Prefer an outbound-only backup connection from the node to a named target.

The backup path should have:

- target identity;
- target address;
- authenticated encrypted transport;
- bounded bandwidth;
- backup window;
- verification;
- restore test;
- retention;
- removal and exit behavior.

Do not give the backup network unrestricted access to application interfaces or databases.

When inbound restore coordination is required, expose only the declared restore endpoint and only during the approved operation.

## 21. DNS, Time, Updates, and Offline Operation

### 21.1 DNS

Use local service discovery or stable local names for minimum local operation.

Permit DNS only to declared resolvers. A resolver response does not establish destination trust.

When public names are required for an optional external integration, bind resolution and egress to that integration.

### 21.2 Time

Use a declared local or trusted time source.

When time is materially uncertain:

- block certificate-sensitive activation;
- block expiring consent or trust decisions;
- block time-sensitive publication and federation;
- preserve non-time-sensitive local operation.

### 21.3 Updates

Prefer a local mirror or an explicitly declared update destination.

Update egress remains separate from general external-integration egress.

### 21.4 Offline state

Internet or public-DNS loss should not disable:

- local identity;
- local governance;
- local application use;
- local backup where the target is local;
- local support;
- local navigation;
- local evidence;
- local recovery.

Do not add a broad fallback resolver or provider when the declared source is unavailable.

## 22. Containers and Local Namespaces

Containers are an implementation mechanism, not a profile or authority boundary.

When rootless Podman is selected:

- use component or workspace labels;
- use separate networks for unrelated mutable owners;
- avoid `--network=host` unless explicitly required and reviewed;
- bind published ports to the intended host address;
- keep databases unpublished;
- validate host `nftables` behavior with rootless networking;
- preserve component application authentication;
- remove unselected optional networks and services;
- keep the host recovery path independent from the container runtime.

Example inspection:

`bash
podman ps --format \
 '{{.ID}}\t{{.Names}}\t{{.Networks}}\t{{.Ports}}\t{{.Labels}}'

podman network inspect network-name
`

Do not infer network ownership from a container name alone.

## 23. Validation

### 23.1 Interface and route validation

`bash
ip -brief link \
 | sudo tee "$WORK_DIR/ip_link_after.txt" >/dev/null

ip -brief address \
 | sudo tee "$WORK_DIR/ip_address_after.txt" >/dev/null

ip route show table all \
 | sudo tee "$WORK_DIR/ip_route_after.txt" >/dev/null

ip -6 route show table all \
 | sudo tee "$WORK_DIR/ip6_route_after.txt" >/dev/null
`

Confirm there is no unintended default route or route between protected zones.

### 23.2 Firewall validation

`bash
sudo nft list table inet koa_node \
 | sudo tee "$WORK_DIR/koa_node_table_after.nft" >/dev/null

sudo nft list ruleset \
 | sudo tee "$WORK_DIR/nft_ruleset_after.nft" >/dev/null
`

Confirm unrelated tables remain present.

### 23.3 Service binding validation

`bash
ss -lntup \
 | sudo tee "$WORK_DIR/listening_sockets_after.txt" >/dev/null
`

Confirm:

- public services bind only to public addresses;
- private services bind only to private addresses;
- administration binds only to administration or recovery addresses;
- databases and local metrics are not publicly bound;
- no removed optional service remains listening.

### 23.4 Connectivity tests

From controlled test clients, verify:

| Test | Expected result |
| --- | --- |
| Administration source to administration endpoint | Accepted with application authentication. |
| Non-administration source to administration endpoint | Denied. |
| Public client to approved public web port | Accepted. |
| Public client to private service | Denied. |
| Public client to database or metrics port | Denied. |
| Private client to approved private service | Accepted with application authorization. |
| Unregistered federation source to federation endpoint | Denied. |
| Registered peer to federation endpoint | Accepted only for declared protocol. |
| Backup target to unrelated service | Denied. |
| Node to local DNS and time | Accepted. |
| Node to undeclared Internet destination | Denied. |
| Node with Internet disconnected | Minimum local operation preserved. |
| Reconnected federation queue | Remains pending until revalidation. |

Use bounded tools such as `curl`, `nc`, `openssl s_client`, or the component’s health client. Avoid broad scanning outside the approved test scope.

### 23.5 Kernel validation

`bash
sysctl net.ipv4.ip_forward
sysctl net.ipv6.conf.all.forwarding
sysctl net.ipv4.conf.all.rp_filter
`

Unless the node has an approved routing role, forwarding should remain disabled.

### 23.6 Application validation

Verify through component-owned interfaces:

- identity and trust;
- governance decisions;
- publication requests and receipts;
- UCKK admission;
- backup;
- support;
- audit;
- local user workflows.

Network success alone does not prove application authorization.

## 24. Commit or Roll Back

### 24.1 Commit

After all validation succeeds:

1. persist the network-manager configuration;
2. persist the dedicated `nftables` table through the approved include path;
3. record active file paths and service versions;
4. record validation evidence;
5. cancel the rollback unit;
6. record completion time;
7. preserve the prior configuration according to the lifecycle policy.

Cancel the rollback unit:

`bash
sudo systemctl stop "koa-network-rollback-$NETWORK_CHANGE_ID.timer" \
 "koa-network-rollback-$NETWORK_CHANGE_ID.service" 2>/dev/null || true

sudo systemctl reset-failed \
 "koa-network-rollback-$NETWORK_CHANGE_ID.service" 2>/dev/null || true
`

Record completion:

`bash
date -u +'%Y-%m-%dT%H:%M:%SZ' \
 | sudo tee "$WORK_DIR/completed_at.txt" >/dev/null

printf '%s\n' 'complete' \
 | sudo tee "$WORK_DIR/change_status.txt" >/dev/null
`

### 24.2 Rollback

Run rollback immediately when:

- administration is lost;
- an unintended service is exposed;
- a required local service becomes unavailable;
- an unrelated firewall table changes;
- the node begins forwarding unexpectedly;
- DNS or time behavior violates the approved plan;
- offline local operation fails;
- tenant or component isolation fails.

`bash
sudo "$WORK_DIR/rollback-network.sh"
`

Restore network-manager files through the recorded predecessor configuration, reload the selected manager, and revalidate the last known working layout.

Record the result as `rolled_back` or `rollback_incomplete`.

## 25. Failure Handling

| Condition | Safe response |
| --- | --- |
| Interface identity differs from the plan | Stop and reconcile the deployment record. |
| Switch VLAN is unavailable | Preserve recovery access and do not activate the candidate. |
| Administration path fails | Allow the rollback timer to restore the predecessor state. |
| Candidate firewall syntax fails | Correct the candidate without changing the active ruleset. |
| Existing firewall ownership is unclear | Do not apply; identify table owners first. |
| Service still binds to a wildcard address | Keep the port denied and correct the service binding. |
| Required egress destination changes address | Update the integration record and review the rule; do not broaden egress. |
| Public DNS is unavailable | Continue local operation using declared local resolution. |
| Time source is unavailable | Block time-sensitive authority and repair time service. |
| Federation peer is unavailable | Queue eligible work without automatic release. |
| Backup target is unavailable | Preserve local data and report degraded backup state. |
| IPv6 policy is incomplete | Keep IPv6 exposure disabled at the service or complete the policy before activation. |
| Rootless container port bypasses expected binding | Stop the container, correct publication, and retest host policy. |
| Another component loses connectivity | Roll back or repair through the owning integration; do not add broad internal allow rules. |
| Ownership or trust is uncertain | Keep the affected route denied. |
| Rollback is incomplete | Preserve console access, stop optional services, and enter incident or recovery handling. |

## 26. Example Implementation Sequence

`text
resolve active profile, overlays, components, integrations, and Release Set
obtain console or out-of-band recovery
inventory interfaces, routes, services, firewall, and namespaces
choose active logical zones
select physical pattern
record addresses, gateways, DNS, time, backup, federation, and egress targets
build the service exposure matrix
configure VLANs or addresses without applying
bind services to intended addresses or sockets
generate a dedicated nftables candidate
validate nftables syntax
review IPv4 and IPv6 behavior
capture the predecessor ruleset
arm automatic rollback
apply the dedicated table
activate network changes through the selected manager
test administration first
test public, private, governance, federation, backup, and egress boundaries
disconnect Internet and verify minimum local operation
verify queues remain pending after reconnection until revalidated
persist the validated configuration
cancel rollback
record evidence and completion
`

## 27. Completion Checklist

- [ ] Active `sovereign_linux_node` profile resolved.
- [ ] Selected overlays are explicit.
- [ ] Active Release Set recorded.
- [ ] Required and optional components recorded.
- [ ] Active integrations recorded.
- [ ] Console or out-of-band recovery verified.
- [ ] Existing interfaces, addresses, routes, services, and firewall captured.
- [ ] Active zones selected explicitly.
- [ ] Physical pattern recorded.
- [ ] Address and route plan approved.
- [ ] Every active listener has an owning component and zone.
- [ ] Databases, queues, object stores, metrics, and privileged sockets remain unexposed.
- [ ] Services bind to intended addresses or sockets.
- [ ] Candidate table changes only `inet koa_node`.
- [ ] No global firewall flush command is used.
- [ ] Ingress defaults to deny.
- [ ] Forwarding defaults to deny.
- [ ] Egress is destination-specific.
- [ ] IPv4 and IPv6 behavior are both accounted for.
- [ ] Administration sources are allowlisted.
- [ ] Federation peers are explicit.
- [ ] Backup targets are explicit.
- [ ] DNS and time sources are explicit.
- [ ] Public DNS and Internet are not required for minimum local operation.
- [ ] Automatic rollback was armed before application.
- [ ] Administration validation passed.
- [ ] Public-to-private denial passed.
- [ ] Unregistered peer denial passed.
- [ ] Undeclared egress denial passed.
- [ ] Offline local-operation validation passed.
- [ ] Reconnection revalidation behavior passed.
- [ ] Unrelated firewall tables remain intact.
- [ ] Rollback or predecessor configuration remains available.
- [ ] Change record is `complete`, `rolled_back`, or `rollback_incomplete`.

## 28. References

Use this recipe with the active versions of:

- `00-governance/02-documentation-contract.md`;
- `00-governance/09-recipes-and-implementation-guidance.md`;
- `07-security/08-network-boundaries.md`;
- `07-security/17-cross-domain-publication.md`;
- `08-operations/05-capacity-management.md`;
- `08-operations/15-support-and-diagnostics.md`;
- `09-conformance/04-profile-test-matrices.md`;
- `contracts/profiles/sovereign-linux-node.profile.json`;
- the active component contracts;
- the active integration contracts;
- the active Release Set;
- the deployment’s address, trust, service, backup, federation, and recovery records.

Where this recipe conflicts with an active canonical contract, the canonical contract controls and this recipe must be corrected.
