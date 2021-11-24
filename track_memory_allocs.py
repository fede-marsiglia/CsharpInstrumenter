import sys
import re

class Instrumenter:

    def __init__(self):

        self._class = r'((public)|(private)|(protected))\s*(sealed)?\s*(partial)?\s*class\s+(\w+).*?\{'
        self._classRx = re.compile(self._class, re.DOTALL)
        self._instrumentedFileContent = ''
        self._alloc = '\n#if DEBUG\n \t\tComm.Common.Utils.Alloc(GetType().ToString()); \n#endif\n'
        self._dealloc = '\n#if DEBUG\n \t\tComm.Common.Utils.Dealloc(GetType().ToString()); \n#endif\n'
        self._bodyOpening = r'.*?(\{)|(=>)'
        self._bodyOpeningRx = re.compile(self._bodyOpening, re.DOTALL)

    def Instrument(self, pathToFile):

        file = open(pathToFile, 'r')
        fileContent = file.read()
        file.close()

        classMatch = self._classRx.search(fileContent)

        while classMatch is not None:

            count = len(classMatch.groups())
            className = classMatch.group(count)

            self._instrumentedFileContent += fileContent[0: classMatch.end()]
            fileContent = fileContent[classMatch.end(): len(fileContent)]

            self._instrumentedFileContent += "\n\t\t~" + className + '() {' + self._dealloc + '}\n\n'

            constructorDefault = className + r'(\s*\(\s*\))'
            constructorDefaultRx = re.compile(constructorDefault, re.DOTALL)
            constructorDefaultMatch = constructorDefaultRx.search(fileContent)

            if constructorDefaultMatch is None:
               self._instrumentedFileContent += "\n\t\t" + className + '() { }'

            constructor = r'((public)|(private)|(protected))\s+' + className + r'(\s*\(.*?\).*?)((\{)|(=>.*?;))'
            constructorRx = re.compile(constructor, re.DOTALL)
            constructorMatch = constructorRx.search(fileContent)

            while constructorMatch is not None:

                constructorBodyStart = constructorMatch.span(5)[1]
                bodyContent = constructorMatch.group(6)

                if constructorMatch.group(0).find('=>') != -1:
                    self._instrumentedFileContent += fileContent[0: constructorBodyStart] + '{' + self._alloc + bodyContent.replace('=>', '') + '\n\t\t}'
                else:
                    self._instrumentedFileContent += fileContent[0: constructorBodyStart] + '{' + self._alloc

                fileContent = fileContent[constructorMatch.end() : len(fileContent)]
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
        print('Parsing => ' + toInstrument)
        instrumenter.Instrument(toInstrument)
