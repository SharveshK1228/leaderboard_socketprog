import socket, ssl, threading, time
import tkinter as tk
from tkinter import ttk

# ===== DATA =====
leaderboard = {}
clients = {}
lock = threading.Lock()

# ===== HANDLE CLIENT =====
def handle_client(conn, addr):
    ip = addr[0]

    with lock:
        clients[ip] = {"status": "Active", "last_seen": time.strftime("%H:%M:%S")}

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            parts = data.strip().split()
            cmd = parts[0]

            with lock:
                clients[ip]["status"] = "Active"
                clients[ip]["last_seen"] = time.strftime("%H:%M:%S")

                if cmd == "UPDATE":
                    user = parts[1]
                    score = int(parts[2])
                    leaderboard[user] = score

                elif cmd == "GET":
                    sorted_board = sorted(leaderboard.items(), key=lambda x: -x[1])
                    conn.send((str(sorted_board) + "\n").encode())

        except:
            break

    with lock:
        clients[ip]["status"] = "Disconnected"

    conn.close()


# ===== SERVER THREAD =====
def start_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("ssl_cert.pem", "ssl_key.pem")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen(5)

    print("🚀 Server running with GUI...")

    while True:
        client, addr = server.accept()
        secure_conn = context.wrap_socket(client, server_side=True)

        threading.Thread(target=handle_client, args=(secure_conn, addr), daemon=True).start()


# ===== GUI UPDATE =====
def update_gui():
    client_table.delete(*client_table.get_children())

    with lock:
        for ip, info in clients.items():
            client_table.insert("", "end",
                                values=(ip, info["status"], info["last_seen"]))

    leaderboard_table.delete(*leaderboard_table.get_children())

    with lock:
        sorted_board = sorted(leaderboard.items(), key=lambda x: -x[1])
        rank = 1
        for name, score in sorted_board:
            leaderboard_table.insert("", "end",
                                     values=(rank, name, score))
            rank += 1

    root.after(2000, update_gui)


# ===== GUI DESIGN =====
root = tk.Tk()
root.title("🖥️ Server Dashboard")
root.geometry("700x500")
root.configure(bg="#121212")

title = tk.Label(root,
                 text="🖥️ Server Monitoring Dashboard",
                 font=("Segoe UI", 18, "bold"),
                 bg="#121212", fg="#00e6e6")
title.pack(pady=10)

# ===== CLIENT TABLE =====
tk.Label(root, text="Active Clients",
         bg="#121212", fg="white",
         font=("Segoe UI", 12)).pack()

columns1 = ("IP Address", "Status", "Last Active")
client_table = ttk.Treeview(root, columns=columns1, show="headings", height=6)

for col in columns1:
    client_table.heading(col, text=col)
    client_table.column(col, anchor="center")

client_table.pack(pady=10, fill="x")

# ===== LEADERBOARD TABLE =====
tk.Label(root, text="Leaderboard",
         bg="#121212", fg="white",
         font=("Segoe UI", 12)).pack()

columns2 = ("Rank", "User", "Score")
leaderboard_table = ttk.Treeview(root, columns=columns2, show="headings", height=8)

for col in columns2:
    leaderboard_table.heading(col, text=col)
    leaderboard_table.column(col, anchor="center")

leaderboard_table.pack(pady=10, fill="both", expand=True)

# ===== START SERVER THREAD =====
threading.Thread(target=start_server, daemon=True).start()

# ===== AUTO UPDATE GUI =====
update_gui()

root.mainloop()