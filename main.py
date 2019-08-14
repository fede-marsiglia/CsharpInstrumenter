import sys
import re

class Instrumenter:

    def __init__(self):

        self._methodStartPattern = r'\w+[\t ]+\w+[\t ]?\(.*?\)*?\n?.*?\{'
        self._instrumentationString = '\n\n LogBroker.Instance.TraceDebug(\"sto eseguendo \" + ' \
                                      'System.Reflection.MethodBase.GetCurrentMethod().Name) \n\n '
        self._instrumentedFileContent = ''

    def Instrument(self, pathToFile):

        file = open(pathToFile, 'r')
        fileContent = file.read()
        file.close()

        methodStartPatternObj = re.compile(self._methodStartPattern)
        match = methodStartPatternObj.search(fileContent)

        while match is not None:

            self._instrumentedFileContent += fileContent[0: match.end()]
            fileContent = fileContent[match.end() + 1 : len(fileContent)]

            value = match.group()

            toIgnore1 = re.compile(r'^[\t ]?(while|if|for|switch)')
            toIgnore2 = re.compile(r'ForEach')
            toIgnore3 = re.compile(r'[ ]?new[ ]?')

            if not toIgnore1.match(value) and not \
                   toIgnore2.match(value) and not \
                   toIgnore3.match(value):

                self._instrumentedFileContent += self._instrumentationString

            match = methodStartPatternObj.search(fileContent)

        self._instrumentedFileContent += fileContent

        if self._instrumentedFileContent != '':

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
