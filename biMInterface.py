import tkinter as tk
from tkinter import ttk # not sure what I wanted ttk for
from bigraph import Bigraph # don't like importing just for typing
from bigraphGenerator import BigraphGenerator
from uniqueTagGenerator import UniqueTagGenerator

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

    # BUTTON
    self.button = tk.Button(self, text="generate bigraph", command=tkParent.generateAndAnalyze)
    self.button.grid(row=1, column=0)

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
        # initialize bigraph generator
        self.bigraphGenerator = BigraphGenerator()
        # initialize tag generator
        self.uniqueTagGenerator = UniqueTagGenerator()


        # initialize the main frame
        self.mainFrame = MainFrame(self)
        # need sticky to expand main frame
        self.mainFrame.grid(row=0, column=0, sticky=("N","E","S","W"))


        # need weight to expand main frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.mainloop()
    
    def drawGraph(self, g: Bigraph):
        # reserve space for the graph
        
        # paint the graph x:(0-300)
        x0 = 0 + 50
        y0 = 0 + 50
        x1 = 300 - 50
        
        x = x0
        y = y0
        # print left side vertices
        for vertex in g.left:
            tag = self.uniqueTagGenerator.generate()
            self.mainFrame.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="orange", tags=(tag))
            self.mainFrame.canvas.create_text(x, y, text=vertex, tags=(tag))
            g.vertexToTag[vertex] = tag
            y += 50

        x = x1
        y = y0
        # print right side vertices
        for vertex in g.right:
            tag = self.uniqueTagGenerator.generate()
            self.mainFrame.canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue", tags=(tag))
            self.mainFrame.canvas.create_text(x, y, text=vertex, tags=(tag))
            g.vertexToTag[vertex] = tag
            y += 50

        # print edges

    def analyze(self, g: Bigraph):
        self.drawGraph(g)

    def generateAndAnalyze(self):
        g = self.bigraphGenerator.generateBigraph()
        self.analyze(g)


if __name__ == "__main__":
    BiMInterface()