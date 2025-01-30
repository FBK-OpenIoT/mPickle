#!/bin/bash

CPYTHON=python3
MPYTHON=../../firmware/dev-scripts/output/micropython

run_test() {
    echo -e "\e[0;36mTesting \e[1;36m$1\e[0m"

    # CPython -> MicroPython
    OUT1=$($CPYTHON pickle_test.py --example_name "$1" --dump)
    STATUS1=$?
    if [ "$STATUS1" -ne 0 ]; then
        echo -e "\e[0;31mFAIL: CPython dump failed for $1\e[0m"
        return
    fi

    OUT2=$($MPYTHON pickle_test.py --example_name "$1" --load)
    STATUS2=${PIPESTATUS[0]}  # Capture exit status of the first command in the pipe
    OUT2_LAST_LINE=$(echo "$OUT2" | tail -n 1)  # Extract last line separately

    if [ "$STATUS2" -ne 0 ]; then
        echo -e "\e[0;31mFAIL: MicroPython load failed for $1\e[0m"
        return
    fi

    echo "Output (CPython -> MicroPython): $OUT2_LAST_LINE"

    # MicroPython -> CPython
    OUT3=$($MPYTHON pickle_test.py --example_name "$1" --dump)
    STATUS3=$?
    if [ "$STATUS3" -ne 0 ]; then
        echo -e "\e[0;31mFAIL: MicroPython dump failed for $1\e[0m"
        return
    fi

    OUT4=$($CPYTHON pickle_test.py --example_name "$1" --load)
    STATUS4=${PIPESTATUS[0]}
    OUT4_LAST_LINE=$(echo "$OUT4" | tail -n 1)

    if [ "$STATUS4" -ne 0 ]; then
        echo -e "\e[0;31mFAIL: CPython load failed for $1\e[0m"
        return
    fi

    rm -f dump.pkl
    echo "Output (MicroPython -> CPython): $OUT4_LAST_LINE"

    echo -e "\e[0;32mTest passed for $1\e[0m"
}

run_test "builtins-data-types"
run_test "custom-class"
run_test "numpy-ndarray"
