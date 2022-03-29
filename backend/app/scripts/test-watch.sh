#!/usr/bin/env bash

set -e
set -x

ptw --runner "./scripts/test.sh" -p -- --last-failed --new-first --exitfirst