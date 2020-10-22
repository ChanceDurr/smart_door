from tkinter import *
from tkinter import ttk
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

LARGE_FONT= ("Verdana", 12)

class Application(Tk):

    def __init__(self):
        Tk.__init__(self)
        container = Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainScreen, Passcode, FaceRecognition, RFID):
            
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky = "nsew")

        self.show_frame(MainScreen)
    def go_to(self, page):
        if page == 'MainScreen':
            new_page = MainScreen
        elif page == 'Passcode':
            new_page = Passcode
        elif page == 'FaceRecognition':
            new_page = FaceRecognition
        elif page == 'RFID':
            new_page = RFID
        else:
            print('Page Not Found')
            return 'Page Not Found'

        frame = 
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class MainScreen(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self,parent)

        label = Label(self, text="Chance's Room", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        # Send to first authentication frame
        button = Button(self, text="Unlock",
                            command=lambda: controller.show_frame(Passcode))
        button.pack()


class Passcode(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self,parent)

        self.controller = controller
        self.entry = []
        self.attempts = 0

        ttk.Label(self, text="Enter Code", font = ('Verdana', 32)).grid(row=0, column=0, sticky="n", pady=60)

        # Set location on warning text
        self.warnings = ttk.Label(self, text="", font=LARGE_FONT, foreground='red')
        self.warnings.grid(row=1, column=0, sticky='n')
        
        # Frame for the Keypad buttons
        keypad_frame = Frame(self)
        keypad_frame.grid(row=2, rowspan=4, column=0, sticky="eswn", padx=90, pady=20)
        
        # Keypad buttons
        Button(keypad_frame, text="7", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(7)).grid(row=0, column=0)
        Button(keypad_frame, text="8", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(8)).grid(row=0, column=1)
        Button(keypad_frame, text="9", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(9)).grid(row=0, column=2)
        Button(keypad_frame, text="4", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(4)).grid(row=1, column=0)
        Button(keypad_frame, text="5", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(5)).grid(row=1, column=1)
        Button(keypad_frame, text="6", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(6)).grid(row=1, column=2)
        Button(keypad_frame, text="1", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(1)).grid(row=2, column=0)
        Button(keypad_frame, text="2", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(2)).grid(row=2, column=1)
        Button(keypad_frame, text="3", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(3)).grid(row=2, column=2)
        Button(keypad_frame, text="0", font = ('Verdana', 20), height=3, width=4, command=lambda: self.entry_press(0)).grid(row=3, column=1)

    def entry_press(self, number):

        self.entry.append(number)

        if len(self.entry) >= 4:

            # Check for correct passcode
            if self.entry == [5, 5, 5, 5]:

                # If correct, reset values and change to next Frame
                self.entry = []
                self.attempts = 0
                self.warnings.configure(text='')
                self.controller.show_frame(RFID)

            else:
                # If incorrect, add warning label for remaining attempts
                self.warnings.configure(text=f"{3-self.attempts} attempts remaining")
                self.entry = []
                self.attempts += 1

                # If too many failed attempts reset values, remove warning, and send back to mainscreen
                if self.attempts > 3:
                    self.warnings.configure(text='')
                    self.attempts = 0
                    self.controller.show_frame(MainScreen)


class RFID(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self,parent)

        self.controller = controller

        title = Label(self, text="RFID Authentication", font=("Verdana", 32))
        title.grid(row=0, column=0, padx=20, pady=150)

        present = ttk.Label(self, text="Present RFID Card", font=("Verdana", 24))
        present.grid(row=1, column=0, padx=20)

        start = ttk.Button(self, text='Start', command=self.read_card)
        start.grid(row=2, column=0, padx=20)

        # Check for RFID, if card ID is same as mine, go to next page

    def read_card(self):
        reader = SimpleMFRC522()

        try:
            card_id = reader.read()[0]
        finally:
            GPIO.cleanup()

        if card_id == 584191377399:
            print('y')
            self.controller.show_frame(FaceRecognition)
        else:
            print('n')
            self.controller.show_frame(MainScreen)

class FaceRecognition(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self,parent)

        label = Label(self, text="FACE RECOG", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(MainScreen))
        button.pack()

        button2 = Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(MainScreen))
        button2.pack()


app = Application()
app.attributes("-fullscreen", True)
app.mainloop()