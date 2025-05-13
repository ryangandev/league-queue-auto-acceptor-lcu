import asyncio
import threading
import tkinter as tk
from tkinter import scrolledtext
from lcu_driver import Connector

# LCU connector
connector = Connector()

# Global state (linked to GUI)
app_running = True
lcu_connected = False


# GUI setup
class AppGUI:
    def __init__(self, root):
        self.root = root
        root.title("League Auto Acceptor")
        root.geometry("500x400")

        self.status_label = tk.Label(root, text="Status: Not Connected", fg="red")
        self.status_label.pack(pady=10)

        self.listen_button = tk.Button(
            root,
            text="Start Listening",
            state=tk.DISABLED,
            command=self.start_listening,
        )
        self.listen_button.pack(pady=5)

        self.log_area = scrolledtext.ScrolledText(root, width=60, height=15)
        self.log_area.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.pack(pady=5)

    def update_status(self, connected: bool):
        if connected:
            self.status_label.config(text="Status: Connected to Client", fg="green")
            self.listen_button.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="Status: Not Connected", fg="red")
            self.listen_button.config(state=tk.DISABLED)

    def log(self, text: str):
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.see(tk.END)

    def start_listening(self):
        self.log("Started listening for queue events... (Not implemented yet)")

    def exit_app(self):
        global app_running
        app_running = False
        self.root.destroy()


# LCU Event: On Connected
@connector.ready
async def connect(connection):
    global lcu_connected
    lcu_connected = True
    gui.update_status(True)
    gui.log("[+] Connected to League Client.")


# LCU Event: On Disconnected
@connector.close
async def disconnect(_):
    global lcu_connected
    lcu_connected = False
    gui.update_status(False)
    gui.log("[x] Disconnected from League Client.")


# Async loop to run LCU connector
def start_lcu_connector():
    connector.start()


# Run GUI and LCU connector in parallel
def start_gui():
    root = tk.Tk()
    global gui
    gui = AppGUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.exit_app)
    root.mainloop()


if __name__ == "__main__":
    # Start LCU connector in a background thread
    threading.Thread(target=start_lcu_connector, daemon=True).start()
    # Run GUI in main thread
    start_gui()
