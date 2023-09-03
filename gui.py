import customtkinter
import sys, os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nodes import *
from members import *
from loads import *
from data import *
from functions import *
from math import sqrt, pow
from prettytable import PrettyTable


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

    def assign_dof_numbers(self):
        """Assign a number to a Degree Of Freedom by comparing the displacements at
        each DOF (unknown(rx=0 || ry=0) or known(rx=1 || ry=1))."""

        try:
            # Select the data of the nodes from the database by sorting them by rx and ry
            db = SQL("sqlite:///data.db")

            check_table("dof_nodes")

            nodes = db.execute("SELECT * FROM nodes ORDER BY rx, ry;")

            # Create a new sql table with id numbers for the nodes
            db.execute(
                """CREATE TABLE IF NOT EXISTS dof_nodes (
                    id INTEGER PRIMARY KEY NOT NULL,
                    node INTEGER NOT NULL,
                    axis TEXT NOT NULL,
                    reaction INTEGER NOT NULL,
                    FOREIGN KEY(node) REFERENCES nodes(id));"""
            )

            # Parse the data of the nodes while inserting each nodes into the new table by comparing rx an ry
            for node in nodes:
                if node["rx"] == 1 and node["ry"] == 0:
                    db.execute(
                        "INSERT INTO dof_nodes (node, axis, reaction) VALUES (?, ?, ?);",
                        node["id"],
                        "y",
                        node["ry"]
                    )
                    db.execute(
                        "INSERT INTO dof_nodes (node, axis, reaction) VALUES (?, ?, ?);",
                        node["id"],
                        "x",
                        node["rx"]
                    )
                else:
                    db.execute(
                        "INSERT INTO dof_nodes (node, axis, reaction) VALUES (?, ?, ?);",
                        node["id"],
                        "x",
                        node["rx"]
                    )
                    db.execute(
                        "INSERT INTO dof_nodes (node, axis, reaction) VALUES (?, ?, ?);",
                        node["id"],
                        "y",
                        node["ry"]
                    )
            return True
        except:
            return False

    def generate_msm(self):
        """Generates the stiffness matrices of each members of the truss.
        Returns a list of the matrices (type: np.array)."""

        # Query the members, nodes and dof_nodes databases
        db = SQL("sqlite:///data.db")
        members = db.execute(
            """SELECT m.id, 
                    start_node, 
                    end_node, 
                    section_area AS A, 
                    young_mod AS E, 
                    inertia AS I,  
                    n1.x AS x_i, 
                    n1.y AS y_i, 
                    n2.x AS x_j, 
                    n2.y AS y_j 
                FROM members m
                JOIN nodes n1 ON n1.id=m.start_node
                JOIN nodes n2 ON n2.id=m.end_node;"""
        )

        check_table("lambdas")

        # Add a new table of lambdas in the database
        db.execute(
            """CREATE TABLE IF NOT EXISTS lambdas(
                    id INTEGER PRIMARY KEY NOT NULL,
                    member INTEGER NOT NULL,
                    lambda_x FLOAT NOT NULL,
                    lambda_y FLOAT NOT NULL,
                    length FLOAT NOT NULL,
                    FOREIGN KEY(member) REFERENCES members (id));"""
        )

        # Determine the stiffness matrix for each members and append the to a list
        matrices = []
        for member in members:
            # Determine the length, lambda_x and lambda_y
            length = sqrt(
                pow((member["x_j"] - member["x_i"]), 2)
                + pow((member["y_j"] - member["y_i"]), 2)
            )

            try:
                lambda_x = abs(member["x_j"] - member["x_i"]) / length
                lambda_y = abs(member["y_j"] - member["y_i"]) / length

                # Add the lambdas and length to the members table for finding the internal forces
                db.execute("INSERT INTO lambdas (member, lambda_x, lambda_y, length) VALUES (?, ?, ?, ?);", member["id"], lambda_x, lambda_y, length)
            except ZeroDivisionError:
                CTkMessagebox(
                    title="Error",
                    message="One of the members length is null, please restart analysis by inputing new coordinates.",
                )

            # Write the matrix form with the lambdas
            msm = [
                [
                    pow(lambda_x, 2),
                    lambda_x * lambda_y,
                    -(pow(lambda_x, 2)),
                    -(lambda_x * lambda_y),
                ],
                [
                    lambda_x * lambda_y,
                    pow(lambda_y, 2),
                    -(lambda_x * lambda_y),
                    -(pow(lambda_y, 2)),
                ],
                [
                    -(pow(lambda_x, 2)),
                    -(lambda_x * lambda_y),
                    pow(lambda_x, 2),
                    lambda_x * lambda_y,
                ],
                [
                    -(lambda_x * lambda_y),
                    -(pow(lambda_y, 2)),
                    lambda_x * lambda_y,
                    pow(lambda_y, 2),
                ],
            ]

            msm = ((member["E"] * member["A"]) / length) * np.array(msm)

            print(msm)

            # Query the numbering order for the DOFs
            dof_start_node = db.execute(
                "SELECT id FROM dof_nodes WHERE (node=?);", member["start_node"]
            )
            dof_end_node = db.execute(
                "SELECT id FROM dof_nodes WHERE (node=?);", member["end_node"]
            )
            dof_numbers = [
                dof_start_node[0]["id"],
                dof_start_node[1]["id"],
                dof_end_node[0]["id"],
                dof_end_node[1]["id"],
            ]

            dof_numbers = sorted(dof_numbers)

            # Querying the dimension of the global structure
            dim = db.execute("SELECT COUNT(*) AS n FROM nodes;")[0]["n"] * 2

            # Adding the columns and rows not present in the array to allow members matrix addition
            msm = globalize(dim, dof_numbers, msm)

            print()
            print(msm)

            matrices.append(np.round(msm, 4))

        return matrices

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
        if not check_stability(n_members, n_reactions, n_nodes):
            CTkMessagebox(
                title="Error",
                message="Error encountered. Please check your inputs.",
                option_1="cancel",
            )
        else:
            # Assign the degree of freedom the numbers by order
            response = self.assign_dof_numbers()
            print(response)
            if response:
                # Generate the global structure stiffness matrix
                self.ssm = sum(self.generate_msm())
                x = PrettyTable(self.ssm.dtype.names)
                for row in self.ssm:
                    x.add_row(row)
                print()
                print(x)

                load_v, dsp_v = self.get_loads_displacements()

                # Determine the unknown displacements
                # First partitionate the structure stiffness matrix
                sub_ssm = self.ssm[:load_v.shape[0], :load_v.shape[0]]
                sub_ssm_r = self.ssm[load_v.shape[0]:, :load_v.shape[0]]
                try:
                    # Multiply the load vector by the inverse of the sub matrix to find the unknowned displacements
                    # X = A-1 * B
                    dsp = np.linalg.inv(sub_ssm).dot(load_v)
                    reactions = sub_ssm_r.dot(dsp)
                   
                    # Find the internal efforts
                    # Query the dof code numbers associated with each members
                    dofs = db.execute(
                        """SELECT m.id, 
                                m.start_node, 
                                m.end_node, 
                                d1.id AS dof_SN, 
                                d2.id AS dof_EN,
                                lambda_x,
                                lambda_y,
                                length 
                                FROM members m
                                JOIN dof_nodes d1 ON m.start_node = d1.node
                                JOIN dof_nodes d2 ON m.end_node = d2.node
                                JOIN lambdas ON m.id = lambdas.member;""")
                    
                    # Filter duplicate values through a set
                    set_list = []
                    lambdas_list = []
                    dof_set = set()
                    dof_set_en = set()
                    current = 0
                    lambdas = {}
                    for dof in dofs:
                        if current and dof["id"] !=  current:
                            # Add the sets
                            dof_set.update(dof_set_en)
                            set_list.append(dof_set)
                            lambdas_list.append(lambdas)
                            dof_set = set()
                            dof_set_en = set()
                            lambdas = {}

                        dof_set.add(dof["dof_SN"])
                        dof_set_en.add(dof["dof_EN"])
                        current = dof["id"]

                        # Get the orientations
                        if "x" not in lambdas.keys():
                            lambdas["x"] = dof["lambda_x"]
                        if "y" not in lambdas.keys():
                            lambdas["y"] = dof["lambda_y"]
                        if "l" not in lambdas.keys():
                            lambdas["l"] = dof["length"]
                        if "member" not in lambdas.keys():
                            lambdas["member"] = dof["id"]

                    # Add the last set
                    dof_set.update(dof_set_en)
                    set_list.append(dof_set)
                    lambdas_list.append(lambdas)

                    # Full displacement vector
                    full_dsp = np.concatenate((dsp, dsp_v))

                    check_table("internal_efforts")
                    check_table("node_dsp")

                    # Create a table for saving the internal efforts results
                    db.execute(
                        """CREATE TABLE IF NOT EXISTS internal_efforts (
                            id INTEGER PRIMARY KEY NOT NULL,
                            member INTEGER NOT NULL,
                            effort FLOAT NOT NULL,
                            FOREIGN KEY(member) REFERENCES members(id));"""
                    )

                    # Create a table for saving the node displacements results
                    db.execute(
                        """CREATE TABLE IF NOT EXISTS node_dsp (
                            id INTEGER PRIMARY KEY NOT NULL,
                            node INTEGER NOT NULL,
                            d_x FLOAT NOT NULL,
                            d_y FLOAT NOT NULL,
                            FOREIGN KEY(node) REFERENCES nodes(id));"""
                    )

                    dsp_dct = {}
                    # Add the nodes displacements to the table
                    d_x = 0
                    d_y = 0
                    for i in range(full_dsp.shape[0]):
                        # print(np.round(d, 4)[0])
                        dof_data = db.execute("SELECT axis, node FROM dof_nodes WHERE id=?;", i + 1)[0]
                        if dof_data["axis"] == "x":
                            d_x = np.round(full_dsp[i], 4)[0]
                        else:
                            d_y = np.round(full_dsp[i], 4)[0]
                        
                        dsp_dct[str(dof_data["node"])] = {"x": d_x, "y": d_y}

                    for d in dsp_dct:
                        db.execute("INSERT INTO node_dsp (node, d_x, d_y) VALUES (?, ?, ?);", int(d), dsp_dct[d]["x"], dsp_dct[d]["y"])


                    # Get the appropriate displacement vector for each members by using the dof codes
                    for i in range(len(set_list)):
                        index = list(set_list[i]) 
                        lambdas = lambdas_list[i]
                        sub_dsp = np.concatenate(
                            (full_dsp[(index[0]-1):(index[1])], full_dsp[(index[2]-1):(index[3])]))
                        
                        lambda_mat = np.array(
                            [
                                [-(lambdas["x"]), -(lambdas["y"]), lambdas["x"], lambdas["y"]]
                            ])
                        
                        # Inserting the result to the table
                        db.execute("INSERT INTO internal_efforts (member, effort) VALUES (?, ?);", lambdas["member"], np.round(lambda_mat.dot(sub_dsp) / lambdas["l"], 4)[0][0])

                except np.linalg.LinAlgError:
                    CTkMessagebox(title="Error", message="The stiffness matrix is a singular matrix, could not invert.")
                    


    def get_loads_displacements(self):
        """"Generates the load and displacements vector for the truss."""

        db = SQL("sqlite:///data.db")

        # Query the loads and the dof_nodes from the database
        loads = db.execute("SELECT * FROM loads;")
        if not loads:
            CTkMessagebox(title="Info", message="There is no load applied on the truss.")
            return None
        
        dof_nodes = db.execute("SELECT * FROM dof_nodes;")
        load_v = np.array([[]])
        dsp_v = np.array([[]])

        for dof in dof_nodes:
            # Check if there is a support reaction there
            if dof["reaction"] == 1:
                dsp_v = np.insert(dsp_v, 0, 0, 1)
            else:
                for load in loads:
                    if load["node"] == dof["node"]:
                        if dof["axis"] == "x":
                            load_v = np.insert(load_v, load_v.shape[1], load["x_load"], 1)
                        else:
                            load_v = np.insert(load_v, load_v.shape[1], load["y_load"], 1)
        
        # Transpose the arrays
        return load_v.T, dsp_v.T


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
