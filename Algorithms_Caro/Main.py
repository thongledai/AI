# Điểm chạy chính của trò chơi Caro 3x3.
import sys
import os
import tkinter as tk

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from GUI import CaroGUI

def main():
    root = tk.Tk()
    app = CaroGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
