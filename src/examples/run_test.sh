# -----------------------------------------------------------------------------
# MIT License
# 
# Copyright (c) 2025 Mattia Antonini (Fondazione Bruno Kessler) m.antonini@fbk.eu
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------
#
# run_test.sh - Bash script to run tests between CPython and MicroPython

#!/bin/bash

CPYTHON=python3
MPYTHON=../../firmware/dev-scripts/output/micropython

run_test() {
    echo "Testing $1"

    # CPython -> MicroPython
    if ! $CPYTHON mpickle_tests.py --example_name "$1" --dump; then
        echo "FAIL: CPython Pickle dump failed for $1"
        return 1
    fi

    OUT2=$($MPYTHON mpickle_tests.py --example_name "$1" --load)
    if [ $? -ne 0 ]; then
        echo "FAIL: MicroPython mPickle load failed for $1"
        echo "Error details: $OUT2"
        return 1
    fi

    rm -f dump.pkl
    OUT2_LAST=$(echo "$OUT2" | tail -n 1)
    echo "Test Dump: CPython (pickle) -> Load: MicroPython (mpickle): $OUT2_LAST"

    # MicroPython -> CPython
    if ! $MPYTHON mpickle_tests.py --example_name "$1" --dump; then
        echo "FAIL: MicroPython mPickle dump failed for $1"
        return 1
    fi

    OUT4=$($CPYTHON mpickle_tests.py --example_name "$1" --load)
    if [ $? -ne 0 ]; then
        echo "FAIL: CPython Pickle load failed for $1"
        return 1
    fi

    rm -f dump.pkl
    OUT4_LAST=$(echo "$OUT4" | tail -n 1)
    echo "Test Dump: MicroPython (mpickle) -> Load: CPython (pickle): $OUT4_LAST"

    # MicroPython -> MicroPython
    if ! $MPYTHON mpickle_tests.py --example_name "$1" --dump; then
        echo "FAIL: MicroPython mPickle dump failed for $1"
        return 1
    fi

    OUT6=$($MPYTHON mpickle_tests.py --example_name "$1" --load)
    if [ $? -ne 0 ]; then
        echo "FAIL: MicroPython mPickle load failed for $1"
        echo "$OUT6"
        return 1
    fi

    rm -f dump.pkl
    OUT6_LAST=$(echo "$OUT6" | tail -n 1)
    echo "Test Dump: MicroPython (mpickle) -> Load: MicroPython (mpickle): $OUT6_LAST"

    echo "Test passed for $1"
    echo
}

run_test "builtins-data-types"
run_test "custom-class"
run_test "numpy-ndarray"
