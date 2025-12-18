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
# lenet5_save_model_weights.py - Model weight saver
#           This script creates a LeNet-5 neural network with random weights and
#           saves them to a file using mPickle in MicroPython environments.

from lenet5.model import LeNet5
from lenet5.utils import save_weights_to_file, verify_weights_file
from lenet5.config import get_default_weights_path


def main():
    """Main function to save LeNet-5 model weights."""

    model_file = get_default_weights_path()

    # Initialize network
    print("Initializing LeNet-5 network with random weights...")
    model = LeNet5()
    
    # Print summary
    print(model.get_summary())
    
    # Storing weights
    print("Exporting model weights using mPickle...")
    
    # Save weights using mPickle under the hood
    if save_weights_to_file(model, model_file):
        # Verify by loading using mPickle under the hood
        verify_weights_file(model_file)
        print("\nExport completed successfully!")
        return True
    else:
        return False


if __name__ == "__main__":
    main()