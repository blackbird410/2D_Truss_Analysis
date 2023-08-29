import customtkinter
from cs50 import SQL


class DataFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class Data(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.frames = []

        # Fetching the data and design the headers
        db = SQL("sqlite:///data.db")

        table_list = []
        for table in ["nodes", "members", "loads"]:
            table_list.append(db.execute("SELECT * FROM ?;", table))

        self.table_headers = [
            ["Node", "X", "Y", "Rx", "Ry"],
            ["Bar", "Start Node", "End Node", "S", "E", "I"],
            ["Load", "Fx", "Fy", "Node Applied"],
        ]

        self.table_widths = [
            [40, 40, 40, 40, 40],
            [40, 40, 40, 60, 60, 60],
            [40, 50, 50, 40],
        ]

        counter = 0
        for table in table_list:
            frame = DataFrame(self)
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
