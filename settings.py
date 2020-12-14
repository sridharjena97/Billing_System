import tkinter as tk
import sqlite3


class SettingsWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry("750x500+0+0")
        self.master.title("Settings")
        self.master.theme = "grey50"
        self.master.config(bg="grey50")
        try:
            self.master.iconbitmap("images/settings.ico")
        except:
            pass
        self.showWidgets()
        self.extractSettingsData()

    def showWidgets(self):
        '''Shows the widgets of GUI'''
        textcolor = "yellow2"
        textcolor1 = "White"
        font1 = "Arial 8 normal"
        font2 = "Cascadia 12 normal"
        frame1 = tk.Frame(self.master, bg=self.master.theme)
        frame1.pack(anchor="w")
        tk.Label(frame1, text="App Settings", fg="white", bg=self.master.theme, font="Franklin 22 bold", anchor="w",
                 underline=True).pack(side=tk.LEFT, padx=10, pady=20)
        frame2 = tk.Frame(self.master, bg=self.master.theme)
        frame2.pack(anchor="w", padx=10)
        self.master.optional_label = tk.StringVar()
        self.master.default_city = tk.StringVar()
        self.master.default_state = tk.StringVar()
        self.master.default_note = tk.StringVar()
        self.master.table_label_1 = tk.StringVar()
        self.master.print_heading = tk.StringVar()
        self.master.busniess_name = tk.StringVar()
        self.master.address_line1 = tk.StringVar()
        self.master.address_line2 = tk.StringVar()
        self.master.address_line3 = tk.StringVar()
        tk.Label(frame2, text="Edit Required place and Press ok to save", bg=self.master.theme, fg=textcolor,
                 font=font1).grid()
        tk.Label(frame2, text="Optional Field Name", bg=self.master.theme, fg=textcolor1, font=font2).grid(row=1,
                                                                                                           sticky="e",
                                                                                                           pady=3)
        tk.Entry(frame2, textvariable=self.master.optional_label, font=font2, width=50).grid(row=1, column=1, pady=3)
        tk.Label(frame2, text="Default City", bg=self.master.theme, fg=textcolor1, font=font2).grid(row=2, sticky="e",
                                                                                                    pady=3)
        tk.Entry(frame2, textvariable=self.master.default_city, font=font2, width=50).grid(row=2, column=1, pady=3)
        tk.Label(frame2, text="Default state", bg=self.master.theme, fg=textcolor1, font=font2).grid(row=3, sticky="e",
                                                                                                     pady=3)
        tk.Entry(frame2, textvariable=self.master.default_state, font=font2, width=50).grid(row=3, column=1, pady=3)
        tk.Label(frame2, text="Default text for optional field", bg=self.master.theme, fg=textcolor1, font=font2).grid(
            row=4, sticky="e", pady=3)
        tk.Entry(frame2, textvariable=self.master.default_note, font=font2, width=50).grid(row=4, column=1, pady=3)
        tk.Label(frame2, text="Table Heading", bg=self.master.theme, fg=textcolor1, font=font2).grid(row=5, sticky="e",
                                                                                                     pady=3)
        tk.Entry(frame2, textvariable=self.master.table_label_1, font=font2, width=50).grid(row=5, column=1, pady=3)
        tk.Label(frame2, text="Print Heading", bg=self.master.theme, fg=textcolor1, font=font2).grid(row=6, sticky="e",
                                                                                                     pady=3)
        tk.Entry(frame2, textvariable=self.master.print_heading, font=font2, width=50).grid(row=6, column=1, pady=3)
        tk.Label(frame2, text="Busniess Name", bg=self.master.theme, fg=textcolor1, font=font2).grid(row=7, sticky="e",
                                                                                                     pady=3)
        tk.Entry(frame2, textvariable=self.master.print_heading, font=font2, width=50).grid(row=7, column=1, pady=3)
        tk.Label(frame2, text="Address Line1", bg=self.master.theme, fg=textcolor1, font=font2).grid(row=8, sticky="e",
                                                                                                     pady=3)
        tk.Entry(frame2, textvariable=self.master.address_line1, font=font2, width=50).grid(row=8, column=1, pady=3)
        tk.Label(frame2, text="Address Line2", bg=self.master.theme, fg=textcolor1, font=font2).grid(row=9, sticky="e",
                                                                                                     pady=3)
        tk.Entry(frame2, textvariable=self.master.address_line2, font=font2, width=50).grid(row=9, column=1, pady=3)
        tk.Label(frame2, text="Address Line3", bg=self.master.theme, fg=textcolor1, font=font2).grid(row=10, sticky="e",
                                                                                                     pady=3)
        tk.Entry(frame2, textvariable=self.master.address_line3, font=font2, width=50).grid(row=10, column=1, pady=3)
        frame3 = tk.Frame(self.master, bg=self.master.theme)
        frame3.pack(anchor="w", padx=10)
        tk.Button(frame3, text="Save", font=font2, bd=3, relief=tk.RAISED, command=self.updateSettings).pack(padx=30,
                                                                                                             pady=10,
                                                                                                             side=tk.LEFT)
        tk.Button(frame3, text="Close", font=font2, bd=3, relief=tk.RAISED, command=self.master.destroy).pack(pady=10,
                                                                                                              padx=4,
                                                                                                              side=tk.LEFT)

    def extractSettingsData(self):
        '''Exatracts settings data fom database and set the widgets'''
        conn = sqlite3.connect("database")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appdata WHERE srl='1'")
        for data in cursor:
            self.master.optional_label.set(self.recover(data[1]))
            self.master.default_city.set(self.recover(data[2]))
            self.master.default_state.set(self.recover(data[3]))
            self.master.default_note.set(self.recover(data[4]))
            self.master.table_label_1.set(self.recover(data[5]))
            self.master.print_heading.set(self.recover(data[6]))
            self.master.busniess_name.set(self.recover(data[7]))
            self.master.address_line1.set(self.recover(data[8]))
            self.master.address_line2.set(self.recover(data[9]))
            self.master.address_line3.set(self.recover(data[10]))
        cursor.close()
        conn.close()

    def updateSettings(self):
        optional_label = self.master.optional_label.get()[:50]
        default_city = self.master.default_city.get()[:50]
        default_state = self.master.default_state.get()[:50]
        default_note = self.master.default_note.get()[:50]
        table_label_1 = self.master.table_label_1.get()[:50]
        print_heading = self.master.print_heading.get()[:150]
        busniess_name = self.master.busniess_name.get()[:150]
        address_line1 = self.master.address_line1.get()[:150]
        address_line2 = self.master.address_line2.get()[:150]
        address_line3 = self.master.address_line3.get()[:150]
        optional_label = self.prepare(self.master.optional_label.get())
        default_city = self.prepare(self.master.default_city.get())
        default_state = self.prepare(self.master.default_state.get())
        default_note = self.prepare(self.master.default_note.get())
        table_label_1 = self.prepare(self.master.table_label_1.get())
        print_heading = self.prepare(self.master.print_heading.get())
        busniess_name = self.prepare(self.master.busniess_name.get())
        address_line1 = self.prepare(self.master.address_line1.get())
        address_line2 = self.prepare(self.master.address_line2.get())
        address_line3 = self.prepare(self.master.address_line3.get())
        conn = sqlite3.connect("database")
        cursor = conn.cursor()
        query = f'''UPDATE appdata SET optional_label='{optional_label}',default_city='{default_city}',default_state='{default_state}',default_note='{default_note}',table_label_1='{table_label_1}',print_heading='{print_heading}',busniess_name='{busniess_name}',address_line1='{address_line1}',address_line2='{address_line2}',address_line3 ='{address_line3}'  WHERE srl=1'''
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        self.extractSettingsData()
        tk.Label(self.master, text="Information:Settings Upadated. Restart the program to make changes in effect.",
                 bg="yellow green", fg="white", font="Arial 12 italic").pack(side=tk.LEFT, anchor="w", padx=10)

    def recover(self, data):
        data = data.replace("{", "(")
        data = data.replace("}", ")")
        data = data.replace("^", "\'")
        return data

    def prepare(self, data):
        data = data.replace("(", "{")
        data = data.replace(")", "}")
        data = data.replace("\'", "^")
        data = data.replace("\"", "")
        data = data.replace(";", "")
        data = data.replace("DELETE", "")
        data = data.replace("DROP", "")
        return data


if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsWindow(root)
    root.mainloop()