# Resource Governor migrations

This architecture revision defines no SQL migration for the Resource Governor
adapter bundle. The absence is intentional rather than a placeholder.

The adapters in this bundle have the following persistence boundaries:

- the active profile and resource envelopes are immutable, versioned files read
  through `ProfileFileProvider`;
- procfs and systemd observations are ephemeral measurements and are never
  written back as canonical capacity or envelope state;
- host resource mutations are delegated through the public, profile-declared
  Node Agent operation boundary;
- critical resource evidence is delivered through the public Audit Broker
  boundary and is not stored in another component's database.

Resource Governor owns active-envelope, allocation, and delegated queue state,
but a durable store for that state must be introduced only by an explicitly
inventoried migration bundle with its own ports, schema, backup, restore,
reconciliation, rollback, and receipt tests. Another component must never write
that store directly, and Resource Governor must never use a workload owner's
business database as its persistence mechanism.

When migrations are introduced, they must be numbered, immutable after release,
applied atomically, verified before activation, and capable of preserving the
last valid enforceable state when an upgrade cannot complete.
