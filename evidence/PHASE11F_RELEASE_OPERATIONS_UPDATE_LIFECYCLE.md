# PHASE 11F — Release Operations / Update Lifecycle Contract

Status: **DEFINED / ACTIVE**

This document defines the release lifecycle for Lingua Track Desktop after PHASE 11E public-release drift protection was proven operational.

## 1. Core rule

A published release is never edited in place as part of a normal update.

A new product version must receive:
- a new version/tag;
- a new release identity;
- newly generated package and signing evidence;
- its own pinned integrity baseline.

The currently protected release `v1.0.0-desktop.1` remains historical evidence and is not repurposed for a later build.

## 2. Release lifecycle

### A. Build candidate in the private build repository
The private build repository remains the source/build environment.

Before public publication, the candidate must pass the applicable build, install, runtime, uninstall, integrity/signing, and distribution gates.

### B. Freeze candidate identity
Before publication record:
- source/build commit;
- package filename;
- package SHA-256;
- signature/Sigstore evidence;
- expected release asset set.

After freeze, the candidate bytes must not be silently replaced.

### C. Publish as a new public release
Create a new tag/release in the public release-only repository.

Do not overwrite or mutate the previous release to represent the new version.

### D. Verify public bytes
After upload, verify the public release itself:
- repository visibility;
- tag -> commit;
- Git tree;
- release ID/state;
- exact asset names;
- GitHub-reported SHA-256 digests;
- package/signature verification where applicable.

A release is not accepted merely because upload succeeded.

### E. Pin the new baseline
Only after public verification passes may the drift monitor baseline be moved to the new release.

The baseline update must be an explicit repository commit containing the new:
- release ID;
- tag;
- tag commit;
- Git tree;
- exact asset set;
- asset SHA-256 digests.

### F. Verify baseline handoff
The first monitor run against the new baseline must complete successfully.

Until that PASS exists, the baseline handoff is not closed.

## 3. Failure rules

If candidate QA fails:
- do not publish the candidate.

If publication is incomplete or public verification fails:
- do not advance the drift baseline;
- preserve evidence of the failure;
- correct the release process using a new clean candidate/release when replacement would alter already-published bytes.

If the baseline handoff fails:
- retain the last known-good baseline;
- investigate before declaring the new release protected.

If scheduled drift monitoring later fails unexpectedly:
- treat the protected public release as potentially changed until the mismatch is explained;
- do not normalize the mismatch by blindly editing expected values.

## 4. Baseline rollover invariant

At every handoff there must be a provable chain:

`OLD BASELINE PASS -> NEW RELEASE VERIFIED -> NEW BASELINE COMMIT -> NEW BASELINE PASS`

The old release evidence remains retained after rollover.

## 5. Separation of responsibilities

Private build repository:
- source/build operations;
- candidate QA;
- signing/build evidence.

Public release-only repository:
- distributable release assets;
- public verification evidence;
- pinned drift baseline;
- scheduled read-only drift monitoring.

## 6. Current protected release

Current protected baseline remains:
- tag: `v1.0.0-desktop.1`
- Release ID: `396023249`
- tag commit: `b0e98ef8d15b97bd1aed50bc3b4f6b508bebf261`
- Git tree: `b97b1d6f571a9bd8728fe4a65a7829565eed771a`

PHASE 11F does not change this release.

## 7. Required evidence for every future release

A future release is operationally closed only when evidence exists for:
1. candidate QA PASS;
2. signed/checksummed candidate identity;
3. public release publication;
4. public post-upload integrity verification;
5. explicit drift-baseline rollover commit;
6. first PASS against the new baseline.

## 8. Final lifecycle rule

**Never move the baseline first and then assume the release is valid. Verify the release first; move the baseline second; require a monitor PASS third.**

Lifecycle state:

**RELEASE OPERATIONS / UPDATE LIFECYCLE — DEFINED**
