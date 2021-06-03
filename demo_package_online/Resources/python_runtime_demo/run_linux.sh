#!/bin/sh
BASEDIR=$(dirname $0)
export LD_LIBRARY_PATH=${BASEDIR}/twin_runtime/lib:${LD_LIBRARY_PATH}
python3 run.py TwinModel
