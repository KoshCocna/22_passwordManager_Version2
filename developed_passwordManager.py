from tkinter import *
from random import choice, randint, shuffle
from tkinter import messagebox

# -----------------Password Generator---------------#
letters = list(map(chr, range(65, 123)))
numbers = list(map(chr, range(48, 58)))
symbols = list(map(chr, range(33, 48)))


def generate():
    password = [choice(letters) for _ in range(randint(8, 10))]
    password += [choice(numbers) for _ in range(randint(2, 4))]
    password += [choice(symbols) for _ in range(randint(2, 4))]
    shuffle(password)
    password = "".join(password)
    password_entry.delete(0, END)
    password_entry.insert(0, password)


# -------------------------Save----------------------------#
def save():
    website = website_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="warning", message="Pls fill out the every field!")
    else:
        res = is_website_in_data(website)
        if res[0]:
            want_update = messagebox.askokcancel(title="update?",
                                                 message=f"There is already password of {website}, are you sure to update?")
            if want_update:
                update(res[1], password)

        else:
            is_ok = messagebox.askokcancel(title="save",
                                           message=f"Is it ok to save as followings? {website} | {email} | {password}")
            if is_ok:
                with open("password_file.txt", "a") as data:
                    data.write(f" {website} | {email} | {password} \n")
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)
            else:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ------------------------Update----------------------------#

def update(old_password, new_password):
    with open("password_file.txt", 'r') as data:
        f = data.read()
    f = f.replace(old_password, new_password)
    with open('password_file.txt', 'w') as file:
        file.write(f)
    website_entry.delete(0, END)
    password_entry.delete(0, END)


# ------------------------Search---------------------------#
def search():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showwarning(title="warning", message="Pls enter the website name to search!")
    else:
        result = is_website_in_data(website)
        if result[0]:
            password_entry.delete(0, END)
            password_entry.insert(0, result[1])
        else:
            messagebox.showwarning(title="warning", message="Pls enter the correct website name to search!")


# ---------------------is_website_in_data---------------------#

def is_website_in_data(website):
    is_match = False
    password = ''
    with open("password_file.txt", "r") as data:
        for line in data:
            line = line[:-1]
            line_list = line.split('|')
            data_website = line_list[0]
            data_website = data_website[1:-1]
            data_password = line_list[-1]
            data_password = data_password[1:-1]
            if website == data_website:
                is_match = True
                password = data_password
    return is_match, password


# -------------------UI design--------------------#
window = Tk()
window.title("Password Manager V2")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website")
website_label.grid(row=1, column=0)
email_label = Label(text="Email")
email_label.grid(row=2, column=0)
password_label = Label(text="Password")
password_label.grid(row=3, column=0)

website_entry = Entry(width=25)
website_entry.grid(row=1, column=1)
search_btn = Button(text="Search", width=10, command=search)
search_btn.grid(row=1, column=2)
email_entry = Entry(width=25)
email_entry.insert(0, "kim@gmail.com")
email_entry.grid(row=2, column=1)
password_entry = Entry(width=25)
password_entry.grid(row=3, column=1)
generate_btn = Button(text="Generate", width=10, command=generate)
generate_btn.grid(row=3, column=2)
add_btn = Button(text="Add", width=10, command=save)
add_btn.grid(row=4, column=1)

window.mainloop()
