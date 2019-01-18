from tkinter import *
import os

class GUI:
    Title = [
        "Welcome to The Vault!",
        "Created by Jovin...",
        "Murtaza...",
        "And Justin!",
        "You can store your passwords here.",
    ]
    
    def __init__(self, master):
        self.master = master
        master.title("The Vault")

        self.displayed_password = False #for stored passwords window

        self.label_index = 0
        self.label_text = StringVar()
        self.label_text.set(self.Title[self.label_index])
        self.label = Label(master, textvariable = self.label_text)
        self.label.bind("<Button-1>", self.cycle_label_text)
        self.label.grid(row=0)

        if os.stat("security.txt").st_size == 0: #checks if there is already a security question setup
            self.first_start()
        else:
            self.start()

    def first_start(self):
        security_questions = ["What is your favourite TV show?",
                         "What is the name of your pet?",
                         "What is your mother's maiden name?",
                         "What is your favourite teacher's name?",
                              "Who is your favourite superhero?"
                         ]
        Label(self.master, text="").grid(row=1) #creates an empty line
        Label(self.master, text="Select your security question").grid(row=2)
        
        questionNum = StringVar(root)
        questionNum.set(security_questions[0])
        question_menu = OptionMenu(root, questionNum, *security_questions)
        question_menu.grid(row=3)

        Label(self.master, text="").grid(row=4)
        Label(self.master, text="Enter the answer to the security question").grid(row=5)
        
        answer = Entry(self.master)
        answer.grid(row=6)

        done_button = Button(self.master, text="Done", command=lambda:[self.buttons(),self.store_security(questionNum.get(),answer.get()),self.master.withdraw()]).grid(row=7)

        Label(self.master, text="").grid(row=8)

    def store_security(self, question, answer):
        security_file = open("security.txt","w")
        security_file.write(question+"\n"+answer)
        security_file.close()
        
    def start(self):
        Label(self.master, text="Answer the security question below").grid(row=2)
        Label(self.master, text="").grid(row=3)
        
        security_file = open("security.txt","r")
        security_info = security_file.read().splitlines()
        security_file.close()
        
        Label(self.master, text=security_info[0]).grid(row=4)

        answer = Entry(self.master)
        answer.grid(row=5)

        Button(self.master, text="Start Program", command=lambda:self.correct_answer(answer.get(),security_info[1])).grid(row=6)

        Label(self.master, text="").grid(row=7)

    def correct_answer(self, user_answer, answer):
        if user_answer == answer:
            self.buttons()
            self.master.withdraw()
        else:
            wrong_answer = Label(self.master, text="Incorrect answer, try again")
            wrong_answer.grid(row=7)

    def buttons(self):
        window = Toplevel(root)

        Label(window, text="The Vault").pack()
        
        passwords = Button(window, text="Stored Info", command=self.stored_passwords_window).pack()

        add_password = Button(window, text="Add Password", command=self.add_password_window).pack()

        rchange_password = Button(window, text="Change Stored Info", command=self.change_password_window).pack()

        close_button = Button(window, text="Exit Program", command=self.end).pack()

        Label(window, text="").pack()

    def end(self):
        self.master.destroy()

    def change_password_window(self):
        window = Toplevel(root)

        if os.stat("websites.txt").st_size == 0:
            Label(window, text="You have no stored passwords").grid(row=0)
        else:
            Label(window, text="What website would you like to change the password for?").grid(row=0)

            file = open("websites.txt","r")
            website_list = file.read().splitlines()
            file.close()

            websites = StringVar(root)
            websites.set(website_list[0])
            websites_menu = OptionMenu(window, websites, *website_list)
            websites_menu.grid(row=1)

            next_button = Button(window, text="Next", command=lambda:[self.change_info(window, websites.get(), website_list),websites_menu.grid_forget(),next_button.grid_forget()])
            next_button.grid(row=2)

    def change_info(self, window, website_name, websites):
        Label(window, text="").grid(row=3)

        file = open("passwords.txt","r")
        passwords_list = file.read().splitlines()
        file.close()

        file = open("usernames.txt","r")
        username_list = file.read().splitlines()
        file.close()

        line = 0
        
        for i in websites:
            if website_name == i:
                Label(window, text="Previously stored username:").grid(row=4)
                Label(window, text=username_list[line]).grid(row=5)
                Label(window, text="").grid(row=6)
                Label(window, text="Previously stored password:").grid(row=7)
                Label(window, text=passwords_list[line]).grid(row=8)
                break
            else:
                line += 1

        Label(window, text="").grid(row=9)
        Label(window, text="Enter your new username").grid(row=10)

        new_username = Entry(window)
        new_username.grid(row=11)

        Label(window, text="").grid(row=12)
        Label(window, text="Enter your new password").grid(row=13)

        new_password = Entry(window)
        new_password.grid(row=14)

        Button(window, text="Done", command=lambda:[self.store_info(new_password.get(), new_username.get(), line),window.destroy()]).grid(row=15)

        Label(window, text="").grid(row=16)

    def store_info(self, password, username, line):
        file = open("passwords.txt","r")
        passwords = file.readlines()
        file.close()

        passwords[line] = password+"\n"

        file = open("passwords.txt","w")
        file.writelines(passwords)
        file.close()

        file = open("usernames.txt","r")
        usernames = file.readlines()
        file.close()

        usernames[line] = username+"\n"

        file = open("usernames.txt","w")
        file.writelines(usernames)
        file.close()

    def stored_passwords_window(self):
        window = Toplevel(root)

        if os.stat("websites.txt").st_size == 0:
            Label(window, text="You have no stored passwords").grid()
        else:            
            window_title = Label(window, text = "What website would you like to see your password for?")
            window_title.grid(row=0)

            file = open("websites.txt","r")
            website_list = file.read().splitlines()
            file.close()

            websites = StringVar(root)
            websites.set(website_list[0])
            websites_menu = OptionMenu(window, websites, *website_list)
            websites_menu.grid(row=1)

            next_button = Button(window, text="Next", command=lambda:[self.display_info(window, websites.get(), website_list),window_title.grid_forget(),websites_menu.grid_forget(),next_button.grid_forget()])
            next_button.grid(row=2)

    def display_info(self, window, website_name, websites):
        self.displayed_password = True

        file = open("passwords.txt","r")
        passwords_list = file.read().splitlines()
        file.close()

        file = open("usernames.txt","r")
        username_list = file.read().splitlines()
        file.close()

        line = 0
        
        for i in websites:
            if website_name == i:
                Label(window, text="Username:").grid(row=0)
                Label(window, text=username_list[line]).grid(row=1)
                Label(window, text="").grid(row=2)
                Label(window, text="Password:").grid(row=3)
                Label(window, text=passwords_list[line]).grid(row=4)
                break
            else:
                line += 1

        Button(window, text="Exit", command=lambda:window.destroy())

    def add_password_window(self):
        window = Toplevel(root)
        
        Label(window, text="Website").grid(row=0)
        Label(window, text="Username").grid(row=1)
        Label(window, text="Password").grid(row=2)
        
        website_name = Entry(window)
        website_name.grid(row=0, column=1)

        username = Entry(window)
        username.grid(row=1, column=1)
        
        password = Entry(window)
        password.grid(row=2, column=1)
        
        done = Button(window, text="Add", command=lambda:[self.store_data(website_name.get(),password.get(),username.get()),window.destroy()])
        done.grid(row=3)

    def cycle_label_text(self, event):
        self.label_index += 1
        self.label_index %= len(self.Title)
        self.label_text.set(self.Title[self.label_index])

    def store_data(self, website, password, username):
        website_names = open("websites.txt","a")
        website_names.write(website+"\n")
        website_names.close()

        password_file = open("passwords.txt","a")
        password_file.write(password+"\n")
        password_file.close()

        username_file = open("usernames.txt","a")
        username_file.write(username+"\n")
        username_file.close()

root = Tk()
TheVault = GUI(root)
root.mainloop()
