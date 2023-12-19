#!/bin/bash

set -e

if [ -z "${1-}" ];
then
cmd="uvicorn --host 0.0.0.0 src.app:app"
else	cmd="$@"
fi
exec $cmd
