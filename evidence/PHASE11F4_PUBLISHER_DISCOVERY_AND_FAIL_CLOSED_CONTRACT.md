# PHASE 11F.4 — Publisher Discovery and Fail-Closed Integration Contract

Status: **PARTIAL — DESIGN RECORDED; ENFORCEMENT NOT VERIFIED**

## Findings (2026-10-29)
- Public repository `k49095107-sketch/lingua-track-desktop-releases`: `.github/workflows` contains only:
  - `phase11e3-public-release-drift-monitor.yml`
  - `phase11f2-baseline-rollover-dry-run.yml`
  - `phase11f3-release-promotion-safety-gates.yml`
- None is a production publisher; 11F.2/11F.3 are synthetic demonstrations.
- Private build repository `k49095107-sketch/lingua-track-desktop-build`: `README.md` is readable and explicitly describes build/QA-only infrastructure and instructs against publishing. A conventional `.github/workflows/release.yml` does not exist. Broader repository directory inventory could not be retrieved with the currently available API route, so no claim is made that there is no other publisher.
- No production publishing operation was executed during 11F.4.

## Integration requirements (future actual publisher)

1. Identify the actual authorized `gh release create`, GitHub Release API, or equivalent publication entry point.
2. Place a mandatory fail-closed gate on the same execution path, with no bypass job or alternative write token:
   - exact pinned candidate source/build identity;
   - signed build and independently verified Sigstore bundle;
   - SHA-256 validation of actual candidate bytes;
   - required install/runtime QA evidence;
   - exact release artifact allowlist;
   - version/tag uniqueness and no overwrite of an existing published release.
3. Prohibit release publication unless all prior checks have passed and results are bound to the exact candidate package.
4. After uploading, verify release ID, tag commit/tree, state, complete asset set and published digests independently.
5. Only after post-upload verification update the drift monitor baseline through an explicit reviewed change.
6. Require a successful drift monitor run on the new baseline before closing the handoff.
7. A failed gate or partially completed release must stop further promotion; never silently adjust expected values.
8. Keep last-known-good release and baseline available; use a new release/version for a corrected candidate.

## Verification gates before PHASE 11F.4 closure
- [ ] Real publisher entry point identified and inspected.
- [ ] Gate enforced on every real publishing path.
- [ ] Negative test proves real publish action is prevented before it runs.
- [ ] Positive test proves publishing is *eligible* only after validated candidate evidence.
- [ ] Production release and baseline remain unchanged during tests.
- [ ] GitHub Actions run and logs show end-to-end enforcement.

Until these checks exist, status remains **PARTIAL / NOT CLOSED**. Synthetic PASS from PHASE 11F.3 is not evidence of live publisher enforcement.
