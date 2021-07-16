import sys
import re

class Instrumenter:

    def __init__(self):

        self._class = r'((public)|(private)|(protected))\s*(sealed)?\s*(partial)?\s*class\s+(\w+).*?\{'
        self._classRx = re.compile(self._class, re.DOTALL)
        self._instrumentedFileContent = ''

    def Instrument(self, pathToFile):

        file = open(pathToFile, 'r')
        fileContent = file.read()
        file.close()

        classMatch = self._classRx.search(fileContent)

        while classMatch is not None:

            count = len(classMatch.groups())
            className = classMatch.group(count)
            constructor = r'((public)|(private)|(protected))\s+' + className + '\s*(\(.*?\))?(\s*\:.*?)?\s*((\{)|(=>))'
            constructorRx = re.compile(constructor, re.DOTALL)

            self._instrumentedFileContent += fileContent[0: classMatch.end()]
            self._instrumentedFileContent += "\n\t\t~" + className + '() => Comm.Common.Utils.Dealloc(GetType().ToString());'
            fileContent = fileContent[classMatch.end(): len(fileContent)]

            constructorMatch = constructorRx.search(fileContent)

            if constructorMatch is None:

                self._instrumentedFileContent += "\n\t\t public " + className + "() { Comm.Common.Utils.Alloc(GetType().ToString()); }"

            else:

                while constructorMatch is not None:

                    constructorBodyStart = constructorMatch.end()
                    self._instrumentedFileContent += fileContent[0: constructorBodyStart]
                    self._instrumentedFileContent += "\n\t\t\t Comm.Common.Utils.Alloc(GetType().ToString());"
                    fileContent = fileContent[constructorBodyStart : len(fileContent)]
                    constructorMatch = constructorRx.search(fileContent)

            classMatch = self._classRx.search(fileContent)

        self._instrumentedFileContent += fileContent

        if '' != self._instrumentedFileContent:

            file = open(pathToFile, 'w')
            file.write(self._instrumentedFileContent)
            file.close()
            self._instrumentedFileContent = ''



if __name__ == "__main__":

    instrumenter = Instrumenter()

    for i in range(1, len(sys.argv)):
        toInstrument = sys.argv[i]
        print('STO PARSANDO ====> ' + toInstrument)
        instrumenter.Instrument(toInstrument)
