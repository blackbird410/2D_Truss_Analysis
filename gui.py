import customtkinter
import sys, os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nodes import *
from members import *
from loads import *
from data import *


class PLotFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class OptionFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.root = master


class ButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create GUI  buttons
        self.b_1 = customtkinter.CTkButton(self, text="Node", command=master.add_nodes)
        self.b_2 = customtkinter.CTkButton(
            self, text="Member", command=master.add_members
        )
        self.b_3 = customtkinter.CTkButton(self, text="Load", command=master.add_loads)
        self.b_4 = customtkinter.CTkButton(self, text="Data", command=master.show_data)
        self.b_5 = customtkinter.CTkButton(self, text="Analyze", command=master.analyze)
        self.b_6 = customtkinter.CTkButton(
            self, text="Results", command=master.get_results
        )
        self.b_7 = customtkinter.CTkButton(
            self, text="Deformations", command=master.show_deformation
        )
        self.b_8 = customtkinter.CTkButton(
            self, text="Exit", fg_color="red", command=master.exit
        )
        self.b_9 = customtkinter.CTkButton(
            self, text="Reset", fg_color="red", command=master.reset
        )

        self.b_1.grid(row=0, column=0, padx=20, pady=10)
        self.b_2.grid(row=1, column=0, padx=20, pady=10)
        self.b_3.grid(row=2, column=0, padx=20, pady=10)
        self.b_4.grid(row=3, column=0, padx=20, pady=10)
        self.b_5.grid(row=4, column=0, padx=20, pady=10)
        self.b_6.grid(row=5, column=0, padx=20, pady=10)
        self.b_7.grid(row=6, column=0, padx=20, pady=10)
        self.b_8.grid(row=7, column=0, padx=20, pady=10)
        self.b_9.grid(row=8, column=0, padx=20, pady=10)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("2D Truss Analysis")
        self.geometry("800x680")
        self.minsize(800, 680)
        self.grid_columnconfigure(1, weight=1)

        # Create the frame of the buttons
        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=0, column=0, padx=10, pady=10)

        self.plot_frame = PLotFrame(self)
        self.plot_frame.grid(row=0, column=1, padx=10, pady=10)
        # self.plot_frame.columnconfigure(0, weight=1)

        # Display the plot
        self.fig, self.ax = plt.subplots()
        self.plot_data()

        # Creating a frame for the options
        self.option_frame = OptionFrame(self)
        self.option_frame.grid(
            row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )
        self.option_frame.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.option_frame.configure(fg_color="transparent")

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

    def show_data(self):
        self.destroy_frame()
        data_frame = Data(self.option_frame)
        data_frame.grid(row=0, column=1, padx=10, pady=10)
        data_frame.grid_columnconfigure(minsize=100, index=0, weight=1)

    @classmethod
    def check_stability(cls, m, r, j):
        """ "Verify the internal stability of a truss"""

        try:
            if (m > 1 and r > 2 and j > 2) and (m + r) >= 2 * j:
                return True
            else:
                return False
        except ValueError:
            ...
        return False
    

    def assign_dof_numbers(self):
        """Assign a number to a Degree Of Freedom by comparing the displacements at 
        each DOF (unknown(rx=0 || ry=0) or known(rx=1 || ry=1))."""

        try:
            # Select the data of the nodes from the database by sorting them by rx and ry
            db = SQL("sqlite:///data.db")
            
            # Check if this method has already been executed and the table already created
            test = db.execute("""SELECT name FROM sqlite_master WHERE type="table" AND name="dof_nodes";""")
            if test:
                # Remove the old table
                db.execute("DROP TABLE dof_nodes")
            
            nodes = db.execute("SELECT * FROM nodes ORDER BY rx, ry;")

            # Create a new sql table with id numbers for the nodes
            db.execute(
                """CREATE TABLE IF NOT EXISTS dof_nodes (
                    id INTEGER PRIMARY KEY NOT NULL,
                    node INTEGER NOT NULL,
                    axis TEXT NOT NULL,
                    FOREIGN KEY(node) REFERENCES nodes(id));"""
            )

            # Parse the data of the nodes while inserting each nodes into the new table by comparing rx an ry
            for node in nodes:
                if node["rx"] == 1 and node["ry"] == 0:
                    db.execute("INSERT INTO dof_nodes (node, axis) VALUES (?, ?);", node["id"], "y")
                    db.execute("INSERT INTO dof_nodes (node, axis) VALUES (?, ?);", node["id"], "x")
                else:
                    db.execute("INSERT INTO dof_nodes (node, axis) VALUES (?, ?);", node["id"], "x")
                    db.execute("INSERT INTO dof_nodes (node, axis) VALUES (?, ?);", node["id"], "y")
            return True
        except:
            return False


    def analyze(self):
        self.destroy_frame()

        # Query the numbers of nodes, members and support reactions
        db = SQL("sqlite:///data.db")
        nodes = db.execute("SELECT * FROM nodes;")
        n_nodes = 0
        n_reactions = 0
        for node in nodes:
            if node["rx"] == 1:
                n_reactions += 1
            if node["ry"] == 1:
                n_reactions += 1
            n_nodes += 1
        n_members = db.execute("SELECT COUNT(*) AS n_M FROM members;")[0]["n_M"]

        # Check the stability of the truss
        if self.check_stability(n_members, n_reactions, n_nodes):
            # Assign the degree of freedom the numbers by order
            response = self.assign_dof_numbers()
            if response:
                print("Task completed...")
        else:
            CTkMessagebox(title="Error", message="Error encountered. Please check your inputs.", option_1="cancel")

    def get_results(self):
        self.destroy_frame()

    def show_deformation(self):
        self.destroy_frame()

    def exit(self):
        msg = CTkMessagebox(
            title="Exit?",
            message="Do you want to close the program?",
            icon="question",
            option_1="Cancel",
            option_2="No",
            option_3="Yes",
        )
        response = msg.get()

        if response == "Yes":
            self.destroy()
        sys.exit("Program terminated...")

    def reset(self):
        if os.path.exists("data.db"):
            response = CTkMessagebox(
                self,
                icon="question",
                title="Reset database",
                message="Are you sure you want to reset the database?",
                option_1="No",
                option_2="Yes",
            )
            if response.get() == "Yes":
                # os.remove("data.db")
                CTkMessagebox(title="Info", message="DATABASE ERASED")

    def plot_data(self):
        # Clean the plot frame
        self.fig.clf()
        self.ax.cla()
        self.fig, self.ax = plt.subplots()

        # Parse the database to collect the data
        db = SQL("sqlite:///data.db")

        members = db.execute(
            """SELECT m.id, start_node, end_node, n1.x AS x_i, n1.y AS y_i, n2.x AS x_j, n2.y AS y_j FROM members m
                JOIN nodes n1 ON n1.id=m.start_node
                JOIN nodes n2 ON n2.id=m.end_node;"""
        )

        x_coords = []
        y_coords = []

        for member in members:
            x_coords.append(member["x_i"])
            y_coords.append(member["y_i"])
            x_coords.append(member["x_j"])
            y_coords.append(member["y_j"])

        # self.fig.title
        self.fig.set_figwidth(5.5)
        self.fig.set_figheight(3.8)
        self.ax.plot(x_coords, y_coords)
        self.canvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0)


def create_gui():
    app = App()
    app.mainloop()
