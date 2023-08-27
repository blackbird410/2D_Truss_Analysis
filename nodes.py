import customtkinter


class NodeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Defining variables for the optionmenu input
        self.reaction_var = customtkinter.StringVar(value="Reaction")

        # Creating input elements
        self.label_1 = customtkinter.CTkLabel(self, text="X Coord.:")
        self.label_2 = customtkinter.CTkLabel(self, text="Y Coord.:")

        self.input_1 = customtkinter.CTkEntry(self, placeholder_text="10")
        self.input_2 = customtkinter.CTkEntry(self, placeholder_text="10")

        self.reaction = customtkinter.CTkOptionMenu(self, values=["None", "X", "Y", "XY"], 
                                                    variable=self.reaction_var)

        self.save = customtkinter.CTkButton(self, text="Save", command=self.save_node)

        # Display the input elements
        self.label_1.grid(row=0, column=0, padx=10, pady=10)
        self.label_2.grid(row=1, column=0, padx=10, pady=10)
        self.input_1.grid(row=0, column=1, padx=10, pady=10)
        self.input_2.grid(row=1, column=1, padx=10, pady=10)
        self.reaction.grid(row=0, column=3, rowspan=2, padx=10, pady=10)
        self.save.grid(row=2, column=0, columnspan=3, padx=10, pady=10)


    def save_node(self):
        print("Saving node...")
        x = self.input_1.get()
        y = self.input_2.get()
        r = self.reaction_var.get()
        print(f"X: {x} | Y: {y} | Reaction: {r}")


class Node(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # self.title("Nodes")
        # self.geometry("450x200")

        # Creating a frame for entering the nodes parameters
        self.node_frame = NodeFrame(self)
        self.node_frame.grid(row=0, column=0, padx=10, pady=10)

        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)