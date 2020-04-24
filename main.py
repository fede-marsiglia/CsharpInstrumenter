import sys
import re


class Instrumenter:

    def __init__(self):

        self._methodStartPattern = r'\w+[ ]*(\<.*?\>)?[ ]+\w+[ ]*\(([\[\]a-zA-Z1-9_,.=<>\"\s ]+)?\)\s*\{'
        self._stopWatchStart = "\n\t\t\tvar stopWatch = new System.Diagnostics.Stopwatch(); \n\t\t\t stopWatch.Start();"
        self._stopWatchStop = "\n\t\t\tstopWatch.Stop(); \n\t\t\tvar ts = stopWatch.Elapsed;"
        self._elapsedTime = "\n\t\t\tvar elapsedTime = System.String.Format(\"{0:00}:{1:00}:{2:00}.{3:00}\", ts.Hours, ts.Minutes, ts.Seconds, ts.Milliseconds / 10);"
        self._logTimeSpent = "\n\t\t\tComm.Log.LogBroker.Instance.TraceDebug(\"Runtime =>\" + elapsedTime);\n\t\t"
        self._instrumentedFileContent = ''

    def GetFuncEnd(self, fileContent):

        ret = [-1]
        open = 1

        lastOpen = 0
        lastClsd = 0

        while open > 0:

            foundOpen = fileContent.find('{', lastOpen + 1)
            foundClose = fileContent.find('}', lastClsd + 1)

            if foundClose >= 0 and foundOpen >= 0:

                if foundOpen < foundClose:
                    open += 1
                    lastOpen = foundOpen
                else:
                    open -= 1
                    lastClsd = foundClose
            else:
                break

        ret = lastClsd

        retRx = re.compile('\sreturn(;|\s)')
        match = retRx.finditer(fileContent[:ret])

        if match is not None:

            ret = []
            for m in match:
                ret.append(m.span()[0])

        return ret

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

                startToFuncStart = fileContent[0: methodBodyStart]
                funcStartToEOF = fileContent[methodBodyStart : len(fileContent)]

                self._instrumentedFileContent += startToFuncStart
                self._instrumentedFileContent += self._stopWatchStart

                funcExitPoints = self.GetFuncEnd(funcStartToEOF)
                prev = methodBodyStart

                for x in funcExitPoints:

                    x += methodBodyStart
                    self._instrumentedFileContent += fileContent[prev : x]
                    self._instrumentedFileContent += self._stopWatchStop
                    self._instrumentedFileContent += self._elapsedTime
                    self._instrumentedFileContent += self._logTimeSpent
                    prev = x

                fileContent = fileContent[x : len(fileContent)]
            else:
                fileContent = fileContent[match.end(): len(fileContent)]

            match = methodStartPattern.search(fileContent)

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
