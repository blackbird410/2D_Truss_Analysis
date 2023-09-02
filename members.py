import customtkinter
from cs50 import SQL
from CTkMessagebox import CTkMessagebox


class MemberFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Creating input elements
        self.label_1 = customtkinter.CTkLabel(self, text="Start node:")
        self.label_2 = customtkinter.CTkLabel(self, text="End node:")
        self.label_3 = customtkinter.CTkLabel(self, text="Section Area:")
        self.label_4 = customtkinter.CTkLabel(self, text="Young Modulus:")
        self.label_5 = customtkinter.CTkLabel(self, text="Inertia")

        self.input_1 = customtkinter.CTkEntry(self)
        self.input_2 = customtkinter.CTkEntry(self)
        self.input_3 = customtkinter.CTkEntry(self)
        self.input_4 = customtkinter.CTkEntry(self)
        self.input_5 = customtkinter.CTkEntry(self)

        self.save = customtkinter.CTkButton(self, text="Save", command=self.save_member)

        # Display the input elements
        self.label_1.grid(row=0, column=0, padx=10, pady=10)
        self.label_2.grid(row=0, column=3, padx=10, pady=10)
        self.label_3.grid(row=1, column=0, padx=10, pady=10)
        self.label_4.grid(row=1, column=3, padx=10, pady=10)
        self.label_5.grid(row=1, column=5, padx=10, pady=10)

        self.input_1.grid(row=0, column=1, padx=10, pady=10)
        self.input_2.grid(row=0, column=4, padx=10, pady=10)
        self.input_3.grid(row=1, column=1, padx=10, pady=10)
        self.input_4.grid(row=1, column=4, padx=10, pady=10)
        self.input_5.grid(row=1, column=6, padx=10, pady=10)

        self.save.grid(row=2, column=0, columnspan=6, padx=10, pady=10)

    def save_member(self):
        print("Saving member...")
        s_node = self.input_1.get()
        e_node = self.input_2.get()
        s_area = self.input_3.get()
        yg_mod = self.input_4.get()
        inertia = self.input_5.get()

        db = SQL("sqlite:///data.db")
        if not s_node or not e_node or not s_area or not yg_mod or not inertia:
            CTkMessagebox(title="Info", message="Please fill all the input fields!!!")
        else:
            try:
                db.execute(
                    """INSERT INTO members (
                        start_node, end_node, section_area, young_mod, inertia)
                        VALUES (?, ?, ?, ?, ?);""",
                    s_node,
                    e_node,
                    s_area,
                    yg_mod,
                    inertia,
                )
                self.master.master.root.plot_data()
            except ValueError:
                CTkMessagebox(title="Error", message="Wrong imput!!!", icon="cancel")
            self.clear()

    def clear(self):
        self.input_1.delete(0, customtkinter.END)
        self.input_2.delete(0, customtkinter.END)
        self.input_3.delete(0, customtkinter.END)
        self.input_4.delete(0, customtkinter.END)
        self.input_5.delete(0, customtkinter.END)


class Member(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Creating a frame for the member parameters
        self.member_frame = MemberFrame(self)
        self.member_frame.grid(row=0, column=0, padx=0, pady=0)
