import tkinter as tk
from tkinter import ttk
import sqlite3
import threading
import time
from ast import literal_eval
from PIL import Image, ImageTk
from itertools import count
from tkcalendar import DateEntry
from datetime import timedelta


class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


class History:
    def __init__(self, master):
        self.master = master
        self.master.geometry("852x480")
        self.master.title("Invoice History")
        try:
            self.master.iconbitmap("images/history.ico")
        except:
            pass
        self.showWidgets()

    def showWidgets(self):
        def startThread():
            thread = threading.Thread(target=insertData)
            if thread.is_alive():
                thread.join()
            else:
                thread.start()

        def insertData():
            spinner.load('images/spinner2.gif')
            start = start_date.get_date()
            end = end_date.get_date()
            for i in tree.get_children():
                tree.delete(i)
            start = start.strftime("%Y-%m-%d %H:%M:%S")
            end = end + timedelta(days=1)
            end = end.strftime("%Y-%m-%d %H:%M:%S")
            cnx = sqlite3.connect("DB/database")
            cursor = cnx.cursor()
            query = f"SELECT * FROM medicalbill WHERE entry_time BETWEEN '{start}' AND  '{end}';"
            cursor.execute(query)
            list = cursor.fetchall()
            time.sleep(0.5)
            for index, data in enumerate(list):
                invoice = data[0]
                customer = data[1]
                list = data[6]
                list = self.decodeList(list)
                total = self.calTotal(list)
                entry_time = data[7]
                values = (invoice, customer, total, entry_time)
                tree.insert(parent='', index='end', iid=index, values=values)
            spinner.unload()

        theme = "LightGoldenrod1"
        font1 = "Arial 12 bold"
        frame = tk.Frame(self.master, bg=theme)
        frame.pack(anchor="nw", fill="x")
        tk.Label(frame, text="FROM:", bg=theme, font=font1).pack(side=tk.LEFT, anchor="w", padx=5, pady=12)
        start_date = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        start_date.pack(side=tk.LEFT, anchor="w", padx=5, pady=12)
        tk.Label(frame, text="TO:", bg=theme, font=font1).pack(side=tk.LEFT, anchor="w", padx=5, pady=12)
        end_date = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        end_date.pack(side=tk.LEFT, anchor="w", padx=5, pady=12)
        tk.Button(frame, text="Fetch Data", font="Arial 12", bg="lawn green", command=lambda: startThread()).pack(
            side=tk.LEFT, anchor="w", padx=25, pady=12)

        spinner = ImageLabel(frame, bg=theme)
        spinner.pack(side=tk.LEFT, anchor="w", padx=15, pady=12)

        # Creating a scrollable frame
        frame1 = tk.Frame(self.master, bg="grey60", bd=5)
        frame1.pack(fill="both", expand=1, padx=3, pady=3)
        canvas = tk.Canvas(frame1)
        canvas.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame1, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # adding a new frame to canvas to create new window
        frame2 = tk.Frame(canvas, bg="red")
        frame2.pack(fill="both")
        # adding the new frame to canvas window
        canvas.create_window((0, 0), window=frame2, anchor="nw")
        # creating tree view
        tree = ttk.Treeview(frame2)
        # defining columns
        tree['columns'] = ("Invoice", "Name", "Total", "Time")
        # formatte our columns
        tree.column("#0", width=2, minwidth=5)
        tree.column("Invoice", width=100, anchor="w")
        tree.column("Name", width=200, anchor="w")
        tree.column("Total", anchor="w")
        tree.column("Time", anchor="w")
        # Creating Headings
        tree.heading("#0", text="Label", anchor="w")
        tree.heading("Invoice", text="Invoice Number", anchor="w")
        tree.heading("Name", text="Customer Name", anchor="center")
        tree.heading("Total", text="Total Invoice Value", anchor="w")
        tree.heading("Time", text="Entry Time", anchor="w")
        tree.pack(fill="both", expand=1)

    def decodeList(self, str):
        """decoding algorithm for encoded list"""
        list = str.replace("\\", "\'")
        list = literal_eval(list)  # convering string to list
        return list

    def calTotal(self, list):
        total = ""
        for item in list:
            val = item[3]
            if val == "":
                total += "+0"
            else:
                total += "+" + val
        total = eval(total)
        return total

if __name__ == "__main__":
    root = tk.Tk()
    app = History(root)
    root.mainloop()