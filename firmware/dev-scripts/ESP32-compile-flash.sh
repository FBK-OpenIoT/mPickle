#!/bin/bash

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
# ESP32-compile-flash.sh - Shell script to compile MicroPython for ESP32 devices
#


set -euo pipefail

BUILD=false
BOARD="ESP32_GENERIC"
VARIANT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build_img)
      BUILD=true
      shift
      ;;
    --board)
      BOARD="${2:-}"; shift 2
      ;;
    --variant)
      VARIANT="${2:-}"; shift 2
      ;;
    --board=*)
      BOARD="${1#*=}"; shift
      ;;
    --variant=*)
      VARIANT="${1#*=}"; shift
      ;;
    -h|--help)
      echo "Usage: $0 [--build_img] [--board <name>] [--variant <name>]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

# Build the Docker image if requested or if not already present
if $BUILD || ! $(docker image ls | grep -q "mpy-compile"); then
    echo "building docker image"
    docker build docker -t mpy-compile
fi

# Run the compilation and flashing inside the Docker container
docker run \
    --privileged \
    --rm \
    -it \
    -v /media/$(whoami):/media \
    -v $(realpath "$(pwd)/../../src/mPickle"):/mpy-compile/modules/mPickle \
    mpy-compile /mpy-compile/ESP32-compile-flash-ulab-mpickle.sh $BOARD
