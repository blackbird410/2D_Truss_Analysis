import customtkinter
import sys
from nodes import *
from members import *
from loads import *


class OptionFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class ButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create GUI  buttons
        self.b_1 = customtkinter.CTkButton(self, text="Node", command=master.add_nodes)
        self.b_2 = customtkinter.CTkButton(
            self, text="Member", command=master.add_members
        )
        self.b_3 = customtkinter.CTkButton(self, text="Load", command=master.add_loads)
        self.b_4 = customtkinter.CTkButton(self, text="Analyze", command=master.analyze)
        self.b_5 = customtkinter.CTkButton(
            self, text="Results", command=master.get_results
        )
        self.b_6 = customtkinter.CTkButton(
            self, text="Deformations", command=master.show_deformation
        )
        self.b_7 = customtkinter.CTkButton(
            self, text="Exit", fg_color="red", command=master.exit
        )

        self.b_1.grid(row=0, column=0, padx=20, pady=10)
        self.b_2.grid(row=1, column=0, padx=20, pady=10)
        self.b_3.grid(row=2, column=0, padx=20, pady=10)
        self.b_4.grid(row=3, column=0, padx=20, pady=10)
        self.b_5.grid(row=4, column=0, padx=20, pady=10)
        self.b_6.grid(row=5, column=0, padx=20, pady=10)
        self.b_7.grid(row=6, column=0, padx=20, pady=10)

    def button_callback(self):
        print("Button pressed")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("2D Truss Analysis")
        self.geometry("950x350")

        # Create the frame of the buttons
        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=0, column=0, padx=10, pady=10)

        # Creating a frame for the canvas
        self.canvas = customtkinter.CTkCanvas(self, width="420", bg="lightgrey")
        self.canvas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.canvas.columnconfigure(0, weight=1)

        # Creating a frame for the options
        self.option_frame = OptionFrame(self)
        self.option_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        # self.option_frame.configure(fg_color="transparent")
        self.rowconfigure(index=2, weight=1)

    def destroy_frame(self):
        """Remove the widget in the third column of the main window for adding new ones."""

        for widget in self.option_frame.winfo_children():
            widget.destroy()
        return 0

    def add_nodes(self):
        self.destroy_frame()
        node_frame = Node(self.option_frame)
        node_frame.grid(row=0, column=1, padx=10, pady=10)

    def add_members(self):
        self.destroy_frame()
        member_frame = Member(self.option_frame)
        member_frame.grid(row=0, column=1, padx=10, pady=10)

    def add_loads(self):
        self.destroy_frame()
        load_frame = Load(self.option_frame)
        load_frame.grid(row=0, column=1, padx=10, pady=10)

    def analyze(self):
        self.destroy_frame()

    def get_results(self):
        self.destroy_frame()

    def show_deformation(self):
        self.destroy_frame()

    def exit(self):
        sys.exit("Program terminated...")


def create_gui():
    app = App()
    app.mainloop()
