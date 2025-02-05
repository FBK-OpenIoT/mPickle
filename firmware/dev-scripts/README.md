# Firmware compilation scripts
A collection of scripts, built around a Docker container for compilation, enables quick and efficient building and flashing of MicroPython firmware for various boards, including:
- UNIX
- ESP32
The resulting firmware (or interpreter, in the case of UNIX) integrates (`mPickle`)[/] and (`ulab`)[https://github.com/v923z/micropython-ulab], along with their dependencies, directly into the binary.


## Table of Contents  <!-- omit in toc -->
- [Firmware compilation scripts](#firmware-compilation-scripts)
  - [License](#license)
  - [Preliminaries](#preliminaries)
  - [Build MicroPython for `UNIX`](#build-micropython-for-unix)
  - [Build MicroPython for `ESP32` devices](#build-micropython-for-esp32-devices)

## License
You can read the license [HERE](/LICENSE).

## Preliminaries
The only prerequisite for using the scripts in this directory is Docker, which will run the compilation container. To install Docker, follow the instructions here:
    - Windows: (official Docker documentation)[https://docs.docker.com/desktop/setup/install/windows-install/].
    - macOS: (official Docker documentation)[https://docs.docker.com/desktop/setup/install/mac-install/].
    - Linux: (official Docker documentation)[https://docs.docker.com/engine/install/].

Once Docker is installed, you can proceed with using the provided scripts to build and flash your custom MicroPython firmware.

## Build MicroPython for `UNIX`
To run MicroPython on `UNIX`, execute the following script:
```sh
./UNIX-compile.sh
```
If the Docker container for compilation does not already exist, the script will create it first. It will then compile the MicroPython interpreter and place the output in the `output/`.
Once the compilation is complete, you can launch the interpreter by running:
```sh
./output/micropython
```

## Build MicroPython for `ESP32` devices
To run MicroPython on an `ESP32` device, execute the following script:
```sh
./ESP32-compile-flash.sh
```
If the Docker container for compilation does not already exist, the script will create it first. It will then **compile** the MicroPython firmware and **flash** it to the connected USB device.
You can specify the target board type by passing the `BOARD` argument to the command:
```sh
./ESP32-compile-flash.sh BOARD
```
The available BOARD values can be found (here)[https://github.com/micropython/micropython/tree/master/ports/esp32/boards].
Once the flashing process is complete, you can connect to the MicroPython REPL using:
```sh
mpremote
```