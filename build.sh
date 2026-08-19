# =============================================================================
#  build.sh  —  Optional explicit build script for Render
#  (render.yaml buildCommand is preferred, but this works too)
# =============================================================================
#!/usr/bin/env bash
set -o errexit   # exit immediately on error

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input
