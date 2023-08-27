import customtkinter


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
        self.label_2.grid(row=1, column=0, padx=10, pady=10)
        self.label_3.grid(row=2, column=0, padx=10, pady=10)
        self.label_4.grid(row=3, column=0, padx=10, pady=10)
        self.label_5.grid(row=4, column=0, padx=10, pady=10)

        self.input_1.grid(row=0, column=1, padx=10, pady=10)
        self.input_2.grid(row=1, column=1, padx=10, pady=10)
        self.input_3.grid(row=2, column=1, padx=10, pady=10)
        self.input_4.grid(row=3, column=1, padx=10, pady=10)
        self.input_5.grid(row=4, column=1, padx=10, pady=10)

        self.save.grid(row=5, column=0, columnspan=2, padx=10, pady=10)


    def save_member(self):
        print("Saving member...")
        s_node = self.input_1.get()
        e_node = self.input_2.get()
        s_area = self.input_3.get()
        yg_mod = self.input_4.get()
        inertia = self.input_5.get()

        print(f"Start: {s_node}\nEnd: {e_node}\nArea: {s_area}\nE: {yg_mod}\nI: {inertia}")


class Member(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # self.title("Members")
        # self.geometry("350x350")

        # Creating a frame for the member parameters
        self.member_frame = MemberFrame(self)
        self.member_frame.grid(row=0, column=0, padx=10, pady=10)

        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)