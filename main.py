from tkinter import *
import random
import json
from tkinter import messagebox
import pyperclip
window = Tk()
window.title('Password Manager')
window.config(padx=50,pady=50)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def pass_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    [password_list.append(random.choice(letters)) for char in range(nr_letters)] 

    [password_list.append(random.choice(symbols)) for char in range(nr_symbols)] 

    [password_list.append(random.choice(numbers)) for char in range(nr_numbers)] 

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char
    pyperclip.copy(password)
    password_entry.insert(END, string=password)
    
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = web_entry.get().strip()
    saved_website = website.title()
    email = email_entry.get()
    password = password_entry.get().strip()
    new_data = {
        saved_website:{
            "email" : email,
            "password" : password
        }
    }
    
    if website == "" or password == "":
        
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else: 
        #is_okay = messagebox.askokcancel(title="website", message=f"These are the details entered: \nEmail: {email} \nWebsite; {website} \nPassword: {password} \nIs it ok to save?")
        try:
            with open("data.json", "r") as data_file:   
                #reading old data
                data = json.load(data_file)
        except:
            #writing to file   
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            #updating old data
            data.update(new_data)
            with open("data.json", "w") as data_file: 
               
                json.dump(data, data_file, indent=4)
        finally:
            web_entry.delete(0,'end')
            password_entry.delete(0,'end')
# ---------------------------- SEARCH ------------------------------- #
def get_pass():
    try:
        with open("data.json", "r") as data_file:   
            #reading old data
            search_term = web_entry.get().strip()
            formatted_search_term = search_term.title()
            data = json.load(data_file)
            result = data[formatted_search_term]
    except FileNotFoundError:
        messagebox.showinfo(title="oops!", message="No file found!")
    except KeyError:
        messagebox.showinfo(title=formatted_search_term, message=f"No website found for {formatted_search_term}")
    else:
        email = result['email']
        password = result['password']
        messagebox.showinfo(title=formatted_search_term, message=f"Webiste: {formatted_search_term} \n Email: {email}\n Password: {password}")
    finally:
        web_entry.delete(0,'end')
# ---------------------------- UI SETUP ------------------------------- #
canvas = Canvas(width=200,height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
#timer_text = canvas.create_text(100, 130, text="00:00", font=(FONT_NAME, 32, "bold"))
canvas.grid(column=1, row=0)

web_label = Label(text="Website:",fg="white")
web_label.grid(column=0, row=2)

email_label = Label(text="Email/Username:",fg="white")
email_label.grid(column=0, row=3)

password_label = Label(text="Password:",fg="white")
password_label.grid(column=0, row=4)

web_entry = Entry(width=35,highlightthickness=1,highlightcolor="blue", highlightbackground="#CCCCCC")
web_entry.grid(column=1, row=2,columnspan=2, pady=5)
web_entry.focus()

email_entry = Entry(width=35,bg="white",fg="black",highlightthickness=0)
email_entry.grid(column=1, row=3,columnspan=2, pady=5)
email_entry.insert(END, string="okaz692@gmail.com")

password_entry = Entry(width=35, bg="white",fg="black", highlightthickness=0)
password_entry.grid(column=1, row=4,columnspan=2,pady=5)

calc_button = Button(width=10, text="Generate Password",highlightthickness=0,bd=0, command=pass_gen)
calc_button.grid(column=2, row=4,pady=5,padx=5)

add_button = Button(text="Add",width=33,highlightthickness=0, fg="black", command=save)
add_button.grid(column=1, row=5,columnspan=2, pady=5)

search_button = Button(text="search",width=10,highlightthickness=0, fg="black", command=get_pass)
search_button.grid(column=2, row=2,columnspan=2, pady=5, padx=5)

window.mainloop()


