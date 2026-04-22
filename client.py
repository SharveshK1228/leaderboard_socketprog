import socket, ssl
import tkinter as tk
from tkinter import ttk

# ===== CONFIG =====
HOST = "192.168.56.1"   # 🔴 CHANGE THIS
PORT = 5000
CLIENT_NAME = "Client 1"   # 🔴 Change to Client 2 on other laptop

# ===== SSL SETUP =====
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(sock, server_hostname=HOST)
conn.connect((HOST, PORT))


# ===== FUNCTIONS =====
def update_score():
    user = entry_user.get()
    score = entry_score.get()

    if user and score:
        conn.send(f"UPDATE {user} {score}\n".encode())
        entry_score.delete(0, tk.END)


def refresh_leaderboard():
    try:
        conn.send("GET\n".encode())
        data = conn.recv(4096).decode()

        leaderboard.delete(*leaderboard.get_children())

        try:
            data_list = eval(data)
            rank = 1

            for name, score in data_list:
                tag = ""
                if rank == 1:
                    tag = "gold"
                elif rank == 2:
                    tag = "silver"
                elif rank == 3:
                    tag = "bronze"

                leaderboard.insert("", "end",
                                   values=(rank, name, score),
                                   tags=(tag,))
                rank += 1

        except:
            pass

    except:
        pass


def auto_refresh():
    refresh_leaderboard()
    root.after(2000, auto_refresh)


# ===== GUI DESIGN =====
root = tk.Tk()
root.title("🏆 Premium Leaderboard")
root.geometry("600x450")
root.configure(bg="#121212")

# ===== TITLE =====
title = tk.Label(root,
                 text="🏆 Real-Time Leaderboard",
                 font=("Segoe UI", 20, "bold"),
                 bg="#121212", fg="#00e6e6")
title.pack(pady=10)

# ===== CLIENT LABEL =====
client_label = tk.Label(root,
                        text=f"Connected as: {CLIENT_NAME}",
                        font=("Segoe UI", 10),
                        bg="#121212", fg="#aaaaaa")
client_label.pack()

# ===== INPUT FRAME =====
frame = tk.Frame(root, bg="#121212")
frame.pack(pady=10)

entry_user = tk.Entry(frame, font=("Segoe UI", 10), width=15)
entry_user.grid(row=0, column=0, padx=5)
entry_user.insert(0, "Username")

entry_score = tk.Entry(frame, font=("Segoe UI", 10), width=10)
entry_score.grid(row=0, column=1, padx=5)
entry_score.insert(0, "Score")

update_btn = tk.Button(frame,
                       text="Update",
                       command=update_score,
                       bg="#00c853", fg="white",
                       font=("Segoe UI", 10),
                       width=10)
update_btn.grid(row=0, column=2, padx=5)

refresh_btn = tk.Button(frame,
                        text="Refresh",
                        command=refresh_leaderboard,
                        bg="#2962ff", fg="white",
                        font=("Segoe UI", 10),
                        width=10)
refresh_btn.grid(row=0, column=3, padx=5)

# ===== TABLE =====
columns = ("Rank", "User", "Score")
leaderboard = ttk.Treeview(root, columns=columns, show="headings", height=10)

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#1e1e1e",
                foreground="white",
                rowheight=30,
                fieldbackground="#1e1e1e")

style.configure("Treeview.Heading",
                font=("Segoe UI", 11, "bold"))

leaderboard.heading("Rank", text="Rank")
leaderboard.heading("User", text="User")
leaderboard.heading("Score", text="Score")

leaderboard.column("Rank", anchor="center", width=80)
leaderboard.column("User", anchor="center", width=200)
leaderboard.column("Score", anchor="center", width=100)

leaderboard.pack(pady=20, fill="both", expand=True)

# ===== TAG COLORS =====
leaderboard.tag_configure("gold", background="#FFD700", foreground="black")
leaderboard.tag_configure("silver", background="#C0C0C0", foreground="black")
leaderboard.tag_configure("bronze", background="#CD7F32", foreground="black")

# ===== START AUTO REFRESH =====
auto_refresh()

root.mainloop()