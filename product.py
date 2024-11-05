from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("AITventory | Inventory Management System Developed by Allen")
        self.root.config(bg = "white")
        self.root.focus_force()

        # Variables
        self.var_searchby = StringVar()
        self.var_searchtext = StringVar()

        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sup()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        productFrame = Frame(self.root, bd = 2, relief = RIDGE)
        productFrame.place(x = 10, y = 10, width = 450, height = 480)

        # Title
        title = Label(productFrame, text = "Manage Product Details", font = ("goudy old style", 18), bg = "#0F4D7D", fg = "white").pack(side = TOP, fill = X)

        # Column 1
        label_category = Label(productFrame, text = "Category", font = ("goudy old style", 18), bg = "white").place(x = 30, y = 60)
        label_supplier = Label(productFrame, text = "Supplier", font = ("goudy old style", 18), bg = "white").place(x = 30, y = 110)
        label_name = Label(productFrame, text = "Name", font = ("goudy old style", 18), bg = "white").place(x = 30, y = 160)
        label_price = Label(productFrame, text = "Price", font = ("goudy old style", 18), bg = "white").place(x = 30, y = 210)
        label_quantity = Label(productFrame, text = "Quantity", font = ("goudy old style", 18), bg = "white").place(x = 30, y = 260)
        label_status = Label(productFrame, text = "Status", font = ("goudy old style", 18), bg = "white").place(x = 30, y = 310)

        # Column 2
        cmb_cat = ttk.Combobox(productFrame, textvariable = self.var_cat, values = self.cat_list, state = 'readonly', justify = CENTER, font = ("goudy old style", 15))
        cmb_cat.place(x = 150, y = 60, width = 200)
        cmb_cat.current(0)

        cmb_sup = ttk.Combobox(productFrame, textvariable = self.var_sup, values = self.sup_list, state = 'readonly', justify = CENTER, font = ("goudy old style", 15))
        cmb_sup.place(x = 150, y = 110, width = 200)
        cmb_sup.current(0)

        text_name = Entry(productFrame, textvariable = self.var_name, font = ("goudy old style", 15), bg = "lightyellow").place(x = 150, y = 160, width = 200)
        text_price = Entry(productFrame, textvariable = self.var_price, font = ("goudy old style", 15), bg = "lightyellow").place(x = 150, y = 210, width = 200)
        text_qauntity = Entry(productFrame, textvariable = self.var_qty, font = ("goudy old style", 15), bg = "lightyellow").place(x = 150, y = 260, width = 200)

        cmb_status = ttk.Combobox(productFrame, textvariable = self.var_status, values = ("Active", "Inactive"), state = 'readonly', justify = CENTER, font = ("goudy old style", 15))
        cmb_status.place(x = 150, y = 310, width = 200)
        cmb_status.current(0)

        # Buttons
        button_add = Button(productFrame, text = "Save", command = self.add, font = ("goudy old style", 15), bg = "#2196F3", fg = "white", cursor = "hand2").place(x = 10, y = 400, width = 100, height = 40)
        button_update = Button(productFrame, text = "Update", command = self.update, font = ("goudy old style", 15), bg = "#4CAF50", fg = "white", cursor = "hand2").place(x = 120, y = 400, width = 100, height = 40)
        button_delete = Button(productFrame, text = "Delete", command = self.delete, font = ("goudy old style", 15), bg = "#F44336", fg = "white", cursor = "hand2").place(x = 230, y = 400, width = 100, height = 40)
        button_clear = Button(productFrame, text = "Clear", command = self.clear, font = ("goudy old style", 15), bg = "#607D8B", fg = "white", cursor = "hand2").place(x = 340, y = 400, width = 100, height = 40)

        # Search Frame
        searchFrame = LabelFrame(self.root, text = "Search Product", font = ("goudy old style", 12, "bold"), bd = 2, relief = RIDGE, bg = "white")
        searchFrame.place(x = 480, y = 10, width = 600, height = 80)

        # Options
        cmb_search = ttk.Combobox(searchFrame, textvariable = self.var_searchby, values = ("Select", "Category", "Supplier", "Name"), state = 'readonly', justify = CENTER, font = ("goudy old style", 15))
        cmb_search.place(x = 10, y = 10, width = 180)
        cmb_search.current(0)

        text_search = Entry(searchFrame, textvariable = self.var_searchtext, font = ("goudy old style", 15), bg = "lightyellow").place(x = 200, y = 10)
        button_search = Button(searchFrame, text = "Search", command = self.search, font = ("goudy old style", 15), bg = "#4CAF50", fg = "white", cursor = "hand2").place(x = 410, y = 9, width = 150, height = 30)

        # Product Details
        p_frame = Frame(self.root, bd = 3, relief = RIDGE)
        p_frame.place(x = 480, y = 100, width = 600, height = 390)

        scroll_y = Scrollbar(p_frame, orient = VERTICAL)
        scroll_x = Scrollbar(p_frame, orient = HORIZONTAL)

        self.ProductTable = ttk.Treeview(p_frame, columns = ("pid", "category", "supplier", "name", "price", "qty", "status"), yscrollcommand = scroll_y.set, xscrollcommand = scroll_x.set)
        scroll_x.pack(side = BOTTOM, fill = X)
        scroll_y.pack(side = RIGHT, fill = Y)
        scroll_x.config(command = self.ProductTable.xview)
        scroll_y.config(command = self.ProductTable.yview)
        self.ProductTable.heading("pid", text = "Product ID")
        self.ProductTable.heading("category", text = "Category")
        self.ProductTable.heading("supplier", text = "Supplier")
        self.ProductTable.heading("name", text = "Name")
        self.ProductTable.heading("price", text = "Price")
        self.ProductTable.heading("qty", text = "Quantity")
        self.ProductTable.heading("status", text = "Status")

        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width = 100)
        self.ProductTable.column("category", width = 100)
        self.ProductTable.column("supplier", width = 100)
        self.ProductTable.column("name", width = 100)
        self.ProductTable.column("price", width = 100)
        self.ProductTable.column("qty", width = 100)
        self.ProductTable.column("status", width = 100)
        self.ProductTable.pack(fill = BOTH, expand = 1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # Functions
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            cat = cur.fetchall()
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("SELECT name FROM supplier")
            sup = cur.fetchall()
            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)
    
    def add(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or self.var_sup.get() == "Select" or self.var_sup.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "All the fields must be filled.", parent = self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name = ?", (self.var_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Product already present, try different", parent = self.root)
                else:
                    cur.execute("INSERT INTO product (category, supplier, name, price, qty, status) VALUES(?, ?, ?, ?, ?, ?)", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showerror("Success", "Product added succesfully", parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def show(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values = row) 
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])

    def update(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select product from the list.", parent = self.root)
            else:
                cur.execute("SELECT * FROM product WHERE pid = ?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product.", parent = self.root)
                else:
                    cur.execute("UPDATE product SET category = ?, supplier = ?, name = ?, price = ?, qty = ?, status = ? WHERE pid = ?", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showerror("Success", "Product updated succesfully", parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def delete(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select product from the list.", parent = self.root)
            else:
                cur.execute("SELECT * FROM product WHERE pid = ?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product.", parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent = self.root)
                    if op == True:
                        cur.execute("DELETE FROM product WHERE pid = ?", (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Product deleted successfully.", parent = self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")

        self.var_searchtext.set("")
        self.var_searchby.set("Select")
        
        self.show()

    def search(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By option", parent = self.root)
            elif self.var_searchtext.get() == "":
                messagebox.showerror("Error", "Search input is required.", parent = self.root)
            else:
                cur.execute("SELECT * FROM product WHERE " + self.var_searchby.get() + " LIKE '%"+self.var_searchtext.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values = row) 
                else:
                    messagebox.showerror("Error", "No record found.", parent = self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()