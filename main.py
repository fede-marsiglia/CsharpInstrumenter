import sys
import re

class Instrumenter:

    def __init__(self):

        self._methodStartPattern = r'\w+[\t ]?\(.*?\)*?\n?.*?\{'
        self._instrumentationString = '\n\n LogBroker.Instance.TraceDebug(\'sto eseguendo \' + ' \
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
            fileContent = fileContent[match.end() + 1 : len(fileContent) - 1]

            value = match.group()
            toIgnore1 = re.compile('^[\t ]?(if|for|switch)')
            toIgnore2 = re.compile('[ ]new[ ]')

            if not toIgnore1.match(value) and not toIgnore2.match(value):

                self._instrumentedFileContent += self._instrumentationString

            match = methodStartPatternObj.search(fileContent)

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
