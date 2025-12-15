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
if [ -n "$2" ]; then
   BOARD_VARIANT="-${2}"
fi
# build with 4 dimensions
MATRIX_DIMENSIONS=4
PORT_DIR=esp32
BOARD_DIR=$PORT_DIR/boards/$BOARD

# Load ESP-IDF environment
. $IDF_PATH/export.sh

# Configure build with ulab and mPickle frozen modules
USER_C_MODULES=/mpy-compile/ulab/code/micropython.cmake
MPICKLE_FROZEN_MANIFEST=/mpy-compile/modules/mPickle/manifest.py
FROZEN_MANIFEST=/mpy-compile/manifest.py

echo "include(\"$MPICKLE_FROZEN_MANIFEST\")" >> $FROZEN_MANIFEST

if [ -f /mpy-compile/micropython/ports/$BOARD_DIR/manifest.py ]; then
    echo "include(\"/mpy-compile/micropython/ports/$BOARD_DIR/manifest.py\")" >> $FROZEN_MANIFEST
elif [ -f /mpy-compile/micropython/ports/$PORT_DIR/boards/manifest.py ]; then
    echo "include(\"/mpy-compile/micropython/ports/$PORT_DIR/boards/manifest.py\")" >> $FROZEN_MANIFEST
fi

# Extra compilation flags for ulab
EXTRA_FLAGS="-DULAB_HAS_DTYPE_OBJECT=1 -DULAB_MAX_DIMS=${MATRIX_DIMENSIONS}"

# Build MicroPython firmware
cd /mpy-compile/micropython/ports/esp32
# IDF_FLAGS="-D MICROPY_BOARD=$BOARD -D MICROPY_BOARD_DIR=/mpy-compile/micropython/ports/esp32/boards/$BOARD -D USER_C_MODULES=$USER_C_MODULES  -DCMAKE_C_FLAGS="$EXTRA_FLAGS" -DCMAKE_CXX_FLAGS="$EXTRA_FLAGS""
IDF_FLAGS="-D MICROPY_BOARD=$BOARD -D MICROPY_BOARD_DIR=/mpy-compile/micropython/ports/esp32/boards/$BOARD -D USER_C_MODULES=$USER_C_MODULES -D MICROPY_FROZEN_MANIFEST=$FROZEN_MANIFEST -DCMAKE_C_FLAGS="$EXTRA_FLAGS" -DCMAKE_CXX_FLAGS="$EXTRA_FLAGS""
[ -n "$BOARD_VARIANT" ] && IDF_FLAGS="$IDF_FLAGS -DMICROPY_BOARD_VARIANT=${BOARD_VARIANT#'-'}"

make -j $(nproc) BOARD=$BOARD submodules
BUILD=/mpy-compile/micropython/ports/esp32/build-$BOARD$BOARD_VARIANT
mkdir -p $BUILD

cmake -S . -B $BUILD $IDF_FLAGS  -GNinja
ninja -j $(nproc) -C $BUILD
python3 makeimg.py \
   $BUILD/sdkconfig \
   $BUILD/bootloader/bootloader.bin \
   $BUILD/partition_table/partition-table.bin \
   $BUILD/micropython.bin \
   $BUILD/firmware.bin \
   $BUILD/micropython.uf2

# Flash firmware to the device
cd $BUILD
esptool.py erase_flash
esptool.py write_flash $(cat flash_args)

echo "Flashing completed!"
# End of script
 