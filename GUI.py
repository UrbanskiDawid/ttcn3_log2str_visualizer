#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from ttcn3_log2str import ttcnlog2tree,ELEMENT

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        tk.Frame.__init__(self, master)

        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2) #row1 will take more space after resize
        self.columnconfigure(0, weight=1)

        self.create_widgets()

    def processDataLeaf(self,leaf,parentID):
        parentID=self.tree.insert(parentID, 'end', text=leaf.name,  values=('#%d'%(len(leaf.val))) )
        self.dataDict[parentID]=leaf

        if type(leaf.val) is list:
           for l in leaf.val:
               if isinstance(l, ELEMENT):
                   self.processDataLeaf(l,parentID)
               else:
                   id=self.tree.insert(parentID, 'end', text=str(l), tags=('value'))
        else:
            self.tree.insert(parentID, 'end', text=str(leaf.val), tag=('value'))

    def onButton1(self):
        #remove all
        for item in self.tree.get_children():
          self.tree.delete(item)
        #get data
        text=self.text.get('1.0', 'end')
        try:
          self.dataDict=dict()
          self.data=ttcnlog2tree(text)
        except Exception as e:
          self.data=None
          print(str(e))
          return
        #process data
        for idx,f in enumerate(self.data):
            if f.name=="?": f.name="noname"+str(idx)
            self.processDataLeaf(f,'')

    def selectText(self,begin,end): #in self.text by begin char num, end char num
        text=self.text.get('1.0', 'end')
        i=-1
        rowS=1
        celS=1

        while i<len(text) and i<begin:
          i=i+1
          if text[i]=="\n":
            rowS=rowS+1
            celS=1
          else:             celS=celS+1

        i=-1
        rowE=1
        celE=1

        while i<len(text) and i<end:
            i=i+1
            if text[i]=="\n":
              rowE=rowE+1
              celE=1
            else:             celE=celE+1

        #remove selection
        ranges = self.text.tag_ranges(tk.SEL)
        for i in range(0, len(ranges), 2):
            start = ranges[i]
            stop = ranges[i+1]
            self.text.tag_remove(tk.SEL,start,stop)

        self.text.tag_add(tk.SEL, "%d.%d"%(rowS,celS), "%d.%d"%(rowE,celE))

    def onValueClicked(self,item):
        item = self.tree.selection()[0]
        parent=self.tree.parent(item)

        if parent and self.dataDict[parent]:
          e=self.dataDict[parent]
          print(self.tree.item(parent,"text"),"name",e.name,e.begin,e.end)

          self.selectText(e.begin[1]-1,e.end[1]-1)


    def create_widgets(self):

        #http://www.tkdocs.com/tutorial/text.html
        sampleText="""my1 := { 1,2,3 }
test2 := { a:=1, b:=2, c:={ c1:="napis" }, d := { {},{1},{2,2}} }"""
        self.text = tk.Text(self, width=100, height=10)
        self.text.insert('1.0', sampleText)
        self.text.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        #http://www.tkdocs.com/tutorial/widgets.html#button
        self.quit = tk.Button(self, text="GO", fg="red",  command=self.onButton1)
        self.quit.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        #http://www.tkdocs.com/tutorial/tree.html
        self.tree = ttk.Treeview(self, height=10,columns=('size'))
        self.tree['columns'] = ('size')
        self.tree.column('size', width=100, anchor='center')
        self.tree.heading('size', text='Size')
        self.tree.tag_configure('value', background='yellow')
        #self.tree.tag_bind('value', '<1>', self.onValueClicked) TODO
        self.tree.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("ttcn3 log2str visualizer")
    app = Application(master=root)
    app.mainloop()
