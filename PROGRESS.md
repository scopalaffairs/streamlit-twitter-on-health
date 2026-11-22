# PROGRESS (sec/fix-image-findings-2026-11-22) - delete in final commit

Stack: Python / Streamlit multipage app (pandas + plotly; seaborn, altair, watchdog also listed), pip requirements.txt with `~=` pins from 2022 (numpy 1.22 / pandas 1.4 only install on Python <= 3.10); README documents a systemd deployment, not Docker. NO Dockerfile, compose file, CI or tests in this repo; image miniapps-streamlit is built from a path outside the repo (not visible; unclear whether it is only this app).

- [x] 1. Clone, branch, read repo
- [x] 2. Scan before (throwaway image, NOT committed: python:3.10-slim + host-installed deps; Python version of the server image is an assumption)
- [ ] 3. Fix fixable findings (requirements.txt only)
- [ ] 4. Smoke test (pages run with AppTest, server health), rescan
- [ ] 5. Commit, push, PR
- [ ] 6. PR checks

## Notes
- Before (Trivy 0.76.1, throwaway image python:3.10-slim (Debian 13.7, image last rebuilt Oct 6 = EOL line, no more upstream rebuilds) + repo requirements.txt installed with uv on the host as linux/arm64 wheels; the real server image/Python version is NOT visible): HIGH+CRIT 86 findings / 47 unique CVEs (5 CRITICAL, 81 HIGH). python-pkg 33: pillow 12.3.0 x29 (5 CRIT; fix 13.0.0 which needs Python >= 3.11 and streamlit >= 1.66), protobuf 3.20.3 x2 (fix 6.33.5+), vendored wheel 0.45.1 and jaraco.context 5.3.0 from the base setuptools 79.0.1. os-pkgs 53: 50 no fix; 3 fixable only via apt (apt/libapt-pkg7.0 3.0.4, zlib1g deb13u1).
- The release notes' server image has only ~49-51 HIGH, i.e. no python-pkg findings: the server build evidently does NOT install this repo's requirements.txt as-is (or uses another Python/package set). The pins here are still old: pip-audit flags streamlit 1.22.0 (PYSEC-2024-153 fixed 1.37.0, GHSA-8qw9-gf7w-42x5 1.30.0, PYSEC-2026-212 1.53.1, PYSEC-2026-2285 1.54.0).
- Constraint: tornado 6.6+ and pillow 13 need Python >= 3.11; streamlit <= 1.65 caps pillow < 13. Python 3.10-compatible best case: streamlit 1.54 (needs numpy >= 1.23).
- Plan (py3.10-compatible, no behaviour change expected): streamlit~=1.54.0, numpy~=1.23.5, setuptools>=81; keep pandas/plotly/seaborn/altair/watchdog pins. Verify the four pages with streamlit AppTest on py3.10 and start the server in the container.
