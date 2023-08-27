import customtkinter
from nodes import *
from members import *
from loads import *



class ButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create GUI  buttons
        self.b_1 = customtkinter.CTkButton(self, text="Node", command=self.add_nodes)
        self.b_2 = customtkinter.CTkButton(self, text="Member", command=self.add_members)
        self.b_3 = customtkinter.CTkButton(self, text="Load", command=self.add_loads)
        self.b_4 = customtkinter.CTkButton(self, text="Analyze", command=self.analyze)
        self.b_5 = customtkinter.CTkButton(self, text="Results", command=self.get_results)
        self.b_6 = customtkinter.CTkButton(self, text="Deformations", command=self.show_deformation)
        
        self.b_1.grid(row=0, column=0, padx=20, pady=10)
        self.b_2.grid(row=1, column=0, padx=20, pady=10)
        self.b_3.grid(row=2, column=0, padx=20, pady=10)
        self.b_4.grid(row=3, column=0, padx=20, pady=10)
        self.b_5.grid(row=4, column=0, padx=20, pady=10)
        self.b_6.grid(row=5, column=0, padx=20, pady=10)


    def add_nodes(self):
        print("Adding nodes")
        create_gui("Node")


    def add_members(self):
        print("Adding members")
        create_gui("Member")
    
    
    def add_loads(self):
        print("Adding loads")
        create_gui("Load")

    
    def analyze(self):
        print("Analyzing")

    
    def get_results(self):
        print("Showing results")


    def show_deformation(self):
        print("Showing deformations")


    def button_callback(self):
        print("Button pressed")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("2D Truss Analysis")
        self.geometry("700x320")

        # Create the frame of the buttons
        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=0, column=0, padx=10, pady=10)
    

def create_gui(s="App"):
    match(s):
        case "Node":
            app_node = Node()
            app_node.mainloop()
        case "Member":
            app_member = Member()
            app_member.mainloop()    
        case "Load":
            app_load = Load()
            app_load.mainloop()
        case _:
            app = App()
            app.mainloop()
