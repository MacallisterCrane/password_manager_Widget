from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_l = [choice(letters) for l in range(randint(8, 10))]
    password_s = [choice(symbols) for s in range(randint(2, 4))]
    password_n = [choice(numbers) for i in range(randint(2, 4))]

    password_list = password_l + password_s + password_n
    shuffle(password_list)
    password = "".join(password_list)

    password_box.insert(0, password)
    pyperclip.copy(password)

def save_info():
    web = website_box.get()
    user = email_user_box.get()
    passw = password_box.get()
    new_data = {
        web: {
            "email": user,
            "password": passw
        }
    }

    if len(passw) == 0 or len(web) == 0:
        messagebox.showinfo("Error", "Password and Website must both be filled in")
    if len(passw) and len(web) > 0:
        ok = messagebox.askokcancel(title="Adding Information", message=f"Would you like to commit {web} | {user} | {passw} to password manager")
        if ok:
            try:
                with open("pass_manager.json", "r") as file:
                    data = json.load(file)
            except:
                with open("pass_manager.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)

                with open("pass_manager.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                website_box.delete(0, END)
                password_box.delete(0, END)

def search():
    match = website_box.get()
    try:
        with open("pass_manager.json") as file:
            data = json.load(file)
    except:
        messagebox.showinfo("Error", "Password Manager file doesnt exist.")
    else:
        if match in data:
            return messagebox.showinfo(title=match, message=f"Email: {match}\n Password: {password}")
        else:
            return messagebox.showinfo(title="No match found", message=f"There are no current entries for the website name: {match}")

window = Tk()
window.title('Password Manager')
window.config(padx=25, pady=25)

canvas = Canvas(window, width=200, height=200)
logo = PhotoImage(file='logo.png')
canvas.create_image(100, 100,image=logo)
canvas.grid(column=1, row=0)

website = Label(window, text='Website:')
website.grid(column=0, row=1)
email_user = Label(window, text='Email/Username:')
email_user.grid(column=0, row=2)
password = Label(window, text='Password:')
password.grid(column=0, row=3)

website_box = Entry(width=35)
website_box.grid(column=1, row=1, columnspan=2)
website_box.focus()
email_user_box = Entry(width=35)
email_user_box.insert(0, "macallisterlcrane@gmail.com")
email_user_box.grid(column=1, row=2, columnspan=2)
password_box = Entry(width=21)
password_box.grid(column=1, row=3)

add_button = Button(window, text='Add', command=save_info)
add_button.config(width=36)
add_button.grid(column=1, row=4, columnspan=2)

pass_gen = Button(window, text='Generate Password', command=generate_pass)
pass_gen.grid(column=2, row=3)

search = Button(window, text='Search', command=search)
search.grid(column=2, row=2)
window.mainloop()
