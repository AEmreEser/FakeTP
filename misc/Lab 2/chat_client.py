import socket
import threading
import tkinter as tk

def get_message(s, insert):
    while True:
        data = s.recv(1024)
        print("received", data)
        insert(tk.END, data.decode())


def send_message(s, nickname, grab):
    data = f"[{nickname}] - {grab()}"
    s.sendall(data.encode())


# initial configuration screen
initial = tk.Tk()
initial.title("Server Configuration")

initial.rowconfigure([0, 1], minsize=25, weight=1)
initial.columnconfigure(0, minsize=100, weight=1)

# server configuration part start
frm_input = tk.Frame(master=initial, relief=tk.RIDGE, borderwidth=3)

lbl_server = tk.Label(master=frm_input, text="Server Address")
ent_server = tk.Entry(master=frm_input, width=30)

lbl_port = tk.Label(master=frm_input, text="Port")
ent_port = tk.Entry(master=frm_input, width=10)

lbl_colon = tk.Label(master=frm_input, text=":")

lbl_server.grid(row=0, column=0)
ent_server.grid(row=1, column=0, padx=5, pady=5)

lbl_colon.grid(row=1, column=1)

lbl_port.grid(row=0, column=2)
ent_port.grid(row=1, column=2, padx=5, pady=5)

frm_input.grid(row=0, column=0, padx=10, pady=20)
# server configuration part end

# nickname part start
lbl_nickname = tk.Label(master=initial, text="Nickname")
ent_nickname = tk.Entry(master=initial, width=30)

lbl_nickname.grid(row=1, column=0)
ent_nickname.grid(row=2, column=0, pady=10)
# nickname part end


def create_message_window(s, nickname):
    initial.destroy()

    chat = tk.Tk()
    chat.title("Enjoy the Chat")

    chat.rowconfigure([0, 1], minsize=25, weight=1)
    chat.columnconfigure(0, minsize=100, weight=1)

    # history frame startß
    frm_history = tk.Frame(master=chat, relief=tk.RIDGE, borderwidth=3)

    listbox_history = tk.Listbox(master=frm_history, width=150, height=50)
    listbox_history.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(master=frm_history, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

    listbox_history.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox_history.yview)

    frm_history.grid(row=0, column=0)
    # history frame end

    # message frame start
    frm_message = tk.Frame(master=chat, relief=tk.SUNKEN, borderwidth=3, bg="gray")

    ent_message = tk.Entry(master=frm_message, width=50)
    btn_send = tk.Button(master=frm_message, text="Send", width=10, command=lambda: send_message(s, nickname, ent_message.get))

    ent_message.grid(row=0, column=0, padx=5, pady=5)
    btn_send.grid(row=0, column=1, padx=5, pady=5)

    frm_message.grid(row=1, column=0, padx=10, pady=10)
    # message frame end

    t = threading.Thread(target=get_message, args=(s, listbox_history.insert))
    t.start()

    chat.mainloop()


def connect_to_server():
    host = ent_server.get()
    port = int(ent_port.get())
    nickname = ent_nickname.get()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    create_message_window(s, nickname)


btn_connect = tk.Button(master=initial, text="Connect", relief=tk.RAISED, borderwidth=2, command=connect_to_server)
btn_connect.grid(row=3, column=0)

initial.mainloop()
