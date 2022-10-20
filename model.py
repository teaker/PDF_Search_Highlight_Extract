# model.py
# D. Thiebaut
# This is the model part of the Model-View-Controller
# The class holds the name of a text file and its contents.
# Both the name and the contents can be modified in the GUI
# and updated through methods of this model.
#

class Model:
    def __init__(self):
        '''
        Initializes the two members the class holds:
        the file name and its contents.
        '''
        self.fileName = None
        self.fileContent = ""

    def isValid(self, fileName):
        '''
        returns True if the file exists and can be
        opened.  Returns False otherwise.
        '''
        try:
            file = open(fileName, 'r')
            file.close()
            return True
        except:
            return False

    def setFileName(self, fileName):
        '''
        sets the member fileName to the value of the argument
        if the file exists.  Otherwise resets both the filename
        and file contents members.
        '''
        if self.isValid(fileName):
            self.fileName = fileName
        else:
            self.fileName = ""

    def getFileName(self):
        '''
        Returns the name of the file name member.
        '''
        return self.fileName


    def setOutFileName(self, outFileName):
        '''
        sets the member fileName to the value of the argument
        if the file exists.  Otherwise resets both the filename
        and file contents members.

        if self.isValid(dirName):
            self.dirName = dirName
            #self.fileContents = open(fileName, 'r').read()
        else:
            #self.fileContents = ""
            self.dirName = ""
        '''
        self.outFileName = outFileName

    def getOutFileName(self):
        '''
        Returns the name of the file name member.
        '''
        return self.outFileName

