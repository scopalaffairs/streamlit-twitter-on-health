#!/bin/sh
# Regression check for the image CVEs (pillow CVE-2026-112393/-112398/-112403/-112900/-96639,
# all fixed in 13.0.0): build the image like the server does and assert the installed pillow.
# Usage: tests/check_image.sh   (needs docker)
set -eu
cd "$(dirname "$0")/.."

docker build --platform linux/amd64 -q -t sec-streamlit:check . >/dev/null
docker run --rm --platform linux/amd64 sec-streamlit:check python -c '
import importlib.metadata as m, sys
v = tuple(int(x) for x in m.version("pillow").split(".")[:3])
print("pillow", m.version("pillow"), "python", sys.version.split()[0])
assert v >= (13, 0, 0), "pillow < 13.0.0 is affected"
import streamlit  # app imports cleanly with the pinned set
'
docker run --rm --platform linux/amd64 sec-streamlit:check pip check
echo OK
