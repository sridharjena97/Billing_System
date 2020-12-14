import tkinter as tk
import sqlite3
from tkinter.filedialog import asksaveasfilename
import threading
from tkinter import messagebox
import subprocess
import os


class PrintWindow:
    def __init__(self, master, dictionary):
        self.master = master
        # Initializing Window
        self.master.geometry("650x620+100+20")
        self.master.minsize(650, 600)
        self.master.configure(bg="gray20")
        self.master.title("Print")
        self.master.invoice = dictionary["invoice"]
        # Trying to set icon
        try:
            self.master.iconbitmap("images/print.ico")
        except:
            pass
        self.showWidgets(dictionary)

    def recover(self, data):
        data = data.replace("{", "(")
        data = data.replace("}", ")")
        data = data.replace("^", "\'")
        return data

    def showWidgets(self, dictionary):
        invoice = dictionary["invoice"]
        customer = dictionary["customer"]
        c_address = dictionary["c_address"]
        c_city = dictionary["c_city"]
        c_state = dictionary["c_state"]
        doc = dictionary["doc"]
        purchage_data = dictionary["purchage_data"]
        total = dictionary["total"]

        # FONTS
        fontlabel = "Eras 9 bold"
        fontinvoice = "Lucida 13 bold"
        fontdata = "Lucida 13 normal"
        fontdata1 = "Lucida 8 bold"
        fontdata2 = "Lucida 8 normal"
        font2 = "Arial 12 normal"
        # Creatting frame for displaying preview
        frame1 = tk.Frame(self.master)
        frame1.pack(fill=tk.BOTH)
        # Frame for buttons
        self.master.frame2 = tk.Frame(self.master, bg="gray30")
        self.master.frame2.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(self.master.frame2, text="Print", font=font2, bd=3, relief=tk.RAISED, command=self.printData).pack(
            side=tk.LEFT, padx=10, pady=5)
        tk.Button(self.master.frame2, text="Save As PDF", font=font2, bd=3, relief=tk.RAISED,
                  command=threading.Thread(target=self.savePDF).start).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(self.master.frame2, text="Close", font=font2, bd=3, relief=tk.RAISED,
                  command=self.master.destroy).pack(side=tk.LEFT, padx=10, pady=5)
        # creating casvas and ploting data
        self.master.cnx = sqlite3.connect("DB/database")
        cursor = self.master.cnx.cursor()
        cursor.execute("SELECT * FROM appdata WHERE srl=1")
        for data in cursor:
            optional_label = self.recover(data[1])
            table_label_1 = self.recover(data[5])
            print_heading = self.recover(data[6])
            busniess_name = self.recover(data[7])
            address_line1 = self.recover(data[8])
            address_line2 = self.recover(data[9])
            address_line3 = self.recover(data[10])

        self.canvaswidth = 600
        self.canvasheight = 550
        self.canvas = tk.Canvas(self.master, height=self.canvasheight, width=self.canvaswidth, bd=1, relief=tk.GROOVE)
        self.canvas.create_text(300, 25, font="Rockwell 17 bold", text=print_heading)
        self.canvas.create_line(0, 45, 600, 45, dash=(200, 1))
        self.canvas.create_text(10, 70, font=fontlabel, text="INVOICE NUMBER:", anchor="w")
        self.canvas.create_text(120, 70, font=fontinvoice, text=invoice, anchor="w")
        self.canvas.create_text(10, 100, font=fontlabel, text="CUSTOMER NAME:", anchor="w")
        self.canvas.create_text(120, 100, font=fontdata, text=customer, anchor="w")
        self.canvas.create_text(10, 130, font=fontlabel, text="ADDRESS:", anchor="w")
        self.canvas.create_text(73, 130, font=fontdata, text=c_address, anchor="w")
        self.canvas.create_text(392, 130, font=fontlabel, text="CITY:", anchor="w")
        self.canvas.create_text(425, 130, font=fontdata, text=c_city, anchor="w")
        self.canvas.create_text(380, 160, font=fontlabel, text="STATE:", anchor="w")
        self.canvas.create_text(425, 160, font=fontdata, text=c_state, anchor="w")
        self.canvas.create_text(10, 160, font=fontlabel, text=optional_label, anchor="w")
        self.canvas.create_text(93, 160, font=fontdata, text=doc, anchor="w")
        self.canvas.create_line(10, 200, 590, 200)  # table upper line
        self.canvas.create_line(10, 400, 590, 400)  # table bottom line
        self.canvas.create_line(10, 200, 10, 400)  # table left line
        self.canvas.create_line(590, 200, 590, 400)  # table right line
        self.canvas.create_line(50, 200, 50, 400, dash=(4, 1))  # table column1
        self.canvas.create_line(340, 200, 340, 400, dash=(4, 1))  # table column2
        self.canvas.create_line(415, 200, 415, 400, dash=(4, 1))  # table column3
        self.canvas.create_line(490, 200, 490, 400, dash=(4, 1))  # table column4
        # self.canvas.create_line(10,230,590,230,dash=(4,1)) #table row1
        ycord = 230
        a = 0
        while a < 10:
            self.canvas.create_line(10, ycord, 590, ycord, dash=(4, 1))
            ycord += 17
            a += 1
        self.canvas.create_text(20, 210, font=fontdata1, text="Srl.", anchor="w")
        self.canvas.create_text(70, 210, font=fontdata1, text=table_label_1, anchor="w")
        self.canvas.create_text(365, 210, font=fontdata1, text="QTY", anchor="w")
        self.canvas.create_text(425, 210, font=fontdata1, text="UNIT PRICE", anchor="w")
        self.canvas.create_text(505, 210, font=fontdata1, text="TOTAL PRICE", anchor="w")
        self.canvas.create_text(370, 415, font=fontdata, text="GRAND TOTAL:", anchor="w")
        self.canvas.create_text(500, 415, font=fontdata, text="₹" + total, anchor="w")
        # self.canvas.create_text(25,233,font=fontdata1,text="1",anchor="w")
        ycord = 238
        srl = 1
        for srl in range(1, 11):
            self.canvas.create_text(25, ycord, font=fontdata1, text=str(srl), anchor="w")
            ycord += 17
            srl += 1
        ycord = 238
        xcord = [60, 345, 420, 500]
        for row in range(10):
            for column in range(4):
                self.canvas.create_text(xcord[column], ycord, font=fontdata2, text=purchage_data[row][column],
                                        anchor="w")
            ycord += 17
        self.canvas.create_text(450, 460, font=fontlabel, text="SIGNATURE", anchor="w")
        self.canvas.create_line(400, 450, 570, 450)
        self.canvas.create_text(300, 490, font="Bookman 14 bold", text=busniess_name)
        self.canvas.create_text(300, 510, font="Arial 11 normal", text=address_line1)
        self.canvas.create_text(300, 525, font="Arial 8 normal", text=address_line2)
        self.canvas.create_text(300, 542, font="Arial 8 normal", text=address_line3)
        self.canvas.pack(padx=10, pady=10)

    def savePDF(self):
        try:
            self.canvas.postscript(file="temp/tmp.ps", colormode='color')
            self.master.update()
            file = asksaveasfilename(initialfile=f"{self.master.invoice}.pdf", defaultextension=".pdf",
                                     filetypes=[("All Files", "*.*"), ("PDF Documents", "*.pdf")])
            process = subprocess.Popen(["ps2pdf", "temp/tmp.ps", file], shell=True)
            process.wait()

        except:
            messagebox.showerror("Error",
                                 "This Program require ghostscript to run properly.\n You can install ghostscript from "
                                 "<https://ghostscript.com/download/gsdnld.html>.\n If you are in windows and have "
                                 "chocolaty installed. issue command <choco install ghostscript> to install. After "
                                 "installation add it's bin and lb file to path.")

    def printData(self):
        try:
            self.canvas.postscript(file="temp/tmp.ps", colormode='color')
            process = subprocess.Popen(["ps2pdf", "temp/tmp.ps", "temp/temp.pdf"], shell=True)
            process.wait()
            target_file = os.path.abspath('temp/temp.pdf')
            os.startfile(target_file, "print")

        except:
            messagebox.showerror("Error",
                                 "This Program require ghostscript to run properly.\n You can install ghostscript from "
                                 "<https://ghostscript.com/download/gsdnld.html>.\n If you are in windows and have "
                                 "chocolaty installed. issue command <choco install ghostscript> to install. After "
                                 "installation add it's bin and lb file to path.")


if __name__ == "__main__":
    # Program Start
    root = tk.Tk()
    dictionary = {
        "invoice": "invoice",
        "customer": "customer",
        "c_address": "c_address",
        "c_city": "c_city",
        "c_state": "c_state",
        "doc": "doc",
        "purchage_data": [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1],
                          [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
        "total": "total",
    }
    app = PrintWindow(root, dictionary)

    root.mainloop()
