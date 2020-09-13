from tkinter import * #To do various operations on canvas and develop a GUI
from tkinter.colorchooser import askcolor #Allows user to choose drawing color
from tkinter import messagebox #To display result in a messagebox
import pyscreenshot as ImageGrab #To save the input on canvas as a image
import cv2 #Read the canvas image and process it
import tensorflow as tf #Load the trained model
import numpy as np #Handle predictions using function argmax


class DigitRecognizer(object):  #The main class

    DEFAULT_PEN_SIZE= 40 #If user does not select pen size
    DEFAULT_COLOR = 'black' #If user does not select pen color

    def __init__(self): #class init method or constructor
        self.root=Tk() #create a root widget which is a window
        self.root.geometry("600x600") #Set the dimensions of the window
        self.root.title("Digit Recognizer")  #Set the title of the window


        self.pen_button= Button(self.root, text='Pen', command=self.use_pen)  #Initialize pen button
        self.pen_button.grid(row=0, column=6) #Select where to place the widget

        self.color_button= Button(self.root, text='Color' ,command=self.choose_color) #Initialize color button
        self.color_button.grid(row=1, column=6)  #Select where to place the widget

        self.eraser_button= Button(self.root, text='Eraser' ,command=self.use_eraser)  #Initialize eraser button
        self.eraser_button.grid(row=2, column=6) #Select where to place the widget

        self.choose_size_button = Scale(self.root, from_=40, to=50, orient=HORIZONTAL)  #Initialize size button
        self.choose_size_button.grid(row=3, column=6) #Select where to place the widget

        self.predict_button =Button(self.root, text='Predict' ,command=self.predict_digit)  #Initialize predict button
        self.predict_button.grid(row=6, column=1) #Select where to place the widget

        self.reset_button= Button(self.root, text='Reset' ,command=self.reset)  #Initialize resize button
        self.reset_button.grid(row= 6, column=4) #Select where to place the widget

        self.c = Canvas(self.root, bg='white', height=500, width=500) # Setup a canvas
        self.c.grid(row=0, column=0, rowspan=5, columnspan=5) #Select where to place the widget

        self.setup() # Function to setup the coordinates, active button, eraser mode, and bind the events with the functions
        self.root.mainloop() # mainloop for diplaying the window until user closes it

    def setup(self):
        self.old_x= None #Initialize x coordinate
        self.old_y = None #Initialize y coordinate
        self.line_width= self.choose_size_button.get() #Initialize the line width using get function from the size button
        self.color= self.DEFAULT_COLOR # Set color
        self.eraser_on = False #By default the eraser is off
        self.active_button= self.pen_button #By default the active button is the pen button
        self.c.bind("<Button-1>",self.addpoint) #when user presses the left button of the mouse, function addpoint is invoked
        self.c.bind('<B1-Motion>', self.draw) #invokes draw function when user drags the mouse while the left mouse button is pressed
        # The above two are events that are mapped to some function

    def activate_button(self, button, eraser_mode=False): #Defines property of the active button
        self.active_button.config(relief= RAISED) #The already active button should be raised
        button.config(relief= SUNKEN) #The newly active button should be sunken
        self.active_button =button #The newly active button becomes the active button
        self.eraser_on = eraser_mode #sets the eraser mode to True if argument is passed else by default False

    def save(self): #To save the canvas image
        x = self.root.winfo_rootx() + self.c.winfo_x() #winfo_rootx() returns x coordinate of upper left corner of this widget on the root window.
        y = self.root.winfo_rooty() + self.c.winfo_y() #winfo_rooty() returns  coordinate of upper left corner of this widget on the root window.
        x1 = x + self.c.winfo_width() #winfo_width() returns the width of this widget.
        y1 = y + self.c.winfo_height() #winfo_height() returns the height of this widget.
        im = ImageGrab.grab((x, y, x1, y1)) #This method takes a snapshot of the screen according to the given pixels
        #here x,y are the starting points(left corner) and x1,y1 are the end points of capture(right bottom corner)
        im.save("test_images/captured.png") #specify the path and format of the image to be saved
        return im
        #return the image so that none is not returned


    def addpoint(self,event): #function to be mapped with the event
        self.old_x= event.x #when the user clicks on the canvas, by default NONE value of old_x is replaced by the x coordinate where the user has pressed
        self.old_y= event.y #when the user clicks on the canvas, by default NONE value of old_x is replaced by the y coordinate where the user has pressed

    def use_pen(self):
        self.activate_button(self.pen_button)#activates the pen button

    def choose_color(self):
        self.eraser_on=False
        self.color=askcolor(color=self.color)[1] #The user can choose from different RGB shades

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True) #activate eraser

    def predict_digit(self):
        self.activate_button(self.predict_button) #activate the button
        self.save() #save the input on the canvas to a image
        self.predicted_digit= self.prediction() #call the prediction function
        messagebox.showinfo("Digit","You drew :-"+ str(self.predicted_digit)) #Display the output in a messagebox

    def prediction(self):
        image = cv2.imread('test_images/captured.png') #read the saved input on canvas which is stores as image
        grey = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY) #convert to grayscale
        ret, thresh = cv2.threshold(grey.copy(), 75, 255, cv2.THRESH_BINARY_INV) #threshold the image for contouring
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #find contours on threshold image
        preprocessed_digits=[] #empty list to add processed images
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)

            # Creating a rectangle around the digit in the original image (for displaying the digits fetched via contours)
            cv2.rectangle(image, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

            # Cropping out the digit from the image corresponding to the current contours in the for loop
            mean = w + h
            mean = mean / 2
            if (w > h):
                m = abs(mean - h)
                height = int(y + h + m)
                width = int(x + w - m)
                digit = thresh[y:height, x:width]
            elif (h > w):
                m = abs(mean - w)
                height = int(y + h - m)
                width = int(x + w + m)
                digit = thresh[y:height, x:width]
            elif (h == w):
                digit = thresh[y:y + h, x:x + w]

            # ResiImport the libraries to create a GUI Applicationzing that digit to (18, 18)
            resized_digit = cv2.resize(digit, (18, 18))

            # Padding the digit with 5 pixels of black color (zeros) in each side to finally produce the image of (28, 28)
            padded_digit = np.pad(resized_digit, ((5, 5), (5, 5)), "constant", constant_values=0)

            # Adding the preprocessed digit to the list of preprocessed digits
            preprocessed_digits.append(padded_digit)

        model = tf.keras.models.load_model('Digit_Recognition_Model_2.model') #Load our trained model
        for digit in preprocessed_digits:
            prediction = model.predict(digit.reshape(1, 28, 28, 1)) #Predict the digit using our model after reshaping the digit to the dimensions the model is trained on
            self.ans=np.argmax(prediction )#convert the predicted array to a readable format
        return self.ans
        #return the predicted value

    def reset(self): #reset the canvas
        self.c.delete("all") #Deletes 'all' drawn input on the canvas

    def draw(self, event): #the draw or paint function
        self.line_width=self.choose_size_button.get() #select the line width for drawing
        draw_color= 'white' if self.eraser_on else self.color #If ereser mode is True then paint white(to erase) else paint according to the selected color
        if self.old_x and self.old_y: #if the old-x old-y are true and not NONE i.e. the user has pressed on the canvas
            self.c.create_line((self.old_x, self.old_y, event.x, event.y), width=self.line_width,
                               fill=draw_color,capstyle=ROUND,smooth=True,splinesteps=0) #draw line from old_x, old_y points to the points where the user left the dragging
            self.old_x=event.x #to replace the old coordinates with the coordinates where the user left the mouse dragging
            self.old_y=event.y #to replace the old coordinates with the coordinates where the user left the mouse dragging

if __name__ == '__main__':
    DigitRecognizer()
#Before executing code, Python interpreter reads source file and define few special variables/global variables.
#If the python interpreter is running that module (the source file) as the main program, it sets the special
# __name__ variable to have a value “__main__”. If this file is being imported from another module,
# __name__ will be set to the module’s name. Module’s name is available as value to __name__ global variable.
#Here our class DigitRecognizer script is being used as a module so its __name__ is __main__







