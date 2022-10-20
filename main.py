from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot, QCoreApplication
from mainwindow import Ui_MainWindow
import sys
from model import Model

# begin PDFsearch imports
import PyPDF2
import re
import os
import glob
from pathlib import Path
import fitz
from io import FileIO
from timeit import default_timer as timer

import itertools


class MainWindowUIClass(Ui_MainWindow):

    def __init__(self):
        # Initialize the super class
        super().__init__()
        self.model = Model()

    def setupUi(self, MW):
        ''' Setup the UI of the super class, and add here code
        that relates to the way we want our UI to operate.
        '''
        super().setupUi(MW)

    def debugPrint(self, msg):
        self.debugTextBrowser.append(msg)

    def refreshAll(self):
        '''
        Updates the widgets whenever an interaction happens.
        Typically some interaction takes place, the UI responds,
        and informs the model of the change.  Then this method
        is called, pulling from the model information that is
        updated in the GUI.
        '''
        self.lineEdit.setText(self.model.getFileName())
        # self.lineEdit_3.setText(self.model.getDirName())
        # self.textEdit.setText( self.model.getFileContents() )

    def refreshAllOutFile(self):
        self.lineEdit_4.setText(self.model.getOutFileName())

    def returnSearchTerms(self):
        searchTerms = self.lineEdit_2.text()
        return searchTerms

    def returnWholeWordSearchTerms(self):
        wholeWordSearchTerms = self.lineEdit_3.text()
        return wholeWordSearchTerms

    # slot
    def exitProgramSlot(self):
        sys.exit(QtWidgets.QApplication.exec_())

    # slot
    def browseSlot(self):
        ''' Called when the user presses the Browse button
        '''
        options = QtWidgets.QFileDialog.Options()
        # options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Select PDF File",
            "",
            "All Files (*);;PDF Files (*.pdf)",
            options=options)

        if fileName:
            self.model.setFileName(fileName)
            self.refreshAll()

    def browseSaveFileSlot(self):
        options = QtWidgets.QFileDialog.Options()
        outFileName, _ = QtWidgets.QFileDialog.getSaveFileName(
            None,
            "Save File",
            "C:\\",
            "PDF File (*.pdf)",
            options=options)
        if outFileName:
            self.debugPrint("File will be saved to:" + outFileName)
            self.model.setOutFileName(outFileName)
            self.refreshAllOutFile()




    def PDFsearch(self):
        searchString = self.returnSearchTerms()
        wholeWord = self.returnWholeWordSearchTerms()
        wordList = re.sub(";", " ", searchString).split()
        wholeWordList = re.sub(";", " ", wholeWord).split()

        searchList = re.compile(r'|'.join(wordList), re.IGNORECASE)
        wholeWordSearchList = re.compile(r'|'.join(wholeWordList), re.IGNORECASE)
        #wholeWordSearchList = re.compile(r'|'.join(wholeWordList), re.IGNORECASE)
        #wholeWordSearchList = r'\b(?:{})\b'.format('|'.join(wholeWordList))
        #wholeWordSearchList = rf'\b(?:{"|".join(map(re.escape, wholeWordList))})\b'

        inputFile = self.model.getFileName()
        outputFile = self.model.getOutFileName()
        object2 = PyPDF2.PdfFileReader(FileIO(inputFile), strict=False)

        object = fitz.Document(inputFile)
        # doc = fitz.open(docPath)
        # numPages = doc.pageCount
        # page = doc[0]

        NumPages = object.page_count
        output = PyPDF2.PdfFileWriter()
        foundPages = []

        # Do the search
        for i in range(0, NumPages):
            # PageObj = object.getPage(i)
            PageObj = object[i]
            p = i + 1
            Text = PageObj.get_text()
            Text_WordsOnly = PageObj.get_text("words")
            self.debugPrint("Checking page " + str(p))
            QtWidgets.QApplication.processEvents()
            if re.search(searchList, Text):
                self.debugPrint("File: " + str(inputFile) + "  |  " + "Page: " + str(p))
                foundPages.append(i)
            else:
                for text in Text_WordsOnly:
                    if re.fullmatch(wholeWordSearchList,text[4]):
                        self.debugPrint("File: " + str(inputFile) + "  |  " + "Page: " + str(p))
                        foundPages.append(i)
                        break

        self.debugPrint("Saving " + str(len(foundPages)) + " Pages to file.  Please wait...")
        QtWidgets.QApplication.processEvents()

        for page in foundPages:
            p = page + 1
            self.debugPrint("Writing page " + str(p))
            QtWidgets.QApplication.processEvents()
            output.addPage(object2.getPage(page))

        with open(str(outputFile), "wb") as outputStream:
            output.write(outputStream)

        outputFilepath = str(self.model.getOutFileName())
        if not os.path.exists(str(outputFilepath)):
            self.debugPrint("No results found.  Make sure PDF is searchable/OCR'd.  Press any key to exit.")
            QtWidgets.QApplication.processEvents()
            return

        docPath = Path(self.model.getOutFileName())
        doc = fitz.Document(docPath)
        numPages = doc.page_count
        page = doc[0]

        for i in range(0, numPages):
            page = doc[i]
            #Text = page.get_text()
            Text_WordsOnly = page.get_text("words")
            for word in wordList:
                text_instances = page.search_for(word, hit_max=100)
                for inst in text_instances:
                    print(page, inst, type(inst))
                    highlight = page.add_highlight_annot(inst)

            for text in Text_WordsOnly:
                if re.fullmatch(wholeWordSearchList, text[4]):
                        print(page, "word in ", text[4])
                        highlight = page.add_highlight_annot(text[0:4])

            '''
            for word in wholeWordSearchList:
                text_instances = page.search_for(word, hit_max=100)
                for inst in text_instances:
                    print(page, inst, type(inst))
                    highlight = page.add_highlight_annot(inst)
            '''



        # doc.save(docPath, garbage=4, deflate=True, clean=True)
        doc.saveIncr()
        self.debugPrint("-------------------------------------------------------")
        self.debugPrint("Finished.  File saved to " + str(docPath))

    def runIt(self):
        start = timer()
        searchString = self.returnSearchTerms()
        wordList = re.sub(";", " ", searchString).split()
        self.debugPrint("STARTING...")
        self.debugPrint("Searching file: " + self.model.getFileName())
        self.debugPrint("Searching for the following terms: " + str(wordList))
        self.PDFsearch()
        end = timer()
        totalTime = (end - start)
        self.debugPrint("Total time to process: " + str(totalTime) + " seconds.")
        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUIClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


main()
