from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("AITventory | Inventory Management System Developed by Allen")
        self.root.config(bg = "white")
        self.root.focus_force()

        # Variables
        self.var_searchby = StringVar()
        self.var_searchtext = StringVar()
        
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        # Search Frame
        # Options
        label_search = Label(self.root, text = "Invoice No.", bg = "white", font = ("goudy old style", 15))
        label_search.place(x = 700, y = 80)

        text_search = Entry(self.root, textvariable = self.var_searchtext, font = ("goudy old style", 15), bg = "lightyellow").place(x = 830, y = 80, width = 130)
        button_search = Button(self.root, text = "Search", command = self.search, font = ("goudy old style", 15), bg = "#4CAF50", fg = "white", cursor = "hand2").place(x = 980, y = 79, width = 100, height = 28)

        # Title
        title = Label(self.root, text = "Manage Supplier Details", font = ("goudy old style", 20, "bold"), bg = "#0F4D7D", fg = "white").place(x = 50, y = 10, width = 1000, height = 40)

        # Content
        # Row 1
        label_supplier_invoice = Label(self.root, text = "Invoice No.", font = ("goudy old style", 15),bg = "white").place(x = 50, y = 80)
        text_supplier_invoice = Entry(self.root, textvariable = self.var_sup_invoice, font = ("goudy old style", 15),bg = "lightyellow").place(x = 180, y = 80, width = 180)
        
        # Row 2
        label_name = Label(self.root, text = "Name", font = ("goudy old style", 15),bg = "white").place(x = 50, y = 120)           
        text_name = Entry(self.root, textvariable = self.var_name, font = ("goudy old style", 15),bg = "lightyellow").place(x = 180, y = 120, width = 180)
        
        # Row 3
        label_contact = Label(self.root, text = "Contact", font = ("goudy old style", 15),bg = "white").place(x = 50, y = 160)        
        text_contact = Entry(self.root, textvariable = self.var_contact, font = ("goudy old style", 15),bg = "lightyellow").place(x = 180, y = 160, width = 180)

        # Row 4
        label_desc = Label(self.root, text = "Description", font = ("goudy old style", 15),bg = "white").place(x = 50, y = 200)   
        self.text_desc = Text(self.root, font = ("goudy old style", 15),bg = "lightyellow")
        self.text_desc.place(x = 180, y = 200, width = 470, height = 90)
        
        # Buttons
        button_add = Button(self.root, text = "Save", command = self.add, font = ("goudy old style", 15), bg = "#2196F3", fg = "white", cursor = "hand2").place(x = 180, y = 370, width = 110, height = 35)
        button_update = Button(self.root, text = "Update", command = self.update, font = ("goudy old style", 15), bg = "#4CAF50", fg = "white", cursor = "hand2").place(x = 300, y = 370, width = 110, height = 35)
        button_delete = Button(self.root, text = "Delete", command = self.delete, font = ("goudy old style", 15), bg = "#F44336", fg = "white", cursor = "hand2").place(x = 420, y = 370, width = 110, height = 35)
        button_clear = Button(self.root, text = "Clear", command = self.clear, font = ("goudy old style", 15), bg = "#607D8B", fg = "white", cursor = "hand2").place(x = 540, y = 370, width = 110, height = 35)

        # Supplier Details
        sup_frame = Frame(self.root, bd = 3, relief = RIDGE)
        sup_frame.place(x = 700, y = 120, width = 380, height = 350)

        scroll_y = Scrollbar(sup_frame, orient = VERTICAL)
        scroll_x = Scrollbar(sup_frame, orient = HORIZONTAL)

        self.SupplierTable = ttk.Treeview(sup_frame, columns = ("invoice", "name", "contact", "desc"), yscrollcommand = scroll_y.set, xscrollcommand = scroll_x.set)
        scroll_x.pack(side = BOTTOM, fill = X)
        scroll_y.pack(side = RIGHT, fill = Y)
        scroll_x.config(command = self.SupplierTable.xview)
        scroll_y.config(command = self.SupplierTable.yview)

        self.SupplierTable.heading("invoice", text = "Invoice No.")
        self.SupplierTable.heading("name", text = "Name")
        self.SupplierTable.heading("contact", text = "Contact")
        self.SupplierTable.heading("desc", text = "Description")

        self.SupplierTable["show"] = "headings"

        self.SupplierTable.column("invoice", width = 100)
        self.SupplierTable.column("name", width = 100)
        self.SupplierTable.column("contact", width = 100)
        self.SupplierTable.column("desc", width = 100)
        self.SupplierTable.pack(fill = BOTH, expand = 1)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def add(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice is required.", parent = self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice = ?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Invoice No. already assigned, try different.", parent = self.root)
                else:
                    cur.execute("INSERT INTO supplier (invoice , name, contact, desc) values(?, ?, ?, ?)", (
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.text_desc.get('1.0', END),
                    ))
                    con.commit()
                    messagebox.showerror("Success", "Supplier added succesfully", parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def show(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('', END, values = row) 
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def get_data(self, ev):
        f = self.SupplierTable.focus()
        content = (self.SupplierTable.item(f))
        row = content['values']

        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.text_desc.delete('1.0', END)
        self.text_desc.insert(END, row[3])

    def update(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice no. is required.", parent = self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice = ?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice no.", parent = self.root)
                else:
                    cur.execute("UPDATE supplier SET name = ?, contact = ?, desc = ? WHERE invoice = ?", (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.text_desc.get('1.0', END),
                        self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showerror("Success", "Supplier updated succesfully.", parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def delete(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. is required.", parent = self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice = ?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent = self.root)
                    if op == True:
                        cur.execute("DELETE FROM supplier WHERE invoice = ?", (self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Supplier deleted successfully.", parent = self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.text_desc.delete('1.0', END)
        self.var_searchtext.set("")
        
        self.show()

    def search(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.var_searchtext.get() == "":
                messagebox.showerror("Error", "Invoice no. is required.", parent = self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice = ?", (self.var_searchtext.get(),))
                row = cur.fetchone()
                if row != None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('', END, values = row) 
                else:
                    messagebox.showerror("Error", "No record found.", parent = self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)
 
if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()