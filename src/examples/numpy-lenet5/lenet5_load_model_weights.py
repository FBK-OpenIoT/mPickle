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
# lenet5_load_model_weights.py - Model weight loader
#           This script loads pre-trained weights into a LeNet-5 neural network
#           using the mPickle library for deserialization in MicroPython and
#           displays the model summary.
#


from lenet5.model import LeNet5
from lenet5.utils import load_weights_from_file
from lenet5.config import get_default_weights_path


def main():
    """Main function to load LeNet-5 model weights."""
    
    print("Initializing LeNet-5 network...")
    model = LeNet5()

    # Load weights using mPickle
    load_weights_from_file(model, get_default_weights_path())
    
    print("\nLoad completed successfully!")

    print(model.get_summary())

    return True


if __name__ == "__main__":
    main()