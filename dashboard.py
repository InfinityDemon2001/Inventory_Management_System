from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
import os
import time

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("AITventory | Inventory Management System Developed by Allen")
        self.root.config(bg = "white")

        # Title
        self.icon_title = PhotoImage(file = "images/logo1.png")
        title = Label(self.root, text = "AITventory", image = self.icon_title, compound = LEFT, font = ("times new roman", 40, "bold"), bg = "#010C48", fg = "white", anchor = "w", padx = 20).place(x = 0, y = 0, relwidth = 1, height = 70)

        # Button Logout
        button_logout = Button(self.root, text = "Logout", command = self.logout, font = ("times new roman", 15, "bold"), bg = "yellow", cursor = "hand2").place(x = 1150, y = 10, height = 50, width = 150)

        # Clock
        self.label_clock = Label(self.root, text = "Welcome to AITventory\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS", font = ("times new roman", 15), bg = "#4D636D", fg = "white")
        self.label_clock.place(x = 0, y = 70, relwidth = 1, height = 30)

        # Left Menu
        self.MenuLogo = Image.open("images/menu_im.png")
        self.MenuLogo = self.MenuLogo.resize((200, 200), Image.Resampling.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        leftMenu = Frame(self.root, bd = 2, relief = RIDGE, bg = "white")
        leftMenu.place(x = 0, y = 102, width = 200, height = 565)

        labelMenuLogo = Label(leftMenu, image = self.MenuLogo)
        labelMenuLogo.pack(side = TOP, fill = X)

        self.icon_side = PhotoImage(file = "images/side.png")
        labelMenu = Label(leftMenu, text = "Menu", font = ("times new roman", 20), bg = "#009688").pack(side = TOP, fill = X)

        button_employee = Button(leftMenu, text = "Employee", command = self.employee, image = self.icon_side, compound = LEFT, padx = 5, anchor = "w", font = ("times new roman", 20, "bold"), bg = "white", bd = 3, cursor = "hand2").pack(side = TOP, fill = X)
        button_supplier = Button(leftMenu, text = "Supplier", command = self.supplier, image = self.icon_side, compound = LEFT, padx = 5, anchor = "w", font = ("times new roman", 20, "bold"), bg = "white", bd = 3, cursor = "hand2").pack(side = TOP, fill = X)
        button_category = Button(leftMenu, text = "Category", command = self.category, image = self.icon_side, compound = LEFT, padx = 5, anchor = "w", font = ("times new roman", 20, "bold"), bg = "white", bd = 3, cursor = "hand2").pack(side = TOP, fill = X)
        button_product = Button(leftMenu, text = "Product", command = self.product, image = self.icon_side, compound = LEFT, padx = 5, anchor = "w", font = ("times new roman", 20, "bold"), bg = "white", bd = 3, cursor = "hand2").pack(side = TOP, fill = X)
        button_sales = Button(leftMenu, text = "Sales", command = self.sales, image = self.icon_side, compound = LEFT, padx = 5, anchor = "w", font = ("times new roman", 20, "bold"), bg = "white", bd = 3, cursor = "hand2").pack(side = TOP, fill = X)
        button_exit = Button(leftMenu, text = "Exit", image = self.icon_side, compound = LEFT, padx = 5, anchor = "w", font = ("times new roman", 20, "bold"), bg = "white", bd = 3, cursor = "hand2").pack(side = TOP, fill = X)

        # Content
        self.label_employee = Label(self.root, text = "Total Employees\n[ 0 ]", bd = 5, relief = RIDGE, bg = "#33BBF9", fg = "white", font = ("goudy old style", 20, "bold"))
        self.label_employee.place(x = 300, y = 120, height = 150, width = 300)

        self.label_supplier = Label(self.root, text = "Total Suppliers\n[ 0 ]", bd = 5, relief = RIDGE, bg = "#FF5722", fg = "white", font = ("goudy old style", 20, "bold"))
        self.label_supplier.place(x = 650, y = 120, height = 150, width = 300)

        self.label_category = Label(self.root, text = "Total Categories\n[ 0 ]", bd = 5, relief = RIDGE, bg = "#009688", fg = "white", font = ("goudy old style", 20, "bold"))
        self.label_category.place(x = 1000, y = 120, height = 150, width = 300)

        self.label_product = Label(self.root, text = "Total Products\n[ 0 ]", bd = 5, relief = RIDGE, bg = "#607D8B", fg = "white", font = ("goudy old style", 20, "bold"))
        self.label_product.place(x = 300, y = 300, height = 150, width = 300)

        self.label_sales = Label(self.root, text = "Total Sales\n[ 0 ]", bd = 5, relief = RIDGE, bg = "#FFC107", fg = "white", font = ("goudy old style", 20, "bold"))
        self.label_sales.place(x = 650, y = 300, height = 150, width = 300)

        # Footer
        label_footer = Label(self.root, text = "AITventory-Inventory Management System | Developed by Allen\nFor any Technical Issue Contact: 8929718053", font = ("times new roman", 12), bg = "#4D636D", fg = "white").pack(side = BOTTOM, fill = X)

        self.update_content()

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            product = cur.fetchall()
            self.label_product.config(text = f"Total Products\n[ {str(len(product))} ]")

            cur.execute("SELECT * FROM supplier")
            supplier = cur.fetchall()
            self.label_supplier.config(text = f"Total Suppliers\n[ {str(len(supplier))} ]")

            cur.execute("SELECT * FROM category")
            category = cur.fetchall()
            self.label_category.config(text = f"Total Categories\n[ {str(len(category))} ]")

            cur.execute("SELECT * FROM employee")
            employee = cur.fetchall()
            self.label_employee.config(text = f"Total Employees\n[ {str(len(employee))} ]")

            bill = len(os.listdir('bill'))
            self.label_sales.config(text = f"Total Sales\n[ {str(bill)} ]")

            time_ = time.strftime("%H:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.label_clock.config(text = f"Welcome to AITventory\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.label_clock.after(200, self.update_content)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")
 
if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()