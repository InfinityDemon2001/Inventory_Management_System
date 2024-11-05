from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import sqlite3
import os
import email_pass
import smtplib
import time

class login_system:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System | Developed by Allen Sabu")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg = "#fafafa")

        self.otp = ""

        # Images
        self.phone_image = ImageTk.PhotoImage(file = "images/phone.png")
        self.lbl_phone_image = Label(self.root, image = self.phone_image, bd = 0).place(x = 200, y = 50)

        # Login Frame
        self.employee_id = StringVar()
        self.password = StringVar()

        login_frame = Frame(self.root, bd = 2, relief = RIDGE, bg = "white")
        login_frame.place(x = 650, y = 90, width = 350, height = 460)

        title = Label(login_frame, text = "Login System", font = ("Elephant", 30, "bold"), bg = "white").place(x = 0, y = 30, relwidth = 1)

        lbl_user = Label(login_frame, text = "Employee ID", font = ("Andalus", 15), bg = "white", fg = "#767171").place(x = 50, y = 100)
        txt_employee_id = Entry(login_frame, textvariable = self.employee_id, font = ("Times New Roman", 15), bg = "#ECECEC").place(x = 50, y = 140, width = 250)

        lbl_pass = Label(login_frame, text = "Password", font = ("Andalus", 15), bg = "white", fg = "#767171").place(x = 50, y = 200)
        txt_pass = Entry(login_frame, textvariable = self.password, show = "*", font = ("Times New Roman", 15), bg = "#ECECEC").place(x = 50, y = 240, width = 250)

        btn_login = Button(login_frame, text = "Login", command = self.login, font = ("Arial Rounded MT Bold", 15), bg = "#00B0F0", activebackground = "#00B0F0", fg = "white", activeforeground = "white", cursor = "hand2").place(x = 50, y = 300, width = 250, height = 35)

        hr = Label(login_frame, bg = "lightgray").place(x = 50, y = 370, width = 250, height = 2)
        or_ = Label(login_frame,text = "OR", bg = "white", fg = "lightgray", font = ("Times New Roman", 15)).place(x = 150, y = 355)

        btn_forgot = Button(login_frame, text = "Forgot Password?", command = self.forgot_win, font = ("Times New Roman", 13), bg = "white", fg = "#00759E", bd = 0, activebackground = "white", activeforeground = "#00759E").place(x = 100, y = 390)

        # Animation Images
        self.im1 = ImageTk.PhotoImage(file = "images/im1.png")
        self.im2 = ImageTk.PhotoImage(file = "images/im3.png")
        self.im3 = ImageTk.PhotoImage(file = "images/im2.png")

        self.lbl_change_image = Label(self.root, bg = "white")
        self.lbl_change_image.place(x = 367, y = 153, width = 240, height = 428)

        self.animate()

    # Funcions
    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image = self.im)
        self.lbl_change_image.after(2000, self.animate)

    def login(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror("Error", "All the fields are required.", parent = self.root)
            else:
                cur.execute("SELECT utype FROM employee WHERE eid = ? AND pass = ?", (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror("Error", "Invalid Employee ID / Password.", parent = self.root)
                else:
                    if user[0] == "Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def forgot_win(self):
        con = sqlite3.connect(database = r'InvMngSys.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required.", parent = self.root)
            else:
                cur.execute("SELECT email FROM employee WHERE eid = ?", (self.employee_id.get(),))
                email = cur.fetchone()
                if email == None:
                    messagebox.showerror("Error", "Invalid email.", parent = self.root)
                else:
                    # Forgot Window
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()

                    chk = self.send_email(email[0])
                    if chk == 'f':
                        messagebox.showerror("Error", "Connection error, try again.", parent = self.root)
                    else:
                        self.forgot_win = Toplevel(self.root)
                        self.forgot_win.title("Reset Password.")
                        self.forgot_win.geometry("400x350+500+100")
                        self.forgot_win.focus_force()
    
                        title = Label(self.forgot_win, text = "Reset Password", font = ("Gpudy Old Style", 15, "bold"), bg = "#3F51B5", fg = "white").pack(side = TOP, fill = X)
                        lbl_reset = Label(self.forgot_win, text = "Enter OTP sent on registered email ID", font = ("Times New Roman", 15)).place(x = 20, y = 60)
                        txt_reset = Entry(self.forgot_win, textvariable = self.var_otp, font = ("Times New Roman", 15), bg = "lightyellow").place(x = 20, y = 100, width = 250, height = 30)
                        self.btn_reset = Button(self.forgot_win, text = "Submit", command = self.validate_otp, font = ("Times New Roman", 15), bg = "lightblue")
                        self.btn_reset.place(x = 280, y = 100, width = 100, height = 30)
    
                        lbl_new_pass = Label(self.forgot_win, text = "New Password", font = ("Times New Roman", 15)).place(x = 20, y = 160)
                        txt_new_pass = Entry(self.forgot_win, textvariable = self.var_new_pass, font = ("Times New Roman", 15), bg = "lightyellow").place(x = 20, y = 190, width = 250, height = 30)
    
                        lbl_conf_pass = Label(self.forgot_win, text = "Confirm Password", font = ("Times New Roman", 15)).place(x = 20, y = 225)
                        txt_conf_pass = Entry(self.forgot_win, textvariable = self.var_conf_pass, font = ("Times New Roman", 15), bg = "lightyellow").place(x = 20, y = 255, width = 250, height = 30)
    
                        self.btn_update = Button(self.forgot_win, text = "Update", command = self.update_password, state = DISABLED, font = ("Times New Roman", 15), bg = "lightblue")
                        self.btn_update.place(x = 150, y = 300, width = 100, height = 30)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def update_password(self):
        if self.var_new_pass.get() == "" or self.var_conf_pass.get() == "":
            messagebox.showerror("Error", "Password is required.", parent = self.forgot_win)
        elif self.var_new_pass.get() != self.var_conf_pass.get():
            messagebox.showerror("Error", "Password must match.", parent = self.forgot_win)
        else:
            con = sqlite3.connect(database = r'InvMngSys.db')
            cur = con.cursor()
            try:
                cur.execute("UPDATE employee SET pass = ? WHERE eid = ?", (self.var_new_pass.get(), self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success", "Password updated successfully.", parent = self.forgot_win)
                self.forgot_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def validate_otp(self):
        if int(self.otp) == int(self.var_otp.get()):
            self.btn_update.config(state = NORMAL)
            self.btn_reset.config(state = DISABLED)
        else:
            messagebox.showerror("Error", "Invalid OTP, try again!", parent = self.forgot_win)

    def send_email(self, to_):
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        email_ = email_pass.email_
        pass_ = email_pass.pass_

        s.login(email_, pass_)

        self.otp = int(time.strftime("%H%S%M")) + int(time.strftime("%S"))

        subj = "AITventory - Reset Password OTP"
        msg = f"Dear User, \n\nYour reset OTP is {str(self.otp)}.\n\nWith Regards,\n AITventory Team"
        msg = "Subject:{}\n\n{}".format(subj, msg)
        s.sendmail(email_, to_, msg)
        chk = s.ehlo()
        if chk[0] == 250:
            return 's'
        else:
            return 'f'

root = Tk()
obj = login_system(root)
root.mainloop()