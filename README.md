# Synthetic Dataset Generator for Traffic Analysis

This readme file describes prerequisites and use cases of synthetic dataset generator. The generator implementation includes 3 scripts in Python programming language.

## Getting Started

For running the project on your computer, run this command:

```
$ git clone https://git.fit.vutbr.cz/xsvore01/IBP.git

```

### Prerequisites

It is necessary to install PIL and OpenCV library first.

### Installing

PIL - Python Image Library

```
$ pip install pil 

```
or

```
$ pip install Pillow

```

OpenCV, Numpy for Python

```
$ yum install numpy opencv*

```

How to import installed dependencies:

```
>>> from PIL import Image

```

```
>>> import cv2 

```

## Usage

First script generates synthetic license plates of 4 countries according to command line arguments and saves them to output directory:

```
$ python rzgenerator.py -i [amount] -o [output_dir_path='RZ/'] -t [nationality_shortcut]

```

### Use Cases

```
$ python rzgenerator.py -i 10000 -o license_plates_out/ -t cz
$ python rzgenerator.py -i 10000 -o license_plates_out/ -t sk
$ python rzgenerator.py -i 10000 -o license_plates_out/ -t pl
$ python rzgenerator.py -i 10000 -o license_plates_out/ -t h

```


Second script iterates the directory with automobile photos and user can easily set 4 corner coordinates of licesne plate on the picture and save them to textfile for further processing.

```
$ python clicker.py -i [src_path='photo_templates/']

```
### Controls

Mouse and Keyboard

After setting position by clicking mouse left button, change the position using keys W, A, S, D. Before confirming each point by key X, it's possible to remove last point using key Z. If all the points are set and saved, press ENTER to confirm their position. Then press ESC to continue.

```
Left Mouse Button - Set position

key W - Up
key A - Left
key S - Down
key D - Right
key Z - Step back
key X - Save
ENTER key - Confirm
ESC key - Next

```

### Use Case

```
$ python clicker.py -i photos/

```

Third script merges synthetic license plates with automobile photos.

```
$ python supertool.py -t [path_to_tmp='photo_templates2/'] -r [path_to_rz='RZ/'] -o [path_to_output='final/']

```

### Use Case

```
$ python supertool.py -t photos/ -r license_plates_out/ -o final_output

```


## Authors

* **Ondrej Svoreň** - *Bachelor Thesis* - [Git Repository](https://git.fit.vutbr.cz/xsvore01)