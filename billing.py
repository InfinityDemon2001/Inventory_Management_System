from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile
import subprocess

class billClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("AITventory | Inventory Management System Developed by Allen")
        self.root.config(bg = "white")
        self.cart_list = []
        self.chk_print = 0

        # Title
        self.icon_title = PhotoImage(file = "images/logo1.png")
        title = Label(self.root, text = "AITventory", image = self.icon_title, compound = LEFT, font = ("times new roman", 40, "bold"), bg = "#010C48", fg = "white", anchor = "w", padx = 20).place(x = 0, y = 0, relwidth = 1, height = 70)

        # Button Logout
        button_logout = Button(self.root, text = "Logout", command = self.logout, font = ("times new roman", 15, "bold"), bg = "yellow", cursor = "hand2").place(x = 1150, y = 10, height = 50, width = 150)

        # Clock
        self.label_clock = Label(self.root, text = "Welcome to AITventory\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS", font = ("times new roman", 15), bg = "#4D636D", fg = "white")
        self.label_clock.place(x = 0, y = 70, relwidth = 1, height = 30)

        # Product Frame
        productFrame1 = Frame(self.root, bd = 4, relief = RIDGE, bg = "white")
        productFrame1.place(x = 6, y = 110, width = 410, height = 550)

        p_title = Label(productFrame1, text = "All Products", font = ("goudy old style", 20, "bold"), bg = "#262626", fg = "white").pack(side = TOP, fill = X)

        # Product Search Frame
        self.var_search = StringVar()

        productFrame2 = Frame(productFrame1, bd = 2, relief = RIDGE, bg = "white")
        productFrame2.place(x = 2, y = 42, width = 398, height = 90)

        label_search = Label(productFrame2, text = "Search Product | By Name", font = ("times new roman", 15, "bold"), bg = "white", fg = "green").place(x = 2, y = 5)

        label_search = Label(productFrame2, text = "Product Name", font = ("times new roman", 15, "bold"), bg = "white").place(x = 2, y = 45)
        text_search = Entry(productFrame2, textvariable = self.var_search, font = ("times new roman", 15), bg = "lightyellow").place(x = 128, y = 47, width = 150, height = 22)
        button_search = Button(productFrame2, text = "Search", command = self.search, font = ("goudy old style", 15), bg = "#2196F3", fg = "white", cursor = "hand2").place(x = 285, y = 45, width = 100, height = 25)
        button_show_all = Button(productFrame2, text = "Show All", command = self.show, font = ("goudy old style", 15), bg = "#083531", fg = "white", cursor = "hand2").place(x = 285, y = 10, width = 100, height = 25)

        # Product Detail Frame
        product_frame3 = Frame(productFrame1, bd = 3, relief = RIDGE)
        product_frame3.place(x = 2, y = 140, width = 398, height = 375)

        scroll_y = Scrollbar(product_frame3, orient = VERTICAL)
        scroll_x = Scrollbar(product_frame3, orient = HORIZONTAL)

        self.ProductTable = ttk.Treeview(product_frame3, columns = ("pid", "name", "price", "qty", "status"), yscrollcommand = scroll_y.set, xscrollcommand = scroll_x.set)
        scroll_x.pack(side = BOTTOM, fill = X)
        scroll_y.pack(side = RIGHT, fill = Y)
        scroll_x.config(command = self.ProductTable.xview)
        scroll_y.config(command = self.ProductTable.yview)

        self.ProductTable.heading("pid", text = "Product ID")
        self.ProductTable.heading("name", text = "Name")
        self.ProductTable.heading("price", text = "Price")
        self.ProductTable.heading("qty", text = "Quantity")
        self.ProductTable.heading("status", text = "Status")

        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width = 70)
        self.ProductTable.column("name", width = 100)
        self.ProductTable.column("price", width = 60)
        self.ProductTable.column("qty", width = 60)
        self.ProductTable.column("status", width = 70)
        self.ProductTable.pack(fill = BOTH, expand = 1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        label_note = Label(productFrame1, text = "Note: Enter 0 Quantity to remove product from the cart.", font = ("goudy old style", 12), anchor = 'w', bg = "white", fg = "red").pack(side = BOTTOM, fill = X)

        # Customer Frame
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        customer_frame = Frame(self.root, bd = 4, relief = RIDGE, bg = "white")
        customer_frame.place(x = 420, y = 110, width = 530, height = 70)

        c_title = Label(customer_frame, text = "Customer Details", font = ("goudy old style", 15), bg = "lightgray").pack(side = TOP, fill = X)
        label_name = Label(customer_frame, text = "Name", font = ("times new roman", 15), bg = "white").place(x = 5, y = 35)
        text_name = Entry(customer_frame, textvariable = self.var_cname, font = ("times new roman", 13), bg = "lightyellow").place(x = 80, y = 35, width = 180)

        label_contact = Label(customer_frame, text = "Contact No.", font = ("times new roman", 15), bg = "white").place(x = 270, y = 35)
        text_contact = Entry(customer_frame, textvariable = self.var_contact, font = ("times new roman", 13), bg = "lightyellow").place(x = 380, y = 35, width = 140)

        # Calculator-Cart Frame
        cal_cart_frame = Frame(self.root, bd = 2, relief = RIDGE, bg = "white")
        cal_cart_frame.place(x = 420, y = 190, width = 530, height = 360)

        # Calculator Frame
        self.var_cal_input = StringVar()

        cal_frame = Frame(cal_cart_frame, bd = 9, relief = RIDGE, bg = "white")
        cal_frame.place(x = 5, y = 10, width = 268, height = 340)

        txt_cal_input = Entry(cal_frame, textvariable = self.var_cal_input, font = ("arial", 15, "bold"), width = 21, bd = 10, relief = GROOVE, state = "readonly", justify = RIGHT)
        txt_cal_input.grid(row = 0, columnspan = 4)

        btn_7 = Button(cal_frame, text = '7', font = ("arial", 15, "bold"), command = lambda:self.get_input(7), bd = 5, width = 4, pady = 10, cursor = "hand2").grid(row = 1, column = 0)
        btn_8 = Button(cal_frame, text = '8', font = ("arial", 15, "bold"), command = lambda:self.get_input(8), bd = 5, width = 4, pady = 10, cursor = "hand2").grid(row = 1, column = 1)
        btn_9 = Button(cal_frame, text = '9', font = ("arial", 15, "bold"), command = lambda:self.get_input(9), bd = 5, width = 4, pady = 10, cursor = "hand2").grid(row = 1, column = 2)
        btn_sum = Button(cal_frame, text = '+', font = ("arial", 15, "bold"), command = lambda:self.get_input('+'), bd = 5, width = 4, pady = 10, cursor = "hand2").grid(row = 1, column = 3)

        btn_4 = Button(cal_frame, text = '4', font = ("arial", 15, "bold"), command = lambda:self.get_input(4), bd = 5, width = 4, pady = 10, cursor = "hand2").grid(row = 2, column = 0)
        btn_5 = Button(cal_frame, text = '5', font = ("arial", 15, "bold"), command = lambda:self.get_input(5), bd = 5, width = 4, pady = 10, cursor = "hand2").grid(row = 2, column = 1)
        btn_6 = Button(cal_frame, text = '6', font = ("arial", 15, "bold"), command = lambda:self.get_input(6), bd = 5, width = 4, pady = 10, cursor = "hand2").grid(row = 2, column = 2)
        btn_sub = Button(cal_frame, text = '-', font = ("arial", 15, "bold"), command = lambda:self.get_input('-'), bd = 5, width = 4, pady = 10, cursor = "hand2").grid(row = 2, column = 3)

        btn_1 = Button(cal_frame, text = '1', font = ("arial", 15, "bold"), command = lambda:self.get_input(1), bd = 5, width = 4, pady = 10, cursor = "hand2").grid(row = 3, column = 0)
        btn_2 = Button(cal_frame, text = '2', font = ("arial", 15, "bold"), command = lambda:self.get_input(2), bd = 5, width = 4, pady = 10, cursor = "hand2").grid(row = 3, column = 1)
        btn_3 = Button(cal_frame, text = '3', font = ("arial", 15, "bold"), command = lambda:self.get_input(3), bd = 5, width = 4, pady = 10, cursor = "hand2").grid(row = 3, column = 2)
        btn_mul = Button(cal_frame, text = '*', font = ("arial", 15, "bold"), command = lambda:self.get_input('*'), bd = 5, width = 4, pady = 10, cursor = "hand2").grid(row = 3, column = 3)

        btn_0 = Button(cal_frame, text = '0', font = ("arial", 15, "bold"), command = lambda:self.get_input(0), bd = 5, width = 4, pady = 15, cursor = "hand2").grid(row = 4, column = 0)
        btn_c = Button(cal_frame, text = 'c', font = ("arial", 15, "bold"), command = self.clear_cal, bd = 5, width = 4, pady = 15, cursor = "hand2").grid(row = 4, column = 1)
        btn_eq = Button(cal_frame, text = '=', font = ("arial", 15, "bold"), command = self.perform_cal, bd = 5, width = 4, pady = 15, cursor = "hand2").grid(row = 4, column = 2)
        btn_div = Button(cal_frame, text = '/', font = ("arial", 15, "bold"), command = lambda:self.get_input('/'), bd = 5, width = 4, pady = 15, cursor = "hand2").grid(row = 4, column = 3)

        # Cart Frame
        cart_frame = Frame(cal_cart_frame, bd = 3, relief = RIDGE)
        cart_frame.place(x = 280, y = 8, width = 245, height = 342)
        self.cart_title = Label(cart_frame, text = "Cart      Total Product: [0]", font = ("goudy old style", 15), bg = "lightgray")
        self.cart_title.pack(side = TOP, fill = X)

        scroll_y = Scrollbar(cart_frame, orient = VERTICAL)
        scroll_x = Scrollbar(cart_frame, orient = HORIZONTAL)

        self.cart_table = ttk.Treeview(cart_frame, columns = ("pid", "name", "price", "qty"), yscrollcommand = scroll_y.set, xscrollcommand = scroll_x.set)
        scroll_x.pack(side = BOTTOM, fill = X)
        scroll_y.pack(side = RIGHT, fill = Y)
        scroll_x.config(command = self.cart_table.xview)
        scroll_y.config(command = self.cart_table.yview)

        self.cart_table.heading("pid", text = "Product ID")
        self.cart_table.heading("name", text = "Name")
        self.cart_table.heading("price", text = "Price")
        self.cart_table.heading("qty", text = "Quantity")

        self.cart_table["show"] = "headings"

        self.cart_table.column("pid", width = 70)
        self.cart_table.column("name", width = 100)
        self.cart_table.column("price", width = 60)
        self.cart_table.column("qty", width = 60)
        self.cart_table.pack(fill = BOTH, expand = 1)
        self.cart_table.bind("<ButtonRelease-1>", self.get_data_cart)

        # Add Cart Widget Frame
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        add_cart_widget_frame = Frame(self.root, bd = 2, relief = RIDGE, bg = "white")
        add_cart_widget_frame.place(x = 420, y = 550, width = 530, height = 110)

        lbl_p_name = Label(add_cart_widget_frame, text = "Product Name", font = ("times new roman", 15), bg = "white").place(x = 5, y = 5)
        txt_p_name = Entry(add_cart_widget_frame, textvariable = self.var_pname, font = ("times new roman", 15), bg = "lightyellow", state = 'readonly').place(x = 5, y = 35, width = 190, height = 22)

        lbl_p_price = Label(add_cart_widget_frame, text = "Price per quantity", font = ("times new roman", 15), bg = "white").place(x = 230, y = 5)
        txt_p_price = Entry(add_cart_widget_frame, textvariable = self.var_price, font = ("times new roman", 15), bg = "lightyellow", state = 'readonly').place(x = 230, y = 35, width = 150, height = 22)

        lbl_p_qty = Label(add_cart_widget_frame, text = "Quantity", font = ("times new roman", 15), bg = "white").place(x = 390, y = 5)
        txt_p_qty = Entry(add_cart_widget_frame, textvariable = self.var_qty, font = ("times new roman", 15), bg = "lightyellow").place(x = 390, y = 35, width = 120, height = 22)

        self.lbl_instock = Label(add_cart_widget_frame, text = "In stock", font = ("times new roman", 15), bg = "white")
        self.lbl_instock.place(x = 5, y = 70)

        btn_clear_cart = Button(add_cart_widget_frame, text = "Clear", command = self.clear_cart, font = ("times new roman", 15, "bold"), bg = "lightgray", cursor = "hand2").place(x = 180, y = 70, width = 150, height = 30)
        btn_add_cart = Button(add_cart_widget_frame, text = "Add / Update Cart", command = self.add_update_cart, font = ("times new roman", 15, "bold"), bg = "orange", cursor = "hand2").place(x = 340, y = 70, width = 180, height = 30)

        # Billing Area
        bill_frame = Frame(self.root, bd = 2, relief = RIDGE, bg = "white")
        bill_frame.place(x = 953, y = 110, width = 410, height = 410)

        b_title = Label(bill_frame, text = "Customer Bill Area", font = ("goudy old style", 20, "bold"), bg = "#F44336", fg = "white").pack(side = TOP, fill = X)
        scrolly = Scrollbar(bill_frame, orient = VERTICAL)
        scrolly.pack(side = RIGHT, fill = Y)
        
        self.txt_bill_area = Text(bill_frame, yscrollcommand = scrolly.set)
        self.txt_bill_area.pack(fill = BOTH, expand = 1)
        scrolly.config(command = self.txt_bill_area.yview)

        # Billing Buttons
        bill_menu_frame = Frame(self.root, bd = 2, relief = RIDGE, bg = "white")
        bill_menu_frame.place(x = 953, y = 520, width = 410, height = 140)

        self.lbl_amount = Label(bill_menu_frame, text = "Bill Amount\n[0]", font = ("goudy old style", 15, "bold"), bg = "#3F51B5", fg = "white")
        self.lbl_amount.place(x = 2, y = 5, width = 120, height = 70)

        self.lbl_discount = Label(bill_menu_frame, text = "Discount\n[5%]", font = ("goudy old style", 15, "bold"), bg = "#8BC34A", fg = "white")
        self.lbl_discount.place(x = 124, y = 5, width = 120, height = 70)

        self.lbl_netpay = Label(bill_menu_frame, text = "Net Pay\n[0]", font = ("goudy old style", 15, "bold"), bg = "#607D8B", fg = "white")
        self.lbl_netpay.place(x = 246, y = 5, width = 160, height = 70)

        btn_print = Button(bill_menu_frame, text = "Print", command = self.print_bill, cursor = "hand2", font = ("goudy old style", 15, "bold"), bg = "lightgreen", fg = "white")
        btn_print.place(x = 2, y = 80, width = 90, height = 50)

        btn_clear_all = Button(bill_menu_frame, text = "Clear All", command = self.clear_all, cursor = "hand2", font = ("goudy old style", 15, "bold"), bg = "gray", fg = "white")
        btn_clear_all.place(x = 94, y = 80, width = 90, height = 50)

        btn_generate = Button(bill_menu_frame, text = "Generate / Save Bill", command = self.generate_bill, cursor = "hand2", font = ("goudy old style", 15, "bold"), bg = "#009688", fg = "white")
        btn_generate.place(x = 186, y = 80, width = 205, height = 50)

        # Footer
        footer = Label(self.root, text = "AITventory | Developed by Allen Sabu\nFor any Technical Issue, contact: 8929718053", font = ("times new roman", 11), bg = "#4D636D", fg = "white").pack(side = BOTTOM, fill = X)

        self.show()
        self.update_date_time()

    # All Functions
    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT pid, name, price, qty, status FROM product WHERE status = 'Active'")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values = row) 
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def search(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input is required.", parent = self.root)
            else:
                cur.execute("SELECT pid, name, price, qty, status FROM product WHERE name LIKE '%"+ self.var_search.get() + "%' AND status = 'Active'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values = row) 
                else:
                    messagebox.showerror("Error", "No record found.", parent = self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text = f"In stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set("1")

    def get_data_cart(self, ev):
        f = self.cart_table.focus()
        content = (self.cart_table.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text = f"In stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def add_update_cart(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Please select product from the list.", parent = self.root)
        elif self.var_qty.get() == "":
            messagebox.showerror("Error", "Quantity is empty.", parent = self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror("Error", "Invalid quantity.", parent = self.root)
        else:
            # price_cal = float(int(self.var_qty.get()) * float(self.var_price.get()))
            price_cal = self.var_price.get()
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]
            # Update cart
            present = "no"
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = "yes"
                    break
                index_ += 1
            if present == "yes":
                op = messagebox.askyesno("Confirm", "Product is already present. \nDo you want to update or remove from the cart list?", parent = self.root)
                if op == True:
                    if self.var_qty.get() == '0':
                        self.cart_list.pop(index_)
                    else:
                        # self.cart_list[index_][2] = price_cal
                        self.cart_list[index_][3] = self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.bill_amnt = self.bill_amnt + (float(row[2]) * int(row[3]))
        self.discount = (self.bill_amnt * 5) / 100
        net_pay = self.bill_amnt - self.discount
        self.lbl_amount.config(text = f"Bill Amount\n{str(self.bill_amnt)}")
        self.lbl_netpay.config(text = f"Net Pay\n{str(net_pay)}")
        self.cart_title.config(text = f"Cart     Total Product: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.cart_table.delete(*self.cart_table.get_children())
            for row in self.cart_list:
                self.cart_table.insert("", END, values = row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

    def generate_bill(self):
        if self.var_cname.get() == "" or self.var_contact.get() == "":
            messagebox.showerror("Error", f"Customer details required.", parent = self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", f"Please add product to the cart.", parent = self.root)
        else:
            # Bill Top
            self.bill_top()
            # Bill Middle
            self.bill_middle()
            # Bill Bottom
            self.bill_bottom()

            fp = open(f"bill/{str(self.invoice)}.txt", 'w')
            fp.write(self.txt_bill_area.get("1.0", END))
            fp.close()
            messagebox.showinfo("Saved", "Bill has been generated and is saved.", parent = self.root)
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
\t\tAIT-Inventory
\t Phone No. 8929718053, Pune-411015
{str("=" * 47)}
 Customer Name: {self.var_cname.get()}
 Phone No.: {self.var_contact.get()}
 Bill No.: {str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("=" * 47)}
 Product Name\t\t\tQuantity\tPrice
{str("=" * 47)}
        '''
        self.txt_bill_area.delete("1.0", END)
        self.txt_bill_area.insert("1.0", bill_top_temp)

    def bill_middle(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                qty = int(row[4]) - int(row[3])
                if int(row[3]) == int(row[4]):
                    status = "Inactive"
                if int(row[3]) != int(row[4]):
                    status = "Active"

                price = float(row[2]) * int(row[3])
                price = str(price)
                self.txt_bill_area.insert(END, "\n " + name + "\t\t\t" + row[3] + "\tRs." + price)
                # Update quantity in Product Table
                cur.execute("UPDATE product SET qty = ?, status = ? WHERE pid = ?", (
                    qty, status, pid 
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent = self.root)

    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("=" * 47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("=" * 47)}\n
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_instock.config(text = f"In stock")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set("")
        self.var_contact.set("")
        self.txt_bill_area.delete("1.0", END)
        self.cart_title.config(text = f"Cart     Total Product: [0]")
        self.var_search.set("")
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print = 0

    def update_date_time(self):
        time_ = time.strftime("%H:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.label_clock.config(text = f"Welcome to AITventory\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.label_clock.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo('Print', "Please wait while printing.", parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get("1.0", END))
            try:
                subprocess.run(['notepad.exe', '/p', new_file], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror('Print', f"Failed to print: {e}", parent=self.root)
        else:
            messagebox.showerror('Print', "Please generate bill to print the receipt.", parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__ == "__main__":
    root = Tk()
    obj = billClass(root)
    root.mainloop()