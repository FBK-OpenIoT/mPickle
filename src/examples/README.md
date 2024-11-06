# About the examples

These examples are meant to showcase the usage of pickle and mpickle on cpython and micropython respectively. As such, each `example.py` file can be run on either implementation

## How to run

Along with this file, there is a number of folders representing the python types and classes that will be pickled/unpickled in the respective example; in each folder, a file named `example.py` can be found. While in the desired folder, running

        $PYTHON -i example.py

will start the python REPL and import the file for you. All you need to do is call the `example()` funciton

in some cases, such as for the [built-in datatypes](builtins-data-types), you can provide a list as an argument to the function, and it will try to pickle the objects in your list rather than the predefined one