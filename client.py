#!/usr/bin/env python3

import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import ssl

def send_message(event, client_socket, username, text_widget, entry_widget):
	message = entry_widget.get()
	client_socket.sendall(f"{username} > {message}".encode())

	entry_widget.delete(0, END)
	text_widget.configure(state='normal')
	text_widget.insert(END,f"{username} > {message}\n")
	text_widget.configure(state='disabled')

def receive_message(client_socket, text_widget):
	while True:
		try:
			message = client_socket.recv(1024).decode()

			if not message:
				break

			text_widget.configure(state='normal')
			text_widget.insert(END, message)
			text_widget.configure(state='disabled')

		except:
			break


def get_users_list(client_socket):

	client_socket.sendall("!usuarios".encode())


def exit_request(client_socket, username, window):

	client_socket.sendall(f"\n [+] The user {username} left the chat \n\n".encode())
	client_socket.close()
	window.quit()
	window.destroy()


def client_program():
	host = 'localhost'
	port = 12345

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket = ssl.wrap_socket(client_socket)
	client_socket.connect((host,port))

	username = input(f"\n [+] Introduce your username: ")
	client_socket.sendall(username.encode())


	window = Tk()
	window.title("Chat")

	text_widget = ScrolledText(window)
	text_widget.pack(padx=5, pady=5)

	frame_widget= Frame(window)
	frame_widget.pack(padx=5, pady=5, fill=BOTH, expand=1)
	

	entry_widget = Entry(frame_widget)
	entry_widget.bind("<Return>", lambda event: send_message(event, client_socket, username, text_widget, entry_widget))
	entry_widget.pack(side= LEFT, padx= 5, pady=5, fill = BOTH, expand = 1)

	button_widget= Button(frame_widget, text="Send", command=lambda: send_message(None, client_socket, username, text_widget, entry_widget))
	button_widget.pack(side=RIGHT, padx=5, pady= 5)
	
	users_widget = Button(frame_widget, text="Show Users", command=lambda: get_users_list(client_socket))
	users_widget.pack(pady=5, padx=5)

	exit_widget = Button(frame_widget, text="Exit", command=lambda: exit_request(client_socket, username, window))
	exit_widget.pack(padx=5, pady=5)

	
	thread = threading.Thread(target= receive_message, args=(client_socket, text_widget))
	thread.daemon = True
	thread.start()
	
	
	window.mainloop()
	client_socket.close()

if __name__ == '__main__':
	client_program()
