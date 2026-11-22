# PROGRESS: sec/image-cves-20261122

Findings: `image-update:miniapps-streamlit` (pillow CVEs, image f710bc1aa87e), `runtime:Python:upstream` (pip 23.0.1 / py3.10, streamlit target).

- [x] 1. Worktree + branch from origin/main
- [x] 2. Add server's Dockerfile to repo as-is (it exists only on scopalserver; drift), sha256 identical
- [x] 3. Build baseline image (linux/amd64) + Trivy scan, before-evidence saved
- [x] 4. Regression check `tests/check_image.sh`: RED on baseline (pillow 12.3.0)
- [x] 5. Fix: pillow>=13.0.0 needs Python>=3.11 -> python:3.11-slim, numpy~=1.23.5 / pandas~=1.5.3 (cp311 wheels), pyarrow<26 (26 needs NumPy 2), pip>=26.2.2
- [x] 6. Re-scan, check GREEN, headless health check + all 5 pages rendered over the websocket without exceptions (2 iterations)
- [ ] 7. PR (deploy procedure, smoke check, rollback)

## Evidence (local scan 22.11., linux/amd64, Trivy DB of 22.11.)
- Before: pillow 12.3.0, 43 CVEs (5 CRITICAL: -112393/-112398/-112403/-112900/-96639), all fixed in 13.0.0; pip 23.0.1 (7 CVEs, fix <= 26.2.0; CVE-2026-133949 fixed in 26.2.2); py 3.10.22. Total 309 findings (5 CRIT / 81 HIGH).
- After: pillow 13.0.0 (0 pillow CVEs), pip 26.3 (0), py 3.11.18. Total 253 findings (0 CRIT / 56 HIGH).
- check_image.sh: before exit 1 (pillow 12.3.0 < 13.0.0); after "pillow 13.0.0 python 3.11.18 / No broken requirements found / OK".
- Iteration 1 failed: pyarrow 26.0.1 (released 03.11.) needs NumPy 2, import streamlit broke with numpy 1.23.5 -> pinned pyarrow<26. Iteration 2 green.

## Open questions
- Server app dir is not a git checkout; deploy = copy Dockerfile + requirements.txt there (data-final/*.csv, countries.geojson are gitignored and live only on the server).
- Not fixed (out of scope, no pinned package or needs streamlit major bump): streamlit 1.22.0 (4 CVEs, fix 1.54.0), protobuf 3.20.3 (2 HIGH, streamlit pins <4), setuptools 79.0.1 + vendored jaraco.context/wheel (HIGH), Debian libc6/zlib1g (fix is in Debian as deb13u5/deb13u1 but not yet in python:3.11-slim).
