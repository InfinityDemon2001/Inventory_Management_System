from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("AITventory | Inventory Management System Developed by Allen")
        self.root.config(bg = "white")
        self.root.focus_force()

        # Variables
        self.var_searchby = StringVar()
        self.var_searchtext = StringVar()
        
        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        # Search Frame
        searchFrame = LabelFrame(self.root, text = "Search Employee", font = ("goudy old style", 12, "bold"), bd = 2, relief = RIDGE, bg = "white")
        searchFrame.place(x = 250, y = 20, width = 600, height = 70)

        # Options
        cmb_search = ttk.Combobox(searchFrame, textvariable = self.var_searchby, values = ("Select", "Email", "Name", "Contact"), state = 'readonly', justify = CENTER, font = ("goudy old style", 15))
        cmb_search.place(x = 10, y = 10, width = 180)
        cmb_search.current(0)

        text_search = Entry(searchFrame, textvariable = self.var_searchtext, font = ("goudy old style", 15), bg = "lightyellow").place(x = 200, y = 10)
        button_search = Button(searchFrame, text = "Search", command = self.search, font = ("goudy old style", 15), bg = "#4CAF50", fg = "white", cursor = "hand2").place(x = 410, y = 9, width = 150, height = 30)

        # Title
        title = Label(self.root, text = "Employee Details", font = ("goudy old style", 15), bg = "#0F4D7D", fg = "white").place(x = 50, y = 100, width = 1000)

        # Content
        # Row 1
        label_empid = Label(self.root, text = "Emp ID", font = ("goudy old style", 15),bg = "white").place(x = 50, y = 150)
        label_gender = Label(self.root, text = "Gender", font = ("goudy old style", 15),bg = "white").place(x = 350, y = 150)
        label_contact = Label(self.root, text = "Contact", font = ("goudy old style", 15),bg = "white").place(x = 750, y = 150)
        
        text_empid = Entry(self.root, textvariable = self.var_emp_id, font = ("goudy old style", 15),bg = "lightyellow").place(x = 150, y = 150, width = 180)
        cmb_gender = ttk.Combobox(self.root, textvariable = self.var_gender, values = ("Select", "Male", "Female", "Others"), state = 'readonly', justify = CENTER, font = ("goudy old style", 15))
        cmb_gender.place(x = 500, y = 150, width = 180)
        cmb_gender.current(0)
        text_contact = Entry(self.root, textvariable = self.var_contact, font = ("goudy old style", 15),bg = "lightyellow").place(x = 850, y = 150, width = 180)

        # Row 2
        label_name = Label(self.root, text = "Name", font = ("goudy old style", 15),bg = "white").place(x = 50, y = 190)
        label_dob = Label(self.root, text = "D.O.B.", font = ("goudy old style", 15),bg = "white").place(x = 350, y = 190)
        label_doj = Label(self.root, text = "D.O.J.", font = ("goudy old style", 15),bg = "white").place(x = 750, y = 190)
        
        text_name = Entry(self.root, textvariable = self.var_name, font = ("goudy old style", 15),bg = "lightyellow").place(x = 150, y = 190, width = 180)
        text_dob = Entry(self.root, textvariable = self.var_dob, font = ("goudy old style", 15),bg = "lightyellow").place(x = 500, y = 190, width = 180)
        text_doj = Entry(self.root, textvariable = self.var_doj, font = ("goudy old style", 15),bg = "lightyellow").place(x = 850, y = 190, width = 180)

        # Row 3
        label_email = Label(self.root, text = "Email", font = ("goudy old style", 15),bg = "white").place(x = 50, y = 230)
        label_pass = Label(self.root, text = "Password", font = ("goudy old style", 15),bg = "white").place(x = 350, y = 230)
        label_utype = Label(self.root, text = "User Type", font = ("goudy old style", 15),bg = "white").place(x = 750, y = 230)
        
        text_email = Entry(self.root, textvariable = self.var_email, font = ("goudy old style", 15),bg = "lightyellow").place(x = 150, y = 230, width = 180)
        text_pass = Entry(self.root, textvariable = self.var_pass, font = ("goudy old style", 15),bg = "lightyellow").place(x = 500, y = 230, width = 180)
        cmb_utype = ttk.Combobox(self.root, textvariable = self.var_utype, values = ("Admin", "Employee"), state = 'readonly', justify = CENTER, font = ("goudy old style", 15))
        cmb_utype.place(x = 850, y = 230, width = 180)
        cmb_utype.current(0)

        # Row 4
        label_address = Label(self.root, text = "Address", font = ("goudy old style", 15),bg = "white").place(x = 50, y = 270)
        label_salary = Label(self.root, text = "Salary", font = ("goudy old style", 15),bg = "white").place(x = 500, y = 270)
        
        self.text_address = Text(self.root, font = ("goudy old style", 15),bg = "lightyellow")
        self.text_address.place(x = 150, y = 270, width = 300, height = 60)
        text_salary = Entry(self.root, textvariable = self.var_salary, font = ("goudy old style", 15),bg = "lightyellow").place(x = 600, y = 270, width = 180)

        # Buttons
        button_add = Button(self.root, text = "Save", command = self.add, font = ("goudy old style", 15), bg = "#2196F3", fg = "white", cursor = "hand2").place(x = 500, y = 305, width = 110, height = 28)
        button_update = Button(self.root, text = "Update", command = self.update, font = ("goudy old style", 15), bg = "#4CAF50", fg = "white", cursor = "hand2").place(x = 620, y = 305, width = 110, height = 28)
        button_delete = Button(self.root, text = "Delete", command = self.delete, font = ("goudy old style", 15), bg = "#F44336", fg = "white", cursor = "hand2").place(x = 740, y = 305, width = 110, height = 28)
        button_clear = Button(self.root, text = "Clear", command = self.clear, font = ("goudy old style", 15), bg = "#607D8B", fg = "white", cursor = "hand2").place(x = 860, y = 305, width = 110, height = 28)

        # Employee Details
        emp_frame = Frame(self.root, bd = 3, relief = RIDGE)
        emp_frame.place(x = 0, y = 350, relwidth = 1, height = 150)

        scroll_y = Scrollbar(emp_frame, orient = VERTICAL)
        scroll_x = Scrollbar(emp_frame, orient = HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns = ("eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"), yscrollcommand = scroll_y.set, xscrollcommand = scroll_x.set)
        scroll_x.pack(side = BOTTOM, fill = X)
        scroll_y.pack(side = RIGHT, fill = Y)
        scroll_x.config(command = self.EmployeeTable.xview)
        scroll_y.config(command = self.EmployeeTable.yview)
        self.EmployeeTable.heading("eid", text = "Emp ID")
        self.EmployeeTable.heading("name", text = "Name")
        self.EmployeeTable.heading("email", text = "Email")
        self.EmployeeTable.heading("gender", text = "Gender")
        self.EmployeeTable.heading("contact", text = "Contact")
        self.EmployeeTable.heading("dob", text = "D.O.B.")
        self.EmployeeTable.heading("doj", text = "D.O.J.")
        self.EmployeeTable.heading("pass", text = "Password")
        self.EmployeeTable.heading("utype", text = "User Type")
        self.EmployeeTable.heading("address", text = "Address")
        self.EmployeeTable.heading("salary", text = "Salary")
        self.EmployeeTable["show"] = "headings"
        self.EmployeeTable.column("eid", width = 100)
        self.EmployeeTable.column("name", width = 100)
        self.EmployeeTable.column("email", width = 100)
        self.EmployeeTable.column("gender", width = 100)
        self.EmployeeTable.column("contact", width = 100)
        self.EmployeeTable.column("dob", width = 100)
        self.EmployeeTable.column("doj", width = 100)
        self.EmployeeTable.column("pass", width = 100)
        self.EmployeeTable.column("utype", width = 100)
        self.EmployeeTable.column("address", width = 100)
        self.EmployeeTable.column("salary", width = 100)
        self.EmployeeTable.pack(fill = BOTH, expand = 1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def add(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required.", parent = self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid = ?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent = self.root)
                else:
                    cur.execute("Insert into employee (eid , name, email, gender, contact, dob, doj, pass, utype, address, salary) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.text_address.get('1.0', END),
                        self.var_salary.get()
                    ))
                    con.commit()
                    messagebox.showerror("Success", "Employee added succesfully", parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def show(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values = row) 
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = (self.EmployeeTable.item(f))
        row = content['values']
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.text_address.delete('1.0', END)
        self.text_address.insert(END, row[9])
        self.var_salary.set(row[10])

    def update(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required.", parent = self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid = ?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Employee ID.", parent = self.root)
                else:
                    cur.execute("UPDATE employee SET name = ?, email = ?, gender = ?, contact = ?, dob = ?, doj = ?, pass = ?, utype = ?, address = ?, salary = ? WHERE eid = ?", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.text_address.get('1.0', END),
                        self.var_salary.get(),
                        self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showerror("Success", "Employee updated succesfully", parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def delete(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required.", parent = self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid = ?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Employee ID.", parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent = self.root)
                    if op == True:
                        cur.execute("DELETE FROM employee WHERE eid = ?", (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Employee deleted successfully", parent = self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.text_address.delete('1.0', END)
        self.var_salary.set("")
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
                cur.execute("SELECT * FROM employee WHERE " + self.var_searchby.get() + " LIKE '%"+self.var_searchtext.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values = row) 
                else:
                    messagebox.showerror("Error", "No record found.", parent = self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)
 
if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()