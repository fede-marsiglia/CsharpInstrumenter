import sys
import re

class Instrumenter:

    def __init__(self):

        self._methodStartPattern = r'\w+[ ]*(\<.*?\>)?[ ]+\w+[ ]*\(([\[\]a-zA-Z1-9_,.=<>\"\s ]+)?\)\s*\{'
        self._instrumentationString = "\n\t\t\tComm.Log.LogBroker.Instance.TraceDebug(\"-INSTRUMENTER-\");\n"
        self._instrumentedFileContent = ''

    def GetFuncEnd(self, fileContent):

        open = 1

        lastOpen = 0
        lastClsd = 0

        while open > 0:

            foundOpen = fileContent.find('{', lastOpen + 1)
            foundClose = fileContent.find('}', lastClsd + 1)

            if foundClose != -1 and foundOpen != -1:

                if foundOpen < foundClose:
                    open += 1
                    lastOpen = foundOpen
                else:
                    open -= 1
                    lastClsd = foundClose

            elif foundClose != -1:

                lastClsd = foundClose
                break

        return lastClsd


    def Instrument(self, pathToFile):

        file = open(pathToFile, 'r')
        fileContent = file.read()
        file.close()

        methodStartPatternObj = re.compile(self._methodStartPattern)
        match = methodStartPatternObj.search(fileContent, re.DOTALL)

        while match is not None:

            toIgnore = re.compile(r'(while|if|else if|for|switch|catch|using|ForEach|\s?new\s?)')

            # is the match the start of a method?
            if not toIgnore.match(match.group()):

                startToFuncStart = fileContent[0 : match.end()]

                self._instrumentedFileContent += startToFuncStart
                self._instrumentedFileContent += self._instrumentationString

                funcEnd = self.GetFuncEnd(fileContent[match.end() : len(fileContent)]) + match.end()

                self._instrumentedFileContent += fileContent[match.end() : funcEnd]
                self._instrumentedFileContent += self._instrumentationString

                fileContent = fileContent[funcEnd : len(fileContent)]
            else:
                fileContent = fileContent[match.end(): len(fileContent)]

            match = methodStartPatternObj.search(fileContent)

        # get the rest of the original file and add
        # it's content to the instrumented one
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
