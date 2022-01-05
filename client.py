from email import message
import threading
import socket
import tkinter 
from tkinter import Entry, Label, StringVar, Toplevel, simpledialog, scrolledtext
import email
import smtplib
from email.message import EmailMessage
from tkinter.constants import LEFT, WORD

HOST = '127.0.0.1'
PORT = 9090



class Client:

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.msg = tkinter.Tk()
        self.msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "PLease choose a nickname", parent=self.msg)

        self.gui_done = False
        self.running = True

        # run thread that connects to the server
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        self.gui_loop()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=('Arial', 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)

        self.msg_label = Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=('Arial', 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=('Arial', 12))
        self.send_button.pack(padx=20, pady=5)

        self.send_mail_button = tkinter.Button(self.win, text="Send Mail", command=self.send_mail)
        self.send_mail_button.config(font=('Arial', 12))
        self.send_mail_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')


    def send_mail(self):

        mail = simpledialog.askstring("Mail", "Enter your mail", parent=self.msg)
        mail_password = simpledialog.askstring("Password", "Enter password", show='*', parent=self.msg)

        receiver = simpledialog.askstring("Mail", "Enter receiver mail", parent=self.msg)
        message = simpledialog.askstring("Message", "Write your message", parent=self.msg)

        # connect with port 587
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # start the connection
        server.starttls()
        # login into the server
        server.login(mail, mail_password)

        #send email
        server.sendmail(mail, receiver, message)
        message2 = '\n' + self.nickname + ' sent an email to ' + receiver + '\n'
        server.send_message(message2)
        server.quit()

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)


    def receive(self): 
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        print(message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                self.sock.close()
                break

client = Client(HOST, PORT)