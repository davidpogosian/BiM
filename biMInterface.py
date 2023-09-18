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
    self.canvas = tk.Canvas(self, width=300, height=300, background="black")
    self.canvas.grid(row=0, column=1, sticky=("N","E","S","W"))

    # scrollbars for canvas
    self.verticalScrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
    self.horizontalScrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
    self.verticalScrollbar.grid(row=0, column=2, sticky=("N", "S"))
    self.horizontalScrollbar.grid(row=1, column=1, sticky=("E","W"))
    
    # hook up scrollbars to canvas
    self.canvas.config(xscrollcommand=self.horizontalScrollbar.set, yscrollcommand=self.verticalScrollbar.set)


    # TEMP
    self["bg"] = "black"
    self.canvas.create_oval(-10, -10, 10, 10, fill="green")

    # smallest scrollable region that contains everything on the canvas
    #self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    # weights for expanding canvas
    self.columnconfigure(1, weight=1)
    self.rowconfigure(0, weight=1)

class BiMInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('BiM')
        # initialize bigraph generator
        self.bigraphGenerator = BigraphGenerator()
        # initialize tag generator
        self.uniqueTagGenerator = UniqueTagGenerator()

        self.maxGraphSlots = 8
        self.graphWidth = 300

        # initialize the main frame
        self.mainFrame = MainFrame(self)
        # need sticky to expand main frame
        self.mainFrame.grid(row=0, column=0, sticky=("N","E","S","W"))


        # need weight to expand main frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.mainloop()
    
    def drawGraph(self, g: Bigraph) -> None:
        # reserve space for the graph
        
        # paint the graph
        leftColumnX = 0 + 50
        fristRowY = 0 + 50
        rightColumnX = self.graphWidth - 50
        
        tag = self.uniqueTagGenerator.generate()
        self.mainFrame.canvas.create_text((leftColumnX + rightColumnX)/2, fristRowY - 25, text=g.name, fill="red", tags=(tag))
        g.nameTag = tag

        # draw left side vertices
        x = leftColumnX
        y = fristRowY
        for vertex in g.left:
            tag = self.uniqueTagGenerator.generate()
            self.mainFrame.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="orange", tags=(tag))
            self.mainFrame.canvas.create_text(x, y, text=vertex, tags=(tag))
            g.vertexToTag[vertex] = tag
            y += 50

        # draw right side vertices
        x = rightColumnX
        y = fristRowY
        for vertex in g.right:
            tag = self.uniqueTagGenerator.generate()
            self.mainFrame.canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue", tags=(tag))
            self.mainFrame.canvas.create_text(x, y, text=vertex, tags=(tag))
            g.vertexToTag[vertex] = tag
            y += 50

        # Curiously, running canvas.coords(tag), with multiple items having that tag, gives us only
        # 1 set of coords, looks like the more inclusive one.

        # draw edges
        for v in list(g.edges.keys()):
            for w in g.edges[v]:
                tag = self.uniqueTagGenerator.generate()
                vx, vy, _, _ = self.mainFrame.canvas.coords(g.vertexToTag[v])
                wx, wy, _, _ = self.mainFrame.canvas.coords(g.vertexToTag[w])
                self.mainFrame.canvas.create_line(vx+10, vy+10, wx+10, wy+10, fill="pink", tags=(tag))
                g.edgeToTag[(v, w)] = tag

        self.mainFrame.canvas.config(scrollregion=[0, 0, self.graphWidth, y])

    def analyze(self, g: Bigraph):
        self.drawGraph(g)

    def generateAndAnalyze(self):
        g = self.bigraphGenerator.generateBigraph()
        self.analyze(g)


if __name__ == "__main__":
    BiMInterface()