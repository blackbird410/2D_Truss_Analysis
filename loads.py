import customtkinter
from cs50 import SQL
from CTkMessagebox import CTkMessagebox 


class LoadFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Creating input elements
        self.label_1 = customtkinter.CTkLabel(self, text="Node No:")
        self.label_2 = customtkinter.CTkLabel(self, text="X Load:")
        self.label_3 = customtkinter.CTkLabel(self, text="Y Load:")

        self.input_1 = customtkinter.CTkEntry(self)
        self.input_2 = customtkinter.CTkEntry(self)
        self.input_3 = customtkinter.CTkEntry(self)

        self.save = customtkinter.CTkButton(self, text="Save", command=self.save_load)

        # Display the input elements
        self.label_1.grid(row=0, column=0, padx=10, pady=10)
        self.label_2.grid(row=1, column=0, padx=10, pady=10)
        self.label_3.grid(row=2, column=0, padx=10, pady=10)

        self.input_1.grid(row=0, column=1, padx=10, pady=10)
        self.input_2.grid(row=1, column=1, padx=10, pady=10)
        self.input_3.grid(row=2, column=1, padx=10, pady=10)

        self.save.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def save_load(self):
        print("Saving load ...")
        n = self.input_1.get()
        x = self.input_2.get()
        y = self.input_3.get()
        
        db = SQL("sqlite:///data.db")
        try:
            db.execute("""INSERT INTO loads (x_load, y_load, node) VALUES (?, ?, ?);""", x, y, n)
        except ValueError:
            CTkMessagebox(title="Error", message="Wrong imput!!!", icon="cancel")
        self.clear()


    def clear(self):
        self.input_1.delete(0, customtkinter.END)
        self.input_2.delete(0, customtkinter.END)
        self.input_3.delete(0, customtkinter.END)



class Load(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Creating frame for entering loads parameters
        self.load_frame = LoadFrame(self)
        self.load_frame.grid(row=0, column=0, padx=0, pady=0)
