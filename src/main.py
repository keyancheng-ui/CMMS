import tkinter as tk
from src.db import initialize_database
from ui.general_gui import QuickQueryGUI

from logic.general_service import Service

def main():
    print("start to initialize database...")
    password = input("Input your own mySQL password: ")

    # use all default values
    initialize_database(password = password)

    print("database initialization finished")
    print("the system is now ready for use")

    root = tk.Tk()
    root.geometry("900x900")  # 初始窗口大小
    app = QuickQueryGUI(root, password)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()





