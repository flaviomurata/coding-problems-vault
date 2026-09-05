#!/usr/bin/env bash

set -e
set -x

# Backend tests run without a frontend build.
FASTAPI_ENV=development coverage run -m pytest tests/
coverage report
coverage html --title "${@-coverage}"
