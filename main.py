import sys
import re

class Instrumenter:

    def __init__(self):

        self._methodStartPattern = r'\w+[ ]*(\<.*?\>)?[ ]+\w+[ ]*\(([\[\]a-zA-Z1-9_,.=<>\"\s ]+)?\)\s*\{'
        self._stopWatchStart = "\n\t\t\tvar stopWatch = new System.Diagnostics.Stopwatch(); \n\t\t\t stopWatch.Start();"
        self._stopWatchStop = "\n\t\t\tstopWatch.Stop(); \n\t\t\tvar ts = stopWatch.Elapsed;"
        self._elapsedTime = "\n\t\t\tvar elapsedTime = System.String.Format(\"{0:00}:{1:00}:{2:00}.{3:00}\", ts.Hours, ts.Minutes, ts.Seconds, ts.Milliseconds / 10);"
        self._logTimeSpent = "\n\t\t\tComm.Log.LogBroker.Instance.TraceDebug(\"Runtime =>\" + elapsedTime);\n"
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
                self._instrumentedFileContent += self._stopWatchStart

                funcEnd = self.GetFuncEnd(fileContent[match.end() : len(fileContent)]) + match.end()

                self._instrumentedFileContent += fileContent[match.end() : funcEnd]
                self._instrumentedFileContent += self._stopWatchStop
                self._instrumentedFileContent += self._elapsedTime
                self._instrumentedFileContent += self._logTimeSpent

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
