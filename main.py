import sys
import re

class Instrumenter:

    def __init__(self):

        self._methodStartPattern = r'\w+[ ]*(\<.*?\>)?[ ]+\w+[ ]*\(([\[\]a-zA-Z1-9_,.=<>\"\s ]+)?\)\s*\{'
        self._stopWatchStart = "\n\t\t\tvar stopWatch = new System.Diagnostics.Stopwatch(); \n\t\t\t stopWatch.Start();"
        self._elapsedTime = "\n\t\t\tSystem.String.Format(\"{0:00}:{1:00}:{2:00}.{3:00}\", stopWatch.Elapsed.Hours, stopWatch.Elapsed.Minutes, stopWatch.Elapsed.Seconds)"
        self._logTimeSpent = "\n\t\t\tComm.Log.LogBroker.Instance.TraceDebug(\"Runtime =>\" + " + self._elapsedTime + ");\n\t\t"
        self._instrumentedFileContent = ''

    def GetFuncExitPoints(self, methodStartToFileEnd):

        ret = []
        lastClsd = self.FindMethodClosingBrace(methodStartToFileEnd)

        retRx = re.compile('\sreturn(;|\s)')
        match = retRx.finditer(methodStartToFileEnd[:lastClsd])

        for x in retRx.finditer(methodStartToFileEnd[:lastClsd]):
                ret.append(x.span()[0])

        ret.append(lastClsd)

        return ret

    def FindMethodClosingBrace(self, methodStartToEOF):

        open = 1
        lastOpen = -1
        lastClsd = -1

        searchForOpen = True;

        while open > 0:

            foundOpen = methodStartToEOF.find('{', lastOpen + 1)
            foundClose = methodStartToEOF.find('}', lastClsd + 1)

            if foundOpen < 0:
                searchForOpen = False

            if searchForOpen:
                if foundOpen < foundClose:
                    open += 1
                    lastOpen = foundOpen
                else:
                    open -= 1
                    lastClsd = foundClose
            else:
                open -= 1
                lastClsd = foundClose

        return lastClsd

    def Instrument(self, pathToFile):

        file = open(pathToFile, 'r')
        fileContent = file.read()
        file.close()

        methodStartPattern = re.compile(self._methodStartPattern)
        match = methodStartPattern.search(fileContent, re.DOTALL)

        while match is not None:

            toIgnore = re.compile(r'(while|if|else if|for|switch|catch|using|ForEach|\s?new\s?)')

            # is the match the start of a method?
            if not toIgnore.match(match.group()):

                methodBodyStart = match.end()
                self._instrumentedFileContent += fileContent[0: methodBodyStart]

                self._instrumentedFileContent += self._stopWatchStart
                fileContent = fileContent[methodBodyStart : len(fileContent)]

                funcExitPoints = self.GetFuncExitPoints(fileContent)

                prev = 0

                for x in funcExitPoints:

                    self._instrumentedFileContent += fileContent[prev : x]
                    self._instrumentedFileContent += self._logTimeSpent
                    prev = x

                fileContent = fileContent[prev : len(fileContent)]
            else:
                self._instrumentedFileContent += fileContent[0: match.end()]
                fileContent = fileContent[match.end(): len(fileContent)]

            match = methodStartPattern.search(fileContent)

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
