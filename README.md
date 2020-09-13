# Digit Recognition
# First edition
## Overview

The program opens a window in which the user can draw and the program captures the digit drawn by the user and predicts the drawn digit.


## Open Source Model
Python Library: 
1. Opencv
2. Keras
3. Tkinter
4. Numpy
5. Pyscreenshot
6. Tensorflow 

## Design

The project is written in python file.

## Procedure for running:

            1.python Digit_Recognition.py 

            2. There are 5 buttons
                    a. Pen button - To draw, by default active
			b. Color button - To choose color
			c. Size button - To choose the pen or eraser size
			d. Eraser button - To activate the eraser
			e. Reset button - To clear the canvas
			f. Predict button - To predict the digit drawn

            3. Using tkinter for creating a Graphic User Interface

            4. Use Pyscreenshot to capture the canvas as image

            5. Use the trained model(trained on MNIST data using tensorflow) using the keras load model to predict the digit

            5. Press the red cross button to close the window

## Important file

Digit_Recognition.py
Digit_Recogniton_Model_2.model

## Report

The first edition is doing good when the user draws the digit neatly. The accuracy of prediction is 97% .

## Need Update

The project is only the first edition. we will keep update.
