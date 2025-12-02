# mPickle - Setup <!-- omit in toc -->
To get started with mPickle, you have two options:

- [Deploy the code directly to your board using `mpr` (`mpremote`)](#deploy-the-code-directly-to-your-board-using-mpr-mpremote)
  - [Prerequisites](#prerequisites)
  - [Step-by-Step instructions](#step-by-step-instructions)
- [Build firmware with the mPickle module frozen (embedded)](#build-firmware-with-the-mpickle-module-frozen-embedded)

## Deploy the code directly to your board using `mpr` (`mpremote`)
An alternative way to deploy mPickle is to use `mpr`, which allows you to upload the mPickle code directly to your board without modifying the firmware.

### Prerequisites
1. **Install Python**: Make sure Python> 3.9 is installed on your system.
2. **Install mpremote**: Install `mpr` and `mpremote` using `pip`:
   ```sh
   pip install mpr mpremote
   ```
3. **Connect Your Board**: Connect the microcontroller board to your computer via USB.
4. **Identify Board Port**: Determine the serial port used by your board (e.g., `/dev/ttyUSB0` for Linux/macOS or `COM3` for Windows).

### Step-by-Step instructions
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

## Build firmware with the mPickle module frozen (embedded)
This repository includes a set of compilation scripts located in `firmware/dev-scripts`, to build a custom MicroPython firmware with mPickle as a frozen module, along with (ulab)[https://github.com/v923z/micropython-ulab]. 
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
