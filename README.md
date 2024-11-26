# mPickle - Pickle for MicroPython <!-- omit in toc -->
The **mPickle (microPickle)** library offers a pure-Python implementation of Pickle, compatible with Protocol 5 (except for ), specifically design and adapted for MicroPython. It is adapted by the original CPython library, which can be found [here](https://github.com/python/cpython/blob/main/Lib/pickle.py).

## Table of contents <!-- omit in toc -->
- [Description](#description)
- [Setup](#setup)
  - [1. Code Freezed into Firmware](#1-code-freezed-into-firmware)
    - [Step-by-Step instructions](#step-by-step-instructions)
  - [Deploy the code using `ampy`](#deploy-the-code-using-ampy)
    - [Prerequisites](#prerequisites)
    - [Step-by-Step Deployment](#step-by-step-deployment)
- [Examples](#examples)
- [License](#license)
- [Reference](#reference)

## Description
mPickle is a pure-Python library for MicroPython that addresses the challenge of serializing and deserializing data on microcontrollers running MicroPython firmware. By enabling the transfer of Python objects in Pickle’s native binary format, it streamlines communication between MicroPython and standard Python environments. mPickle bridges the gap between IoT devices, edge computing, and the data science world, enabling efficient data transfer and analysis. This capability fosters collaboration among engineers, scientists, and data analysts, enabling seamless work on real-time data insights, model deployment, and data-driven solutions across diverse computing environments—all within a unified data language.

## Setup
TTo get started with mPickle, you have two options:
1. **Freeze/embed the mPickle code into the firmware installation.**
2. **Deploy the code directly to your board using `ampy`.**

### 1. Code Freezed into Firmware

The mPickle repository includes a compilation tool called `mpy-helper`, which helps build custom MicroPython firmware that includes the mPickle module. This tool is available in the path `firmware/dev-scripts/generic/` and it helps in building the MicroPython firmware for many different targets like ESP32, Unix, ARM, etc.

Using the `mpy-helper` tool, you can build the MicroPython firmware for many different targets, such as ESP32, Unix, ARM, etc.

To embed mPickle into the firmware, follow these steps:

#### Step-by-Step instructions

1. **Move to the Compilation Tool Directory**

   Change your working directory to the location of `mpy-helper`:
   ```sh
   cd firmware/dev-scripts/generic
   ```
2. **Install Requirements (First-Time Setup Only)**

   If this is your first time using mpy-helper, you will need to follow the installation procedure outlined in the [README](firmware/dev-scripts/generic/README.md#installation) file.

3. **Add mPickle to Modules for Firmware**

   Copy the mPickle code into the `modules/user_mp_modules/include/` directory:
   ```sh
   cp -r ../../../src/mPickle ./modules/user_mp_modules/include/
   ```
4. **Compile the Firmware**

   Use the `mpy-helper` tool to compile the firmware, specifying your target. For example, to compile for ESP32-S3:

   ```sh
   ./mpy-helper build ESP32_GENERIC_S3
   ```

   The `ESP32_GENERIC_S3` target is just an example; replace it with your desired target board (e.g., `UNIX`, `ESP32_GENERIC`, `RPI_PICO_W`, `ARDUINO_NICLA_VISION`, `STM32L496GDISC`, etc.).

5. **Flash the Firmware**
   Use the `mpy-helper` tool to flash the firmware, specifying your target. For example, to flash a ESP32-S3 on port `<PORT>`:

   ```sh
   ./mpy-helper flash ESP32_GENERIC_S3 PORT=<PORT>
   ```

   The `ESP32_GENERIC_S3` target is just an example; replace it with your desired target board (e.g., `UNIX`, `ESP32_GENERIC`, `RPI_PICO_W`, `ARDUINO_NICLA_VISION`, `STM32L496GDISC`, etc.) and the right `<PORT>`.

6. **Verify Installation**
   If the compilation succeeds, mPickle will be embedded in the new firmware. You can confirm this by connecting to the MicroPython REPL and running:
   ```python
   import mpickle
   ```

**Removing mPickle from Firmware**
If you decide to remove mPickle from the firmware in the future, run the following command and then compile again:
```sh
./mpy-helper ignore mPickle
```
If you want to re-include mPickle into the firmware, run the following command and then compile again:
```sh
./mpy-helper include mPickle
```

### Deploy the code using `ampy`
An alternative way to deploy mPickle is to use `ampy`, which allows you to upload the mPickle code directly to your board without modifying the firmware.

#### Prerequisites
1. **Install Python**: Make sure Python> 3.9 is installed on your system.
2. **Install ampy**: Install `ampy` using `pip`:
   ```sh
   pip install adafruit-ampy
   ```
3. **Connect Your Board**: Connect the microcontroller board to your computer via USB.
4. **Identify Board Port**: Determine the serial port used by your board (e.g., `/dev/ttyUSB0` for Linux/macOS or `COM3` for Windows).

#### Step-by-Step Deployment
1. **Navigate to the Project Directory**
   Move to the directory that contains the `src` folder:
   ```sh
   cd path/to/mPickle
   ```

2. **Upload Files Using `ampy`**
   Use the following command to upload the src/mPickle/mpickle folder to the board. This will create a directory named mpickle on the board:
   ```sh
   ampy --port <PORT> put src/mPickle/ mPickle
   ```

   - Replace `<PORT>` with the appropriate port for your board (e.g., `/dev/ttyUSB0` or `COM3`).
   - `src/mPickle/mpickle` is the path to the code folder.
   - `mpickle` is the name of the destination directory on the board (the name of the module).

3. **Confirm Upload**
   Once uploaded, you can list the files on your board using:
   ```sh
   ampy --port <PORT> ls
   ```
   You should see the `mpickle` folder in the output.

6. **Verify the deployment**
   If the deployment succeeds, mPickle will be available as module. You can confirm this by connecting to the MicroPython REPL and running:
   ```python
   import mpickle
   ```

## Examples
The mPickle project comes with a few examples available [here](/examples).

## License
You can read the license [HERE](/LICENSE).

## Reference
This library has been described in 
```
Put the citation
```