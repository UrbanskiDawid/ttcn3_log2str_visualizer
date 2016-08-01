#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
from sys import argv,exit
import pprint
from PyQt4 import QtGui
from ttcn3_log2str import ttcnlog2dict

class Window(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        QtGui.QWidget.setWindowTitle(self,"TTCN3 log2str viewer")

        layout = QtGui.QVBoxLayout(self)

        #Edit
        self.edit = QtGui.QTextEdit()
        layout.addWidget(self.edit)
        self.edit.setMaximumHeight(200);

        #Button
        self.button = QtGui.QPushButton('GO')
        layout.addWidget(self.button)

        #Tree
        self.tree= QtGui.QTreeView()
        self.tree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['name', 'val'])
        self.tree.setModel(self.model)

        layout.addWidget(self.tree)

        self.button.clicked.connect(self.onButton)

    def addLeaf(self,parent,data):
        if isinstance(data, dict):
            items=sorted(data.items())
            for key,val in items:
                child = QtGui.QStandardItem(str(key))
                row = self.addLeaf(child,val)
                parent.appendRow(row)
            return parent
        else:
            row=[]
            row.append( QtGui.QStandardItem(parent.text()) )
            row.append( QtGui.QStandardItem(str(data)) )
            return row


    def fill(self):
        self.model.removeRows(0,self.model.rowCount())

        text = unicode(self.edit.toPlainText())
        data = ttcnlog2dict(text)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)

        parent = self.model.invisibleRootItem()
        row=self.addLeaf(parent,data)

    def onButton(self):
        self.fill()

if __name__ == '__main__':
    sampleText = """my1 := { 1,2,3 }
     test2 := { a:=1, b:=2, c:={ c1:="napis" }, d := { {},{1},{2,2}} }"""

    app = QtGui.QApplication(argv)
    win = Window()
    win.resize(800, 400)
    win.edit.setText(sampleText)
    win.show()
    exit(app.exec_())
