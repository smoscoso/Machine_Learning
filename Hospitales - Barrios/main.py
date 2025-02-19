import tkinter as tk
from View.GUI import HospitalDistributionView
from controller.app_controller import AppController

def main():
    root = tk.Tk()
    view = HospitalDistributionView(root)
    AppController(view)
    root.mainloop()

if __name__ == "__main__":
    main()
