import socket               
import tkinter
from tkinter import messagebox
from threading import Thread

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        inputMessage.set("{Exit}")
        send()
        client.close()
        mainWindow.destroy()

def receiveMessages():
    while True:
        try:
            msg = client.recv(1024).decode("utf8") # receive UTF8 messages on a 1024 byte buffer
            messagesBox.insert(tkinter.END, msg) # insert the message at the END of the listbox that holds messages
        except OSError:  # Some sort of system error e.g. file not found, IO failure or other- probably client has lost connection.
            break

def send(event=None): #we use bind later to bind the event
    msg = entry_field.get() #get the message we've entered and store it
    inputMessage.set("")  # Clears input field.
    client.send(bytes(msg, "utf8")) #send the message (as a byte stream encoded in UTF8)
    #here we could detect certain key words and pair this with a chatbot for instance?

def handle_click(event):
    entry_field.delete()

#setup standard tkinter creation stuff
mainWindow = tkinter.Tk()
mainWindow.title("PyChat Instant Messaging")
mainWindow.geometry("700x500")
messageFrame = tkinter.Frame(mainWindow) #container for the messaging stuff
inputFrame = tkinter.Frame(mainWindow)
inputMessage = tkinter.StringVar()  # container for the messages to be sent.
inputMessage.set("Please enter message...") # pre made message to send
scrollbar = tkinter.Scrollbar(messageFrame)  # scrollbar to scroll through messages.

# setup stuff to hold sent/ received messages
# listboxes height and width is in lines and characters!
messagesBox = tkinter.Listbox(messageFrame, height=20, width=55, yscrollcommand=scrollbar.set)
messagesBox.config(font=("Arial", 14))
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y) #put the scrollbar on the right
messagesBox.pack(side=tkinter.LEFT, fill=tkinter.BOTH) # and the messages on the left
messagesBox.pack()
messageFrame.pack()

# setup frame for entering and sending message
entry_field = tkinter.Entry(inputFrame, width=40, textvariable=inputMessage) #entry for entering messages
entry_field.config(font=("Arial", 14))
entry_field.bind("<Return>", send) #bind the send event to enter when pressed in entry
entry_field.pack(side=tkinter.LEFT) 
entry_field.bind("<1>",handle_click) #bind a delete to press

send_button = tkinter.Button(inputFrame, text="Send", command=send)
send_button.pack(side=tkinter.RIGHT)
inputFrame.pack()

mainWindow.protocol("WM_DELETE_WINDOW", on_closing)

client = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
host = "127.0.0.1"          # localhost IP
port = 65430                # Reserve a port to communicate on.
client.connect((host, port))        # Bind to the port
receive_thread = Thread(target=receiveMessages) #setup a new thread for receiving messages so it's not blocked
receive_thread.start()
tkinter.mainloop()  # Start the GUI and program