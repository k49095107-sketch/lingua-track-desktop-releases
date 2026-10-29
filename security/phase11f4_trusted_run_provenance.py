#!/usr/bin/env python3
"""Fail-closed GitHub Actions provenance validator; no publishing operations.

Candidate and QA run descriptions must come from authenticated GitHub API
responses; never accept these dictionaries from the candidate artifact.
"""
import json
import re
import sys

EXPECTED_SOURCE_REPOSITORY = "k49095107-sketch/lingua-track-desktop-build"
# Keep blank until future approved production pipelines are created and reviewed.
TRUSTED_BUILD_WORKFLOW_ID = None
TRUSTED_QA_WORKFLOW_ID = None
TRUSTED_BUILD_PATH = None
TRUSTED_QA_PATH = None


def validate(build, qa, *, source_repo=EXPECTED_SOURCE_REPOSITORY,
             build_workflow_id=TRUSTED_BUILD_WORKFLOW_ID,
             qa_workflow_id=TRUSTED_QA_WORKFLOW_ID,
             build_path=TRUSTED_BUILD_PATH, qa_path=TRUSTED_QA_PATH):
    failures = []
    if not all([build_workflow_id, qa_workflow_id, build_path, qa_path]):
        failures.append("trusted future workflow identities are not configured")
        return failures
    if build_workflow_id == qa_workflow_id:
        failures.append("build and QA must be separate trusted workflows")
    for label, run, workflow_id, path in (
        ("build", build, build_workflow_id, build_path),
        ("qa", qa, qa_workflow_id, qa_path),
    ):
        if run.get("repository", {}).get("full_name") != source_repo:
            failures.append(label + ": wrong source repository")
        if run.get("workflow_id") != workflow_id or run.get("path") != path:
            failures.append(label + ": untrusted workflow identity/path")
        if run.get("status") != "completed" or run.get("conclusion") != "success":
            failures.append(label + ": run not successfully completed")
        if run.get("event") not in ("push", "workflow_dispatch"):
            failures.append(label + ": unapproved trigger event")
        if not re.fullmatch(r"[0-9a-f]{40}", run.get("head_sha", "")):
            failures.append(label + ": invalid commit")
        if run.get("run_attempt") != 1:
            failures.append(label + ": rerun requires independent review")
    if build.get("head_sha") != qa.get("head_sha"):
        failures.append("build and QA did not use the exact same commit")
    if build.get("id") == qa.get("id"):
        failures.append("build and QA may not be the same run")
    return failures


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: trusted_run_provenance.py BUILD_API_JSON QA_API_JSON")
    with open(sys.argv[1], encoding="utf8") as f:
        build = json.load(f)
    with open(sys.argv[2], encoding="utf8") as f:
        qa = json.load(f)
    errs = validate(build, qa)
    if errs:
        for err in errs:
            print("FAIL:", err)
        sys.exit(1)
    print("PASS: authenticated trusted build and QA runs")
