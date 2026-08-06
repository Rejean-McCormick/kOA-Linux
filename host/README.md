# kOA host platform

This directory contains host-platform integration owned by kOA-Linux. It does
not contain component business logic and it does not grant release authority.

## Boot and image boundary

- `host/image/` builds and verifies immutable host-image artifacts from
  explicitly supplied inputs. It never mutates a running node or component
  data.
- `host/boot/` verifies already issued Release Sets and records explicit,
  durable slot-selection and acceptance transitions.
- `active`, `candidate`, `previous_good`, and `recovery` are distinct states.
- A successful boot is not acceptance. `mark-boot-success.py` requires a
  profile health verdict before it can accept a candidate.
- There is no automatic fallback. Recovery and last-known-good entry are
  explicit, attributable operations that produce receipts.

## Deterministic image flow

1. Materialize an admitted root filesystem without executing candidate code.
2. Run `build-rootfs.py` with a fixed `SOURCE_DATE_EPOCH` or `--source-date-epoch`.
3. Verify the complete signed Release Set with `verify-release-set.py`.
4. Obtain externally produced provenance, SBOM, and signature-verification
   evidence.
5. Run `seal-image.py` to bind those inputs to the rootfs digest.
6. Run `verify-image.py`; use its receipt as the image-verification input for
   slot selection.

The scripts use JSON-compatible YAML documents so the implementation remains
usable with the Python standard library. They write state and receipts through
atomic replacement and fail closed on malformed, incomplete, incompatible, or
unverified inputs.

## Privilege boundary

These utilities prepare and verify files. Installation, partition mutation,
boot-loader changes, mount operations, and other privileged effects must pass
through the Node Agent or another registered narrow broker. Running a script as
an administrator does not authorize an invalid Release Set or image.
