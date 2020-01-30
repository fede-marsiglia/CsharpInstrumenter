import sys
import re

class Instrumenter:

    def __init__(self):

        self._methodStartPattern = r'\w+[ ]*(\<.*?\>)?[ ]+\w+[ ]*\(([a-zA-Z1-9_,.=<> \s]+)?\)\s*\{'
        self._instrumentationString = "\n\t\t\tComm.Log.LogBroker.Instance.TraceDebug(\"-INSTRUMENTER-\" + Duid);\n"
        self._instrumentedFileContent = ''

    def Instrument(self, pathToFile):

        file = open(pathToFile, 'r')
        fileContent = file.read()
        file.close()

        methodStartPatternObj = re.compile(self._methodStartPattern)
        match = methodStartPatternObj.search(fileContent, re.DOTALL)

        while match is not None:

            self._instrumentedFileContent += fileContent[0: match.end()]
            fileContent = fileContent[match.end() : len(fileContent)]

            value = match.group()

            toIgnore = re.compile(r'(while|if|else if|for|switch|catch|using|ForEach|\s?new\s?)')

            if not toIgnore.match(value):

                self._instrumentedFileContent += self._instrumentationString

            match = methodStartPatternObj.search(fileContent)

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
