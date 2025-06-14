from tkinterdnd2 import TkinterDnD
from gui.app import StegApp

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = StegApp(root)
    root.mainloop()

