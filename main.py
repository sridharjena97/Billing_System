import sqlite3
import time
import tkinter as tk
from ast import literal_eval
from tkinter import messagebox
from datetime import datetime
from printwindow import PrintWindow
from settings import SettingsWindow
from history import History
# TODO: create data visualization window


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
            self.master.iconbitmap("images/icon.ico")
        except:
            pass
        self.connectDB()
        self.showWidgets()
        self.statusBar()
        self.menubar()

    def about(self):
        """Shows information about the application"""
        messagebox.showinfo("About",
                            "Developed By: Sridhar Jena. \n\nThis software is sole property of SRIDHWORK. Selling "
                            "copy of this software is strictly prohibited.\nUse at your own risk.\nFor any "
                            "query/customization, please contact sridhwork@gmail.com. \n\n© SridhWork 2020 all rights "
                            "reserved.")

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
                    print_heading,busniess_name,address_line1,address_line2,address_line3) VALUES ('1','Notes', 'Jamshedpur','Jharkhand','Note:','Item Name','TAX INVOICE','EXAMPLE STORE','25/10 New market {Near SBI ATM}, simarpali, Jamshedpur, pin-831010','Busniess timing: 8AM - 8PM {online delivery abailabe on phone. Call 999999999 for enquiry}','Tel- 0657 669 6652   Mobile- 999999999 / 88888888888');''')
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
            current_time = datetime.now()
            current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            # encoding list data to insert into db
            prepared_data = self.encodeList(purchage_data)
            try:
                self.commitDB(
                    query=f"INSERT INTO medicalbill (invoice_no,customer, address, city, state, doctor, purchage_data, "
                          f"entry_time) VALUES ('{invoice}','{customer}', '{c_address}', '{c_city}', '{c_state}', "
                          f"'{doc}', '{prepared_data}', '{current_time}')")
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


# Main Program
if __name__ == "__main__":
    # Program Start
    root = tk.Tk()
    app = MainWindow(root)

    root.mainloop()
