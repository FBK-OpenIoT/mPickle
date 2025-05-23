#!/bin/sh

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
# ESP32-compile-flash-ulab-mpickle.sh - Shell script to compile MicroPython
#                                       inside a Docker container and flash
#                                       ESP32 devices
#

. ./common.sh

BOARD=${1:-ESP32_GENERIC}
# build with 4 dimensions
MATRIX_DIMENSIONS=4

cd /mpy-compile/esp-idf
. ./export.sh
cd /mpy-compile/

cd /mpy-compile/micropython/ports/esp32
make submodules
cd /mpy-compile/

# Create the Makefile for the compilation
cat > "/mpy-compile/micropython/ports/esp32/makefile" <<EOL
BOARD = $BOARD
USER_C_MODULES = /mpy-compile/ulab/code/micropython.cmake
FROZEN_MANIFEST=/mpy-compile/modules/mPickle/manifest.py

CFLAGS += -DULAB_HAS_DTYPE_OBJECT=1
CFLAGS += -DULAB_MAX_DIMS=4

include Makefile
EOL

# Confirm the Makefile was created
if [ -f "/mpy-compile/micropython/ports/esp32/makefile" ]; then
    echo "Makefile successfully created at /mpy-compile/micropython/ports/esp32/makefile"
else
    echo "Failed to create Makefile!"
    exit 1
fi

cd /mpy-compile/micropython/ports/esp32
make
echo "Flashing..."
make deploy
cd /mpy-compile/
