#!/usr/bin/env bash

set -e
set -x

bash scripts/test.sh --html=report.html --cov-report=html  --cov=app "${@}"
