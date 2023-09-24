from tkinter import ttk # not sure what I wanted ttk for
from bigraph import Bigraph # don't like importing just for typing
from bigraphGenerator import BigraphGenerator
from uniqueTagGenerator import UniqueTagGenerator
from animatedHopcroftKarp import AnimatedHopcroftKarp
from subgraphIntersection import SubgraphIntersection
from singlePath import SinglePath
import tkinter as tk
import logging

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

    pauseDuration = 0
    self.slider = ttk.Scale(self, orient="horizontal", length=100, from_=0, to=1, variable=pauseDuration, command=tkParent.animatedHopcroftKarp.changePauseDuration)
    self.slider.grid(row=2, column = 0)

    # TEMP
    #self["bg"] = "black"
    #self.canvas.create_oval(-10, -10, 10, 10, fill="green")

    # smallest scrollable region that contains everything on the canvas
    #self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    # weights for expanding canvas
    self.columnconfigure(1, weight=1)
    self.rowconfigure(0, weight=1)

class BiMInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('BiM')
        self.bigraphGenerator = BigraphGenerator()
        self.uniqueTagGenerator = UniqueTagGenerator()
        self.animatedHopcroftKarp = AnimatedHopcroftKarp()
        self.subgraphIntersection = SubgraphIntersection()
        self.singlePath = SinglePath()

        self.maxGraphSlots = 8
        self.graphWidth = 300

        # initialize the main frame
        self.mainFrame = MainFrame(self)
        # need sticky to expand main frame
        self.mainFrame.grid(row=0, column=0, sticky=("N","E","S","W"))

        self.animatedHopcroftKarp.setCanvas(self.mainFrame.canvas)

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
        for vertex in range(len(g.edges)):
            tag = self.uniqueTagGenerator.generate()
            self.mainFrame.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="orange", tags=(tag))
            self.mainFrame.canvas.create_text(x, y, text=vertex, tags=(tag))
            g.vertexToTag[vertex] = tag
            y += 50

        # draw right side vertices
        x = rightColumnX
        y = fristRowY
        for vertex in range(len(g.edges), len(g.edges) + len(g.edges[0])):
            tag = self.uniqueTagGenerator.generate()
            self.mainFrame.canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue", tags=(tag))
            self.mainFrame.canvas.create_text(x, y, text=vertex, tags=(tag))
            g.vertexToTag[vertex] = tag
            y += 50

        # Curiously, running canvas.coords(tag), with multiple items having that tag, gives us only
        # 1 set of coords, looks like the more inclusive one.

        # draw edges
        for v in range(len(g.edges)):
            for w in range(len(g.edges), len(g.edges) + len(g.edges[0])):
                if g.edges[v][w - len(g.edges)] == 1:
                    tag = self.uniqueTagGenerator.generate()
                    vx, vy, _, _ = self.mainFrame.canvas.coords(g.vertexToTag[v])
                    wx, wy, _, _ = self.mainFrame.canvas.coords(g.vertexToTag[w])
                    self.mainFrame.canvas.create_line(vx+10, vy+10, wx+10, wy+10, fill="white", width=2, tags=(tag))
                    g.edgeToTag[(v, w)] = tag

        self.mainFrame.canvas.config(scrollregion=[0, 0, self.graphWidth, y])

    def analyze(self, g: Bigraph):
        self.drawGraph(g)
        logging.debug("GRAPH DRAWN")
        self.animatedHopcroftKarp.hopcroftKarp(g)
        for row in range(len(g.matching)):
            for column in range(len(g.matching[0])):
                if g.matching[row][column] == 1:
                    self.mainFrame.canvas.itemconfig(g.edgeToTag[(row, column + len(g.edges))], fill="green")

        # idea 1
        # find a maximum matching using hk
        # find all other possible maximum matchings
        # pay attention to the relationship of edges in a mmatching
        # may be base it off of my subgraph approach =>
        # identify what type of component it is (intersection or path)
        # and then find out what decision was made and see if there are decipherable rules

        # idea 2
        # Come up with a partially correct algorithm. Then run it and hk through a group graphs.
        # When results don't match try to adjust the rules for the algorithm to make it work.
        # Repeat until algo works on every graph.

        # idea 3
        # Come up with partially correct algorithm. Once it gets it's matching, use a.p.s to
        # push it to a maximum matching. Then figure out new rules? The challenge is handling
        # bundles of intersections

    def generateAndAnalyze(self):
        g = self.bigraphGenerator.generateBigraph()
        self.analyze(g)


if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format="%(message)s")
    BiMInterface()