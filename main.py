import os
import sqlite3
import subprocess
import time
import tkinter as tk
from ast import literal_eval
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import timedelta
from PIL import Image, ImageTk
from itertools import count
import threading


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry("852x700+0+0")
        self.master.minsize(852, 700)
        self.master.title("JENA Billing System")
        self.master.font1 = "Arial 12 normal"
        self.master.font2 = "Arial 13 normal"
        self.master.theme = "grey69"
        self.master.labelwidth = 15
        self.master.padx = 10
        self.master.ipadx = 3
        self.master.config(bg=self.master.theme)
        try:
            self.master.iconbitmap("icon.ico")
        except:
            pass
        self.connectDB()
        self.showWidgets()
        self.statusBar()
        self.menubar()

    def about(self):
        """Shows information about the application"""
        messagebox.showinfo("About",
                            "Developed By: Sridhar Jena. \n\nThis software is sole property of SRIDHWORK. Selling copy of this software is strictly prohibited.\nUse at your own risk.\nFor any query/customization, please contact sridhwork@gmail.com. \n\n© SridhWork 2020 all rights reserved.")

    def menubar(self):
        mainmenu = tk.Menu(self.master)
        optionsmenu = tk.Menu(mainmenu, tearoff=0)
        optionsmenu.add_command(label="Settings", command=lambda: self.newWindow(SettingsWindow))
        optionsmenu.add_command(label="History", command=lambda: self.newWindow(History))
        optionsmenu.add_command(label="Exit", command=self.master.destroy)
        mainmenu.add_cascade(label="Options", menu=optionsmenu)
        helpmenu = tk.Menu(mainmenu, tearoff=0)
        helpmenu.add_command(label="About", command=self.about)
        mainmenu.add_cascade(label="Help", menu=helpmenu)
        root.configure(menu=mainmenu)

    def connectDB(self):
        """Establishes a connection to database"""
        try:
            conn = sqlite3.connect("database")
            cursor = conn.cursor()
            cursor.execute(''' CREATE TABLE IF NOT EXISTS medicalbill(
                    invoice_no INT PRIMARY KEY UNIQUE NOT NULL,
                    customer CHAR(50) NOT NULL ,
                    address CHAR(150) NOT NULL ,
                    city CHAR(50) NOT NULL ,
                    state CHAR(50) NOT NULL ,
                    doctor CHAR(50) NOT NULL ,
                    purchage_data BLOB NOT NULL,
                    entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                ''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS user (srl INT PRIMARY KEY UNIQUE NOT NULL,
                           user CHAR(50) NOT NULL , 
                           password CHAR(150) NOT NULL
                );
                ''')
            cursor.execute(''' CREATE TABLE IF NOT EXISTS appdata(
                    srl INT PRIMARY KEY UNIQUE NOT NULL,
                    optional_label CHAR(50) NOT NULL ,
                    default_city CHAR(50) NOT NULL ,
                    default_state CHAR(50) NOT NULL ,
                    default_note CHAR(50) NOT NULL ,
                    table_label_1 CHAR(50) NOT NULL ,
                    print_heading CHAR(150) NOT NULL ,
                    busniess_name CHAR(150) NOT NULL ,
                    address_line1 CHAR(550) NOT NULL ,
                    address_line2 CHAR(550) NOT NULL ,
                    address_line3 CHAR(550) NOT NULL ,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                ''')
            cursor.execute("SELECT * FROM appdata;")
            output = cursor.fetchall()
            if not output:
                cursor.execute(
                    '''INSERT INTO appdata (srl,optional_label,default_city,default_state,default_note,table_label_1,
                    print_heading,busniess_name,address_line1,address_line2,address_line3) VALUES ('1','Notes',
                    'Jamshedpur','Jharkhand','Note:','Item Name','TAX INVOICE','EXAMPLE STORE','25/10 New market {
                    Near SBI ATM}, simarpali, Jamshedpur, pin-831010','Busniess timing: 8AM - 8PM {online delivery 
                    abailabe on phone. Call 999999999 for enquiry}','Tel- 0657 669 6652   Mobile- 999999999 / 
                    88888888888');''')
                conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            messagebox.showerror("ERROR", "Error creating Database")

    def prepare(self, data):
        data = data.replace("(", "{")
        data = data.replace(")", "}")
        data = data.replace("\'", "^")
        data = data.replace("\"", "")
        data = data.replace(";", "")
        data = data.replace("DELETE", "")
        data = data.replace("DROP", "")
        return data

    def prepareTable(self, data):
        preparedlist = []
        for list in data:
            list1 = []
            for data in list:
                data = data.replace("(", "{")
                data = data.replace(")", "}")
                data = data.replace("\'", "^")
                data = data.replace("\"", "")
                data = data.replace(";", "")
                data = data.replace("DELETE", "")
                data = data.replace("DROP", "")
                list1.append(data)
            preparedlist.append(list1)
        return preparedlist

    def recover(self, data):
        data = data.replace("{", "(")
        data = data.replace("}", ")")
        data = data.replace("^", "\'")
        return data

    def extractNumber(self, string):
        number = ""
        for char in string:
            if char == ".":
                number += char
            elif char.isnumeric():
                number += char
            else:
                pass
        return number

    def createButton(self, master=None, btntxt="Button", bg="sky blue", relief=tk.RAISED, bd=6, funcname=None,
                     side=None, padx=3, pady=3, anchor=None, ipadx=10, ipady=None, **kwargs):
        """
        To Create a button
        """
        kargs = {}
        for key, value in kwargs.items():
            kargs.__setitem__(key, value)
        btn = tk.Button(master, text=btntxt, command=funcname, bg=bg, relief=relief, bd=bd, **kargs)
        btn.pack(side=side, padx=padx, pady=pady, anchor=anchor, ipadx=ipadx, ipady=ipady)

    def createGridEntry(self, master=None, bg=None, variable=None, relief=tk.SUNKEN, bd=None, padx=None, pady=None,
                        ipady=None, ipadx=None, column=None, row=None, columnspan=None, rowspan=None, **kwargs):
        """
        To Create a entry
        """
        kargs = {}
        for key, value in kwargs.items():
            kargs.__setitem__(key, value)
        entry = tk.Entry(master, bg=bg, relief=relief, bd=bd, textvariable=variable, **kargs)
        entry.grid(ipadx=ipadx, ipady=ipady, padx=padx, pady=pady, columnspan=columnspan, rowspan=rowspan, row=row,
                   column=column)

    def createGridLabel(self, master=None, text="unknown", bg=None, relief=tk.SUNKEN, bd=None, padx=None, pady=None,
                        ipady=None, ipadx=None, column=None, row=None, columnspan=None, rowspan=None, **kwargs):
        """
        To Create a label
        """
        kargs = {}
        for key, value in kwargs.items():
            kargs.__setitem__(key, value)
        label = tk.Label(master, text=text, bg=bg, relief=relief, bd=bd, **kargs)
        label.grid(ipadx=ipadx, ipady=ipady, columnspan=columnspan, rowspan=rowspan, row=row, column=column)

    def showWidgets(self):
        self.master.cnx = sqlite3.connect("database")
        cursor = self.master.cnx.cursor()
        cursor.execute("SELECT * FROM appdata WHERE srl=1")
        for data in cursor:
            optional_label = data[1]
            default_city = data[2]
            default_state = data[3]
            default_note = data[4]
            table_label_1 = data[5]

        tk.Label(self.master, text="JENA Billing Systems", bg=self.master.theme, font="Magneto 30 bold", fg="navy",
                 bd=5, relief=tk.GROOVE).pack(pady=6, ipadx=6, ipady=5)
        frame1 = tk.Frame(self.master, bg=self.master.theme)
        frame1.pack(anchor="nw", padx=20, pady=25)
        # frame1 containts
        # Variables
        self.master.inv_no = tk.StringVar()
        self.master.customer_name = tk.StringVar()
        self.master.local_add = tk.StringVar()
        self.master.city = tk.StringVar()
        self.master.state = tk.StringVar()
        self.master.note = tk.StringVar()
        self.master.entry = {}  # For storing table
        # setting default values
        self.master.city.set(default_city)
        self.master.state.set(default_state)
        self.master.note.set(default_note)
        # Basic Details
        # laself
        self.createGridLabel(master=frame1, text="Invoice no :", font=self.master.font1, row=0, column=0,
                             width=self.master.labelwidth, bg=self.master.theme, anchor="e")
        self.createGridLabel(master=frame1, text="Customer Name :", font=self.master.font1, row=1, column=0,
                             width=self.master.labelwidth, bg=self.master.theme, anchor="e")
        self.createGridLabel(master=frame1, text="Address :", font=self.master.font1, row=2, column=0,
                             width=self.master.labelwidth, bg=self.master.theme, anchor="e")
        self.createGridLabel(master=frame1, text="City :", font=self.master.font1, row=3, column=0,
                             width=self.master.labelwidth, bg=self.master.theme, anchor="e")
        self.createGridLabel(master=frame1, text="State :", font=self.master.font1, row=4, column=0,
                             width=self.master.labelwidth, bg=self.master.theme, anchor="e")
        self.createGridLabel(master=frame1, text=optional_label, font=self.master.font1, row=5, column=0,
                             width=self.master.labelwidth, bg=self.master.theme, anchor="e")
        # Input Box
        self.createGridEntry(master=frame1, variable=self.master.inv_no, row=0, column=1, font=self.master.font1,
                             padx=self.master.padx, bd=3)
        self.createGridEntry(master=frame1, variable=self.master.customer_name, row=1, column=1, font=self.master.font1,
                             padx=self.master.padx, bd=3)
        self.createGridEntry(master=frame1, variable=self.master.local_add, row=2, column=1, font=self.master.font1,
                             padx=self.master.padx, bd=3)
        self.createGridEntry(master=frame1, variable=self.master.city, row=3, column=1, font=self.master.font1,
                             padx=self.master.padx, bd=3)
        self.createGridEntry(master=frame1, variable=self.master.state, row=4, column=1, font=self.master.font1,
                             padx=self.master.padx, bd=3)
        self.createGridEntry(master=frame1, variable=self.master.note, row=5, column=1, font=self.master.font1,
                             padx=self.master.padx, bd=3)
        tk.Button(frame1, text="Get invoice No", bg="RoyalBlue3", font=self.master.font1, fg="white",
                  command=self.setInvoiceNo).grid(row=0, column=2, padx=7)
        tk.Button(frame1, text="Load data from DB", bg="RoyalBlue3", font=self.master.font1, fg="white",
                  command=self.plotInvoice).grid(row=0, column=3, padx=7)
        # creating self.master.frame2 for taking medicine details
        self.master.frame2 = tk.Frame(self.master)
        self.master.frame2.pack(pady=15, anchor="w", padx=20)
        # self.master.frame2 containts
        # variables
        table_title = [("Srl", 0), (table_label_1, 1), ("Qty", 2), ("Unit Price", 3), ("Total", 4)]
        # important constants for table
        row = 4
        column = 10
        # creating entry table
        self.createTable(self.master.frame2, column, row)
        # creating table headers
        for text, col in table_title:
            self.createGridLabel(master=self.master.frame2, text=text, row=0, column=col, font=self.master.font1,
                                 relief=None)
        for row in range(1, 11):
            self.createGridLabel(master=self.master.frame2, text=str(row), row=row, column=0, font=self.master.font1,
                                 bd=None, relief=None)
        # Frame3 for action buttons
        frame3 = tk.Frame(self.master, bg=self.master.theme)
        frame3.pack(anchor="w", padx=10, pady=10)
        # frame3 containts
        # buttons
        self.createButton(frame3, "Create", side=tk.LEFT, font=self.master.font2, padx=10, ipadx=50,
                          funcname=self.createInvoice)
        self.createButton(frame3, "Print", side=tk.LEFT, font=self.master.font2, padx=10, ipadx=57,
                          funcname=self.printInvoice)
        self.createButton(frame3, "Close Window", side=tk.LEFT, font=self.master.font2, padx=10, ipadx=20,
                          funcname=self.master.destroy)

    def setInvoiceNo(self):
        inv = self.getInvoiceNo()
        self.master.inv_no.set(str(inv))

    def getInvoiceNo(self):
        """It connect to database then fetch the last invoice number and return next invoice number"""
        try:
            cursor = self.master.cnx.cursor()
            query = '''SELECT * FROM medicalbill ORDER BY invoice_no DESC LIMIT 1'''
            cursor.execute(query)
            list = cursor.fetchall()  # retuns a list of tupples(each result in a tuple).
            if not list:
                lastinv = "1001"
            else:
                l = 1
                for row in list:
                    if l == 1:
                        inv = row[0]
                        l += 1
                    else:
                        continue
                lastinv = inv + 1
            cursor.close()
        except:
            messagebox.showerror("Error", "Internal Error")
        return lastinv

    def calTotal(self, event):
        """Multiply qty with price and return value"""
        # Requesting Table
        table = self.getTable()
        # Extracting qty and unit price information from table
        # Making list of tuples (qty,price) format
        data = []
        for val in range(10):
            data.append((self.extractNumber(table[val][1]), self.extractNumber(table[val][2])))
        # calculating total
        total = []
        for qty, price in data:
            if qty == "" or price == "":
                total.append("")
            else:
                total.append(float(qty) * float(price))
        # Displaying total on screen
        for row in range(1, 11):
            for column in range(4, 5):
                index = (row, column)
                self.master.entry[index].delete(0, tk.END)
                self.master.entry[index].insert(0, str(total[row - 1]))

    def getTable(self, row=10, column=4):
        """Return a list of lists, containing the data inside the table"""
        rows = row + 1
        columns = column + 1
        result = []
        for row in range(1, rows):
            current_row = []
            for column in range(1, columns):
                index = (row, column)
                current_row.append(self.master.entry[index].get())
            result.append(current_row)
        return result

    def createTable(self, master, row=4, column=10):
        """
        Plot series of input boxes on GUI and store all addresses in entry dictionary which is a global variable.
        Note: Alter the value of row and column(Beacuse master of this grid managed by pack manager)
        """
        rows = row + 1  # leaving space for labels eg: medicine name,qty,rate,total
        columns = column + 1  # leaving space for labels eg: srl,1,2,3....
        # create the table of widgets
        for row in range(1, rows):
            for column in range(1, columns):
                index = (row, column)
                e = tk.Entry(self.master.frame2, font=self.master.font2)
                e.grid(row=row, column=column, stick="nsew")
                e.bind("<FocusIn>", self.calTotal)
                self.master.entry[index] = e
        # adjust column weights so they all expand equally
        for column in range(columns):
            master.grid_columnconfigure(column, weight=1)
        # designate a final, empty row to fill up any extra space
        master.grid_rowconfigure(rows, weight=1)

    def commitDB(self, query):
        cursor = self.master.cnx.cursor()
        cursor.execute(query)
        self.master.cnx.commit()

    def checkDuplicateInvoice(self, invoice):
        cursor = self.master.cnx.cursor()
        query = f"SELECT * FROM medicalbill WHERE invoice_no={invoice}"
        cursor.execute(query)
        row = cursor.fetchall()
        cursor.close()
        if row:
            return True  # duplicate exist
        else:
            return False

    def totalInvoiceValue(self):
        """Retuns total invoice value"""
        table = self.getTable()
        total = "0"
        for row in range(10):
            for column in range(3, 4):
                # total+=int(table[row][column])
                val = table[row][column]
                if val == "":
                    total += "+0"
                else:
                    total += "+" + val
        # Evaluating concatinated  string data eg. "1+2+3+4" will be evaluated as 10.
        total = eval(total)
        return str(total)

    def clearEntries(self, row=10, column=4):
        """Clear Previous entries"""
        rows = row + 1
        columns = column + 1
        self.master.customer_name.set("")
        self.master.local_add.set("")
        self.master.note.set("Dr. ")
        for row in range(1, rows):
            for column in range(1, columns):
                index = (row, column)
                self.master.entry[index].delete(0, 'end')

    def encodeList(self, list):
        """Encoding algorithm of list for database entry"""
        string = str(list)
        prepared_data = ""
        for char in string:
            if char == "\'":
                prepared_data += '\\'
            else:
                prepared_data += char
        return prepared_data

    def decodeList(self, str):
        """decoding algorithm for encoded list"""
        list = str.replace("\\", "\'")
        list = literal_eval(list)  # convering string to list
        return list

    def plotInvoice(self):
        """Recreate invoice from invoice number. It connect to data base and fetch respective data from database."""
        try:
            inv = self.master.inv_no.get()
            cursor = self.master.cnx.cursor()
            query = f"SELECT * FROM `medicalbill` where invoice_no={inv}"
            cursor.execute(query)
            row = cursor.fetchall()
            if row:
                self.clearEntries()
                cursor.execute(query)
                for data in cursor:
                    self.master.customer_name.set(self.recover(data[1]))
                    self.master.local_add.set(self.recover(data[2]))
                    self.master.city.set(self.recover(data[3]))
                    self.master.state.set(self.recover(data[4]))
                    self.master.note.set(self.recover(data[5]))
                    decoded_list = self.decodeList(self.recover(data[6]))
                    self.setTable(decoded_list)
            else:
                messagebox.showerror("Error", "No Entry Found on database!!!")
                cursor.close()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Please Enter a Value.\nIf value entered, Please check database connection.")

    def createInvoice(self):
        """Create a invoice without printing"""
        try:
            self.pushInvoice()
        except Exception as e:
            print(e)
            messagebox.showerror("error", "Internal Error")
        else:
            self.setInvoiceNo()

    def validateForm(self):
        """Form Validation"""
        invoice = self.master.inv_no.get()
        customer = self.master.customer_name.get()
        table = self.getTable()
        count = 1
        if invoice == "":
            messagebox.showwarning("Information", "Invoice Number Required!")
            return False
        elif customer == "":
            messagebox.showwarning("Information", "Customer Name Required!")
            return False
        elif table[0][0] == "":
            messagebox.showwarning("Information", "Atleast 1 Item Required!")
            return False
        elif count == 1:
            rowcount = 1
            for row in table:
                if row[0] != "":
                    if row[1] == "" or row[2] == "" or row[3] == "":
                        messagebox.showwarning("Information", f"Fill all details in Row No-{rowcount}")
                        return False
                rowcount += 1
            return True

    def pushInvoice(self):
        """It push invoice data entered by user to database"""
        invoice = self.getInvoiceNo()
        if self.checkDuplicateInvoice(invoice):
            messagebox.showerror("Error", "Duplicate Entry Found")
        elif self.validateForm():
            customer = self.master.customer_name.get()
            customer = self.prepare(customer)
            purchage_data = self.getTable()
            purchage_data = self.prepareTable(purchage_data)
            c_address = self.master.local_add.get()
            c_address = self.prepare(c_address)
            c_city = self.master.city.get()
            c_city = self.prepare(c_city)
            c_state = self.master.state.get()
            c_state = self.prepare(c_state)
            doc = self.master.note.get()
            doc = self.prepare(doc)
            # encoding list data to insert into db
            prepared_data = self.encodeList(purchage_data)
            try:
                self.commitDB(
                    query=f"INSERT INTO medicalbill (invoice_no,customer, address, city, state, doctor, purchage_data) VALUES ('{invoice}','{customer}', '{c_address}', '{c_city}', '{c_state}', '{doc}', '{prepared_data}')")
                messagebox.showinfo("Information", "Invoice Created")
            except Exception as e:
                print(e)
                messagebox.showerror("Error", "Error Creating Invoice Entry")
            else:
                self.clearEntries()
        else:
            pass

    def setTable(self, list, row=10, column=4):
        """Set the value of table from list generated by getTable method"""
        rows = row + 1
        columns = column + 1
        for row in range(1, rows):
            for column in range(1, columns):
                index = (row, column)
                self.master.entry[index].insert(0, list[(row - 1)][column - 1])

    def printInvoice(self):
        """calls print preview window"""
        invoice = self.master.inv_no.get()
        if self.checkDuplicateInvoice(invoice):
            ans = messagebox.askyesno("Question", "Invoice Already exist.\n Do you want to print DUPLICATE Invoice?")
            if ans:
                customer = self.master.customer_name.get()
                c_address = self.master.local_add.get()
                c_city = self.master.city.get()
                c_state = self.master.state.get()
                doc = self.master.note.get()
                purchage_data = self.getTable()
                total = self.totalInvoiceValue()
                dictionary = {
                    "invoice": invoice,
                    "customer": customer,
                    "c_address": c_address,
                    "c_city": c_city,
                    "c_state": c_state,
                    "doc": doc,
                    "purchage_data": purchage_data,
                    "total": total,
                }
                self.printWindow(PrintWindow, dictionary)
            else:
                pass
        else:
            customer = self.master.customer_name.get()
            c_address = self.master.local_add.get()
            c_city = self.master.city.get()
            c_state = self.master.state.get()
            doc = self.master.note.get()
            purchage_data = self.getTable()
            total = self.totalInvoiceValue()
            dictionary = {
                "invoice": invoice,
                "customer": customer,
                "c_address": c_address,
                "c_city": c_city,
                "c_state": c_state,
                "doc": doc,
                "purchage_data": purchage_data,
                "total": total,
            }
            self.pushInvoice()
            self.printWindow(PrintWindow, dictionary)

    def printWindow(self, _class, dictionary):
        """Open a Printing preview window"""
        self.win = tk.Toplevel(self.master)
        _class(self.win, dictionary)

    def newWindow(self, _class):
        """Open a Application window"""
        self.win = tk.Toplevel(self.master)
        _class(self.win)

    def statusBar(self):
        """
        To show status at buttom of GUI
        """
        self.master.status = tk.StringVar()
        self.master.status.set("Ready")
        frame = tk.Frame(self.master, bg="grey69")
        frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(frame, text="Degined and Developed by: Sridhar JENA", bg="grey69", font="Forte 12 bold", anchor="e",
                 relief=tk.RIDGE, bd=3, fg="medium violet red").pack(side=tk.RIGHT, anchor="e")
        self.master.sbar = tk.Label(frame, textvariable=self.master.status, relief=tk.RIDGE, font="Arial 13 normal",
                                    anchor="w", bg="grey92")
        self.master.sbar.pack(fill=tk.X)

    def updateStatus(self, state="Ready", freeze=0):
        """
        To update status of GUI
        """
        self.master.status.set(state)
        self.master.sbar.update()
        if freeze > 0:
            time.sleep(freeze)


