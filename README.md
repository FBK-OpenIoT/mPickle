# mPickle - Pickle for MicroPython <!-- omit in toc -->
The **mPickle (microPickle)** library offers a pure-Python implementation of Pickle, compatible with Protocol 5 (except for PickleBuffer), specifically design and adapted for MicroPython. It is adapted by the original CPython library, which can be found [here](https://github.com/python/cpython/blob/main/Lib/pickle.py).

## Table of contents <!-- omit in toc -->
- [Description](#description)
- [Setup](#setup)
  - [Deploy the code using `mpr` (`mpremote`)](#deploy-the-code-using-mpr-mpremote)
    - [Prerequisites](#prerequisites)
    - [Step-by-Step instructions](#step-by-step-instructions)
  - [Build a firmware with frozen module](#build-a-firmware-with-frozen-module)
- [Examples](#examples)
- [License](#license)
- [Reference](#reference)

## Description
mPickle is a pure-Python library for MicroPython that addresses the challenge of serializing and deserializing data on microcontrollers running MicroPython firmware. By enabling the transfer of Python objects in Pickle’s native binary format, it streamlines communication between MicroPython and standard Python environments. mPickle bridges the gap between IoT devices, edge computing, and the data science world, enabling efficient data transfer and analysis. This capability fosters collaboration among engineers, scientists, and data analysts, enabling seamless work on real-time data insights, model deployment, and data-driven solutions across diverse computing environments—all within a unified data language.

## Setup
To get started with mPickle, you have two options:
1. **Deploy the code directly to your board using `mpremote`.**
2. **Freeze/embed the mPickle code into the firmware installation.**


### Deploy the code using `mpr` (`mpremote`)
An alternative way to deploy mPickle is to use `mpr`, which allows you to upload the mPickle code directly to your board without modifying the firmware.

#### Prerequisites
1. **Install Python**: Make sure Python> 3.9 is installed on your system.
2. **Install mpremote**: Install `mpr` and `mpremote` using `pip`:
   ```sh
   pip install mpr mpremote
   ```
3. **Connect Your Board**: Connect the microcontroller board to your computer via USB.
4. **Identify Board Port**: Determine the serial port used by your board (e.g., `/dev/ttyUSB0` for Linux/macOS or `COM3` for Windows).

#### Step-by-Step instructions
1. **Navigate to the Project Directory**
   Move to the directory that contains the `src` folder:
   ```sh
   cd path/to/mPickle
   ```

2. **Upload Files Using `ampy`**
   Use the following command to upload the `src/mPickle/mpickle` folder to the board. This will create a directory named mpickle on the board:
   ```sh
   mpr -d <PORT> put -r src/mPickle/mpickle /
   ```

   - Replace `<PORT>` with the appropriate port for your board (e.g., `/dev/ttyUSB0` or `COM3`).
   - `src/mPickle/mpickle` is the path to the code folder.
   - `/` is the name of the destination on the board (the root). It will create the mpickle directory.

3. Install dependencies
   `mPickle` depends on `types` and `functools`, thus install them with the command:
   ```sh
   mpr -d <PORT> mip install types functools
   ```

4. **Confirm Upload**
   Once uploaded, you can list the files on your board using:
   ```sh
   mpr -d <PORT> ls
   ```
   You should see the `mpickle` folder in the output.

5. **Verify the deployment**
   If the deployment succeeds, mPickle will be available as module. You can confirm this by connecting to the MicroPython REPL with the command
   ```sh
   mpr -d <PORT> repl
   ```
   and running:
   ```python
   import mpickle
   ```
   or running
   ```sh
   mpr exec 'import mpickle; print(mpickle.__version__)'
   ```
   and it should print the version of the `mPickle` library.

### Build a firmware with frozen module
This repository includes a set of compilation scripts located in `firmware/dev-scripts`, to build a custom MicroPython firmware with mPickle as a frozen module, along with (`ulab`)[https://github.com/v923z/micropython-ulab]. 
These scripts support firmware compilation for ESP32 (and its variants) as well as UNIX.
For detailed compilation steps, refer to (this guide)[/firmware/dev-scripts/README.md].

Once the MicroPython has been compile, and eventually flashed, it is possible to check if everything is working by connecting to the MicroPython REPL and running:
```python
import mpickle
```
Or, if you have installed `mpr`, you can run
```sh
mpr exec 'import mpickle; print(mpickle.__version__)'
```
and it should print the version of the `mPickle` library.

## Examples
The mPickle project comes with a few examples available [here](/src/examples).

## License
You can read the license [HERE](/LICENSE).

## Reference
This library has been described in 
```
Put the citation
```