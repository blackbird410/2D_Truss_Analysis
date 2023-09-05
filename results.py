import customtkinter
from cs50 import SQL

class ResultFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class Result(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.frames = []

        # Fetching the data and design the headers
        db = SQL("sqlite:///data.db")

        table_list = []
        # for table in ["node_dsp", "internal_efforts", "reactions"]:
        table_list.append(db.execute("SELECT node, d_x, d_y FROM node_dsp ORDER BY node;"))
        table_list.append(db.execute("SELECT member, effort FROM internal_efforts ORDER BY member;"))
        table_list.append(db.execute("SELECT node, axis, reaction FROM reactions ORDER BY node;"))

        self.table_headers = [
            ["Node", "D_x", "D_y"],
            ["Member", "Effort(K)"],
            ["Node", "Axis", "Reaction(K)"]
        ]

        self.table_widths = [
            [80, 80, 80],
            [80, 80],
            [80, 80, 80]
        ]

        counter = 0
        for table in table_list:
            frame = ResultFrame(self)
            # Printing table
            if not table:
                continue

            data = []
            keys = list(table[0].keys())
            for row in table:
                r = []
                for i in range(len(keys)):
                    r.append(row[keys[i]])
                data.append(r)

            for col, header in enumerate(self.table_headers[counter]):
                label = customtkinter.CTkLabel(frame, text=header)
                label.grid(row=0, column=col, padx=10, pady=5)

            widths = self.table_widths[counter]
            for row, row_data in enumerate(data, start=1):
                for col, value in enumerate(row_data):
                    entry = customtkinter.CTkEntry(frame, width=widths[col])
                    entry.insert(customtkinter.END, value)
                    entry.grid(row=row, column=col, padx=10, pady=5)

            frame.grid(row=counter, column=0, padx=10, pady=10)
            counter += 1