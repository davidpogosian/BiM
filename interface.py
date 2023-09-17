import tkinter as tk
from tkinter import ttk # not sure what I wanted ttk for

class Panel(tk.Frame):
    def __init__(self, tkParent):
        super().__init__(tkParent)

        # TEMPORARY
        tk.Label(self, text="PANEL HERE").grid(row=0, column=0)
    
class MainFrame(tk.Frame):
  def __init__(self, tkParent):
    super().__init__(tkParent)

    # PANEL
    self.panel = Panel(self)
    self.panel.grid(row=0, column=0)

    # CANVAS
    self.canvas = tk.Canvas(self, width=300, height=300, background="black", scrollregion=(0, 0, 1000, 1000))
    self.canvas.grid(row=0, column=1, sticky=("N","E","S","W"))

    # scrollbars for canvas
    self.verticalScrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
    self.horizontalScrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
    self.verticalScrollbar.grid(row=0, column=2, sticky=("N", "S"))
    self.horizontalScrollbar.grid(row=1, column=1, sticky=("E","W"))
    
    # hook up scrollbars to canvas
    self.canvas.config(xscrollcommand=self.horizontalScrollbar.set, yscrollcommand=self.verticalScrollbar.set)


    # TEMP
    print(self.canvas.create_line(0, 0, 300, 300, fill="green", width=10))
    print(self.canvas.create_line(0, 100, 300, 300, fill="red", width=10))
    self["bg"] = "blue"

    # smallest scrollable region that contains everything on the canvas
    #self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    # weights for expanding canvas
    self.columnconfigure(1, weight=1)
    self.rowconfigure(0, weight=1)

    # PANNING & ZOOMING HAS STRANGE EFFECTS
    # panning & zooming
    def do_zoom(event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.canvas.scale(tk.ALL, x, y, factor, factor)

    # binds for panning & zooming
    self.canvas.bind("<MouseWheel>", do_zoom)
    self.canvas.bind('<ButtonPress-1>', lambda event: self.canvas.scan_mark(event.x, event.y))
    self.canvas.bind("<B1-Motion>", lambda event: self.canvas.scan_dragto(event.x, event.y, gain=1))

class BiMInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('BiM')


        # initialize the main frame
        self.mainFrame = MainFrame(self)
        # need sticky to expand main frame
        self.mainFrame.grid(row=0, column=0, sticky=("N","E","S","W"))


        # need weight to expand main frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.mainloop()
    
    def clearCanvas(self):
        self.mainFrame.canvas.delete("all")

    def loadGrapg(self, g):
        pass
    
    def drawGraph(self, g):
        pass


if __name__ == "__main__":
    BiMInterface()