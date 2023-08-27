import customtkinter
from cs50 import SQL
from CTkMessagebox import CTkMessagebox 


class NodeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Defining variables for the optionmenu input
        self.reaction_var = customtkinter.StringVar(value="Reaction")

        # Creating input elements
        self.label_1 = customtkinter.CTkLabel(self, text="X Coord.:")
        self.label_2 = customtkinter.CTkLabel(self, text="Y Coord.:")

        self.input_1 = customtkinter.CTkEntry(self)
        self.input_2 = customtkinter.CTkEntry(self)

        self.reaction = customtkinter.CTkOptionMenu(
            self, values=["None", "X", "Y", "XY"], variable=self.reaction_var
        )

        self.save = customtkinter.CTkButton(self, text="Save", command=self.save_node)

        # Display the input elements
        self.label_1.grid(row=0, column=0, padx=10, pady=10)
        self.label_2.grid(row=1, column=0, padx=10, pady=10)
        self.input_1.grid(row=0, column=1, padx=10, pady=10)
        self.input_2.grid(row=1, column=1, padx=10, pady=10)
        self.reaction.grid(row=2, column=1, padx=10, pady=10)
        self.save.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def save_node(self):
        print("Saving node...")
        x = self.input_1.get()
        y = self.input_2.get()
        r = self.reaction_var.get()

        if not x or not y or not r:
            CTkMessagebox(title="Info", message="Please fill all the input fields!!!")
        else:
            match(r):
                case "X":
                    rx = 1
                    ry = 0
                case "Y":
                    rx = 0
                    ry = 1
                case "XY":
                    rx = 1
                    ry = 1
                case _ :
                    rx = 0
                    ry = 0

            db = SQL("sqlite:///data.db")
            try:
                db.execute("INSERT INTO nodes (x, y, rx, ry) VALUES (?, ?, ?, ?);", x, y, rx, ry)
            except ValueError:
                # Show an error message
                CTkMessagebox(title="Error", message="Wrong input!!!", icon="cancel")

            self.clear()


    def clear(self):
        self.input_1.delete(0, customtkinter.END)
        self.input_2.delete(0, customtkinter.END)
        self.reaction_var.set("Reaction") 




class Node(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Creating a frame for entering the nodes parameters
        self.node_frame = NodeFrame(self)
        self.node_frame.grid(row=0, column=0, padx=0, pady=0)
