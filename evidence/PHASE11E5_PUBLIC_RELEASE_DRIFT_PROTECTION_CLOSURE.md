# PHASE 11E.5 — Public Release Drift Protection Operational Closure

Status: **OPERATIONAL / VERIFIED**

Repository: `k49095107-sketch/lingua-track-desktop-releases`
Protected release: `v1.0.0-desktop.1`
Release ID: `396023249`

## Pinned PHASE 11E.2 baseline

- Repository visibility: `public`
- Tag commit: `b0e98ef8d15b97bd1aed50bc3b4f6b508bebf261`
- Git tree: `b97b1d6f571a9bd8728fe4a65a7829565eed771a`
- Release state: `prerelease=true`, `draft=false`
- Expected asset count: `4`

### Asset digests

- `LINGUA_TRACK_VERIFY_SIGSTORE.txt`
  - `sha256:75adff8afd5be0441d9e84ebff4eaa3e1a61fa965d59da193c47c101a4cab21d`
- `PHASE11C7_SIGNED_RC_SHA256.txt`
  - `sha256:1a485252a50561002253d779ef651eef202b7af5e010989dc5260cb5c3760114`
- `lingua-track_1.0.0.desktop.1+phase11c3_amd64.deb`
  - `sha256:aacaa10b4c877a08c480fb48b7790ed2f824b4a483050b130c87789c0839a64f`
- `lingua-track_1.0.0.desktop.1+phase11c3_amd64.deb.sigstore.json`
  - `sha256:55a79973c9d5e53028a1569efa05f4b2fc40ec2b1f6c21108c119f381ec9e849`

## PHASE 11E.3 — Scheduled detector proof

Workflow: `.github/workflows/phase11e3-public-release-drift-monitor.yml`

Operational controls:
- GitHub Actions schedule: daily at `06:17 UTC`
- Manual `workflow_dispatch` retained
- Workflow-change push self-test retained
- Token permission: `contents: read`
- Concurrency prevents overlapping monitor executions
- Any baseline mismatch exits non-zero with:
  - `FAIL — PUBLIC RELEASE DRIFT DETECTED`

Initial verified PASS:
- Run #1: `36463496420`
- Conclusion: `success`
- Result: pinned public release matched PHASE 11E.2 baseline

## PHASE 11E.4 — Failure / recovery proof

Controlled failure injection:
- Only the workflow's expected Release ID was changed:
  - expected `396023249` -> test-only `396023250`
- The real release, tag and four release assets were not changed.
- Run #2: `36464380555`
- Conclusion: `failure`
- Detector observed actual Release ID `396023249` against test-only expected `396023250`.
- Required detector result:
  - `FAIL — PUBLIC RELEASE DRIFT DETECTED`

Recovery:
- Correct expected Release ID `396023249` restored in commit:
  - `7f55089c01dc4e6f494f19c25c94d18da05c43e1`
- Recovery Run #7: `37025968226`
- Conclusion: `success`
- Final result:
  - `PASS — pinned public release matches PHASE 11E.2 baseline`

## PHASE 11E.5 hardening verification

Verified after recovery:
- No test-only Release ID `396023250` remains in the operational workflow.
- Expected Release ID is `396023249`.
- Scheduled monitoring remains enabled in the workflow definition.
- Runtime token remains read-only for repository contents.
- The detector still checks visibility, Release ID, tag commit, Git tree, prerelease/draft state, exact asset set, and all four GitHub-reported SHA-256 asset digests.
- The protected release remains unchanged.

## Closure

Evidence chain:

`PINNED BASELINE -> SCHEDULED PASS -> CONTROLLED DRIFT FAIL -> BASELINE RESTORE -> RECOVERY PASS -> OPERATIONAL HARDENING`

Final status:

**PUBLIC RELEASE DRIFT PROTECTION — OPERATIONAL / VERIFIED**
