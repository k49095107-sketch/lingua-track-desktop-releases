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


## PHASE 11F.4.1 — Historical publisher provenance (2026-10-29)

The private build repository's current `main` tree was inspected via Git trees API: it contains exactly `README.md` (tree `c173d5a17cff5dc79a22ebc8ea48bce47f9e11c0`), with no active publisher workflow on that branch.

Historical GitHub Actions records revealed:
- `PHASE 11C.9 GitHub Prerelease Publication`, workflow `.github/workflows/phase11c9-release-publication.yml`, historical commit `1034b7657fbb8f2589a4215b96659860550b3325`.
- `PHASE 11C.11 Public Release Export`, workflow `.github/workflows/phase11c11-public-release-export.yml`, historical commit `d0102da4c9e3fb02e45755bfe6da81666f2302a2`.

The PHASE 11C.9 workflow was directly retrieved from its historical commit:
- It used `gh release create` for its first publication.
- For an existing release, it used `gh release edit` and `gh release upload --clobber`. Such reconciliation/overwrite logic must **NOT** be copied into future publication flow because it can mutate an already published release.
- It did verify the frozen signed candidate with SHA-256 and Sigstore before publication and downloaded published assets for subsequent verification.
- It targeted its own private repository (`$GITHUB_REPOSITORY`), not the current public release-only repository; therefore this is historical evidence, not proof of the current public publisher entry point.

The PHASE 11C.11 workflow produced a verified release export artifact and explicitly did **not** publish a public release.

### Updated integration decision

Do not reactivate the historical `phase11c9-release-publication.yml` or its overwrite branch. A future publisher must be a new, release-unique, create-only entry point with no `gh release edit` / `gh release upload --clobber` recovery branch. When target tag/release already exists, fail closed and require a different version or an explicitly reviewed exception outside the normal automated path.

**Outcome:** real historical publisher mechanism identified, but no active publication entry point exists in the current private `main` or public release repository. Enforceable production integration remains unproven. PHASE 11F.4.1 is **DISCOVERY VERIFIED / ENFORCEMENT PENDING**, not a final PASS.
