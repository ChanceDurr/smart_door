from tkinter import *
from tkinter import ttk
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C

# RFID Reader setup
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)
pn532.SAM_configuration()

class Application(Tk):

    def __init__(self):

        Tk.__init__(self)

        self.entry = []
        self.attempts = 0
        self.uid = ''

        self.title("Testing")
        
        self.label = Label(self, text="This is our first GUI!")
        self.label.grid(row=0, column=0, padx=150)

        self.button = Button(self, text="Go to another screen", command=self.passcode_screen)
        self.button.grid(row=1, column=0, padx=150)

    def passcode_screen(self):

        passcode_window = Toplevel(self)
        passcode_window.title('Passcode')
        passcode_window.attributes('-fullscreen', True)

        ttk.Label(passcode_window, text="Enter Code", font = ('Verdana', 32)).grid(row=0, column=0, sticky="n", pady=60)

        # Set location on warning text
        self.warnings = ttk.Label(passcode_window, text="", font=('Verdana', 12), foreground='red')
        self.warnings.grid(row=1, column=0, sticky='n')
        
        # Frame for the Keypad buttons
        keypad_frame = Frame(passcode_window)
        keypad_frame.grid(row=2, rowspan=4, column=0, sticky="eswn", padx=90, pady=20)
        
        # Keypad buttons
        Button(keypad_frame, text="7", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(7, passcode_window)).grid(row=0, column=0)
        Button(keypad_frame, text="8", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(8, passcode_window)).grid(row=0, column=1)
        Button(keypad_frame, text="9", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(9, passcode_window)).grid(row=0, column=2)
        Button(keypad_frame, text="4", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(4, passcode_window)).grid(row=1, column=0)
        Button(keypad_frame, text="5", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(5, passcode_window)).grid(row=1, column=1)
        Button(keypad_frame, text="6", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(6, passcode_window)).grid(row=1, column=2)
        Button(keypad_frame, text="1", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(1, passcode_window)).grid(row=2, column=0)
        Button(keypad_frame, text="2", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(2, passcode_window)).grid(row=2, column=1)
        Button(keypad_frame, text="3", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(3, passcode_window)).grid(row=2, column=2)
        Button(keypad_frame, text="0", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(0, passcode_window)).grid(row=3, column=1)

    def rfid_screen(self):

        rfid_window = Toplevel(self)
        rfid_window.title('RFID Authentication')
        rfid_window.attributes('-fullscreen', True)

        Label(rfid_window, text='Present RFID', font=('Verdana', 38)).grid(row=0, column=0, padx=70, pady=50)

        self.after(1, self.rfid_check)

        print('test')
        print(self.uid)

    def face_recog(self):

        face_recog_window = Toplevel(self)
        face_recog_window.title('Facial Recognition')
        face_recog_window.attributes('-fullscreen', True)

        Label(face_recog_window, text='Place Holder looking ass text').grid(row=0, column=0)


    def rfid_check(self):

        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)

            # Try again if no card is available.
            if uid is not None:
                break

        self.uid = ''.join([str(x) for x in uid])


    # Function for passcode key presses
    def entry_press(self, number, window):

        self.entry.append(number)

        if len(self.entry) >= 4:

            # Check for correct passcode
            if self.entry == [5, 5, 5, 5]:

                # If correct, reset values and change to rfid window
                self.entry = []
                self.attempts = 0
                self.warnings.configure(text='')
                window.destroy()
                self.rfid_screen()

            else:
                # If incorrect, add warning label for remaining attempts
                self.warnings.configure(text=f"{3-self.attempts} attempts remaining")
                self.entry = []
                self.attempts += 1

                # If too many failed attempts reset values, remove warning, and send back to mainscreen
                if self.attempts > 3:
                    self.warnings.configure(text='')
                    self.attempts = 0
                    window.destroy()



app = Application()
app.attributes("-fullscreen", True)
app.mainloop()