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
    echo -e "\e[0;36mTesting \e[1;36m$1\e[0m"

    # CPython -> MicroPython
    OUT1=$($CPYTHON mpickle_tests.py --example_name "$1" --dump)
    STATUS1=$?
    if [ "$STATUS1" -ne 0 ]; then
        echo -e "\e[0;31mFAIL: CPython Pickle dump failed for $1\e[0m"
        return
    fi

    OUT2=$($MPYTHON mpickle_tests.py --example_name "$1" --load)
    STATUS2=${PIPESTATUS[0]}  # Capture exit status of the first command in the pipe
    OUT2_LAST_LINE=$(echo "$OUT2" | tail -n 1)  # Extract last line separately

    if [ "$STATUS2" -ne 0 ]; then
        echo -e "\e[0;31mFAIL: MicroPython mPickle load failed for $1\e[0m"
        return
    fi

    rm -f dump.pkl
    echo "Test Dump: CPython (pickle) -> Load: MicroPython (mpickle): $OUT2_LAST_LINE"

    # MicroPython -> CPython
    OUT3=$($MPYTHON mpickle_tests.py --example_name "$1" --dump)
    STATUS3=$?
    if [ "$STATUS3" -ne 0 ]; then
        echo -e "\e[0;31mFAIL: MicroPython mPickle dump failed for $1\e[0m"
        return
    fi

    OUT4=$($CPYTHON mpickle_tests.py --example_name "$1" --load)
    STATUS4=${PIPESTATUS[0]}
    OUT4_LAST_LINE=$(echo "$OUT4" | tail -n 1)

    if [ "$STATUS4" -ne 0 ]; then
        echo -e "\e[0;31mFAIL: CPython Pickle load failed for $1\e[0m"
        return
    fi

    rm -f dump.pkl
    echo "Test Dump: MicroPython (mpickle) -> Load: CPython (pickle): $OUT4_LAST_LINE"

    # MicroPython -> MicroPython

    OUT5=$($MPYTHON mpickle_tests.py --example_name "$1" --dump)
    STATUS5=$?
    if [ "$STATUS5" -ne 0 ]; then
        echo -e "\e[0;31mFAIL: MicroPython mPickle dump failed for $1\e[0m"
        return
    fi

    OUT6=$($MPYTHON mpickle_tests.py --example_name "$1" --load)
    STATUS6=${PIPESTATUS[0]}
    OUT6_LAST_LINE=$(echo "$OUT6" | tail -n 1)

    if [ "$STATUS6" -ne 0 ]; then
        echo -e "\e[0;31mFAIL: MicroPython mPickle load failed for $1\e[0m"
        echo $OUT6
        return
    fi

    rm -f dump.pkl
    echo "Test Dump: MicroPython (mpickle) -> Load: MicroPython (mpickle): $OUT6_LAST_LINE"

    echo -e "\e[0;32mTest passed for $1\e[0m\n"
}

run_test "builtins-data-types"
run_test "custom-class"
run_test "numpy-ndarray"