class PrintWindow(MainWindow):
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
            self.master.iconbitmap("print.ico")
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
        self.master.cnx = sqlite3.connect("database")
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
            self.canvas.postscript(file="tmp.ps", colormode='color')
            self.master.update()
            file = asksaveasfilename(initialfile=f"{self.master.invoice}.pdf", defaultextension=".pdf",
                                     filetypes=[("All Files", "*.*"), ("PDF Documents", "*.pdf")])
            process = subprocess.Popen(["ps2pdf", "tmp.ps", file], shell=True)
            process.wait()

        except:
            messagebox.showerror("Error",
                                 "This Program require ghostscript to run properly.\n You can istall ghostscript from "
                                 "<https://ghostscript.com/download/gsdnld.html>.\n If you are in windows and have "
                                 "chocolaty installed. issue command <choco install ghostscript> to install. After "
                                 "installation add it's bin and lb file to path.")
    def printData(self):
        try:
            self.canvas.postscript(file="tmp.ps", colormode='color')
            process = subprocess.Popen(["ps2pdf", "tmp.ps", "temp.pdf"], shell=True)
            process.wait()
            os.startfile("temp.pdf", "print")

        except:
            messagebox.showerror("Error",
                                 "This Program require ghostscript to run properly.\n You can istall ghostscript from "
                                 "<https://ghostscript.com/download/gsdnld.html>.\n If you are in windows and have "
                                 "chocolaty installed. issue command <choco install ghostscript> to install. After "
                                 "installation add it's bin and lb file to path.")


class SettingsWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry("750x500+0+0")
        self.master.title("Settings")
        self.master.theme = "grey50"
        self.master.config(bg="grey50")
        try:
            self.master.iconbitmap("settings.ico")
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
            self.master.iconbitmap("history.ico")
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
            spinner.load('spinner2.gif')
            start = start_date.get_date()
            end = end_date.get_date()
            for i in tree.get_children():
                tree.delete(i)
            start = start.strftime("%Y-%m-%d %H:%M:%S")
            end = end + timedelta(days=1)
            end = end.strftime("%Y-%m-%d %H:%M:%S")
            cnx = sqlite3.connect("database")
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


# Main Program
if __name__ == "__main__":
    # Program Start
    root = tk.Tk()
    app = MainWindow(root)

    root.mainloop()
