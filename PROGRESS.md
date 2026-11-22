# PROGRESS (sec/fix-image-findings-2026-11-22) - delete in final commit

Stack: Python / Streamlit multipage app (pandas + plotly; seaborn, altair, watchdog also listed), pip requirements.txt with `~=` pins from 2022 (numpy 1.22 / pandas 1.4 only install on Python <= 3.10); README documents a systemd deployment, not Docker. NO Dockerfile, compose file, CI or tests in this repo; image miniapps-streamlit is built from a path outside the repo (not visible; unclear whether it is only this app).

- [x] 1. Clone, branch, read repo
- [ ] 2. Scan before (throwaway image, NOT committed: python:3.10-slim + host-installed deps; Python version of the server image is an assumption)
- [ ] 3. Fix fixable findings (requirements.txt only)
- [ ] 4. Smoke test (pages run with AppTest, server health), rescan
- [ ] 5. Commit, push, PR
- [ ] 6. PR checks

## Notes
