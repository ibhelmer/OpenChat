#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project : OpenChat
File    : Clienet.py
Author  : Ib Helmer Nielsen
Version : 0.1.0
Email   : ihn@ucn.dk
Status  : Prove of concept
License : MPL 2.0
Description: Simpel chat system. The communication is unencrypted and based on tcp.
             The client have a graphic user interface, where message to the chat can be entered and send and a part
             that shows messages from other users. When a client login to the system a dialog box will ask for
             nickname of user.
"""
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

# Ip address of server
HOST = '127.0.0.1'
# Port on server used for chat client connections
PORT = 7913

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))

        msg = tkinter.Tk()
        msg.withdraw()
        self.nickname = simpledialog.askstring("Nickname", "Please chose a nickname", parent=msg)
        self.gui_done = False
        self.running =True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win =tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial",12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win,height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button=tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial",12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW",self.stop)
        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0','end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0','end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client1 = Client(HOST,PORT)
client2 = Client(HOST,PORT)