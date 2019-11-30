import numpy as np

class Simplex(object):
    vectorC = [5, 3, 6]
    vectorB = [7, 3, 3]
    vectorLimitation = [[1, 1, 1],
                        [1, 3, 0],
                        [0, 0.5, 2]]
    matrixSimplex = []

    columnStringSimplex = ["S0", "X1", "X2", "X3"]
    rowStringSimplex = ["X4", "X5", "X6", "F "]

    _resRow = 0
    _resColumn = 0
    _flagSolution = False

    def bruteForce(self):
        print("Метод полного перебора")
        arraySolution = []
        arrayGoSolution = []
        optResult = 0
        optArray = []
        for i in range(5):
            for j in range(5):
                for k in range(5):
                    tmpArray = []
                    tmpArray.append(i)
                    tmpArray.append(j)
                    tmpArray.append(k)
                    arraySolution.append(tmpArray)
        for index in range(int(len(arraySolution))):
            if((self.vectorB[0] >= self.vectorLimitation[0][0] * arraySolution[index][0] + self.vectorLimitation[0][1] * arraySolution[index][1] + self.vectorLimitation[0][2] * arraySolution[index][2])
            and (self.vectorB[1] >= self.vectorLimitation[1][0] * arraySolution[index][0] + self.vectorLimitation[1][1] * arraySolution[index][1] + self.vectorLimitation[1][2] * arraySolution[index][2])
            and (self.vectorB[2] >= self.vectorLimitation[2][0] * arraySolution[index][0] + self.vectorLimitation[2][1] * arraySolution[index][1] + self.vectorLimitation[2][2] * arraySolution[index][2])):
                arrayGoSolution.append(arraySolution[index])
                tmpResult = self.vectorC[0] * arraySolution[index][0] + self.vectorC[1] * arraySolution[index][1] + self.vectorC[2] * arraySolution[index][2]
                if(optResult <= tmpResult):
                    optResult = tmpResult
                    optArray = arraySolution[index]
        print(arrayGoSolution)
        print("X1 = ", optArray[0])
        print("X2 = ", optArray[1])
        print("X3 = ", optArray[2])
        print("F = ", optResult)
        print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        print("Метод ветвей и границ")

    def firstStep(self):
        print("Канонический вид")
        print("F=", "-(", self.vectorC[0], "* x1 +", self.vectorC[1], "* x2 +", self.vectorC[2], "* x3) -> min")
        for i in range(len(self.vectorB)):
            print(self.vectorLimitation[i][0], "* x1 +", self.vectorLimitation[i][1], "* x2 +", self.vectorLimitation[i][2], "* x3 +", "x",
                  (i + 4), "=", self.vectorB[i])

    def getSimplexMatrix(self):
        self.rowStringSimplex = []
        for i in range(int(len(self.vectorB))):
            x = 'X'
            x += str(i+4)
            self.rowStringSimplex.append(x)
        self.rowStringSimplex.append('F')
        self.matrixSimplex = [[0] * (int(len(self.vectorC)) + 1) for i in range(int(len(self.vectorB)) + 1)]
        for i in range(len(self.matrixSimplex)):
            for j in range(int(len(self.vectorC)) + 1):
                if (j != 0) and (i != int(len(self.vectorB))):
                    self.matrixSimplex[i][j] = self.vectorLimitation[i][j - 1]
                elif (j == 0) and (i != int(len(self.vectorB))):
                    self.matrixSimplex[i][j] = self.vectorB[i]
                elif (j > 0) and (i == int(len(self.vectorB))):
                    self.matrixSimplex[i][j] = self.vectorC[j - 1]

    def recountMatrix(self):
        self.vectorC = [5, 3, 6]
        self.vectorB = [7, 3, 3]
        self.vectorLimitation = [[1, 1, 1],
                                 [1, 3, 0],
                                 [0, 0.5, 2]]
        self.matrixSimplex = []

    def printSimplexMatrix(self):
        print("Симплекс таблица")
        print(' ', end='         ')
        for elem in self.columnStringSimplex:
            strFormat = str(elem)
            strFormat = strFormat.ljust(10)
            print(strFormat, end='')
        for i in range(int(len(self.vectorB)) + 1):
            print("\n")
            strFormat = str(self.rowStringSimplex[i])
            strFormat = strFormat.ljust(10)
            print(strFormat, end='')
            for j in range(int(len(self.vectorC)) + 1):
                strFormat = str(np.round(self.matrixSimplex[i][j], 2))
                strFormat = strFormat.ljust(10)
                print(strFormat, end='')
        print("")

    def getResolvingElement(self):
        for i in range(int(len(self.vectorB))):
            if (self._flagSolution == True):
                continue
            if (self.matrixSimplex[i][0] < 0):
                self._resRow = i
                for j in range(int(len(self.vectorC))+1):
                    if (self._flagSolution == True):
                        continue
                    if (self.matrixSimplex[i][j] < 0) and (j != 0):
                        self._resColumn = j
                        self._flagSolution = True
                min = 100000
                for j in range(int(len(self.matrixSimplex)) - 1):
                    if (self.matrixSimplex[j][self._resColumn] != 0):
                        tmp = self.matrixSimplex[j][0] / self.matrixSimplex[j][self._resColumn]
                        if (tmp > 0) and (tmp < min):
                            self._resRow = j
                            min = tmp
        if (self._flagSolution == True):
            print("Разрешающая строка", self.rowStringSimplex[self._resRow])
            print("Разрешающий столбец", self.columnStringSimplex[self._resColumn])

    def getOptimumResolvingElement(self):
        max = 0
        for i in range(int(len(self.vectorC)) + 1):
            if (i != 0) and (self.matrixSimplex[int(len(self.vectorB))][i] > 0) and (
                    self.matrixSimplex[int(len(self.vectorB))][i] > max):
                self._resColumn = i
                max = self.matrixSimplex[int(len(self.vectorB))][i]
                min = 100000
                for j in range(int(len(self.vectorB))):
                    if (self.matrixSimplex[j][self._resColumn] != 0):
                        tmp = self.matrixSimplex[j][0] / self.matrixSimplex[j][self._resColumn]
                        if (tmp > 0) and (tmp < min):
                            self._resRow = j
                            min = tmp
                            self._flagSolution = True

        if (self._flagSolution == True):
            print("Разрешающий столбец", self.columnStringSimplex[self._resColumn])
            print("Разрешающая строка", self.rowStringSimplex[self._resRow])

    def countSimplexMatrix(self):
        tmp = self.columnStringSimplex[self._resColumn]
        self.columnStringSimplex[self._resColumn] = self.rowStringSimplex[self._resRow]
        self.rowStringSimplex[self._resRow] = tmp
        _tmpMatrixSimplex = [[0] * (int(len(self.vectorC)) + 1) for i in range(int(len(self.vectorB)) + 1)]
        for i in range(int(len(self.vectorB)) + 1):
            for j in range(int(len(self.vectorC)) + 1):
                if (i == self._resRow) and (j == self._resColumn):
                    _tmpMatrixSimplex[i][j] = 1 / self.matrixSimplex[self._resRow][self._resColumn]
                elif (i == self._resRow) and (j != self._resColumn):
                    _tmpMatrixSimplex[i][j] = self.matrixSimplex[i][j] / self.matrixSimplex[self._resRow][
                        self._resColumn]
                elif (i != self._resRow) and (j == self._resColumn):
                    _tmpMatrixSimplex[i][j] = (-1) * self.matrixSimplex[i][j] / self.matrixSimplex[self._resRow][
                        self._resColumn]
                else:
                    _tmpMatrixSimplex[i][j] = self.matrixSimplex[i][j] - (
                                self.matrixSimplex[self._resRow][j] * self.matrixSimplex[i][self._resColumn]) / \
                                              self.matrixSimplex[self._resRow][self._resColumn]

        self.matrixSimplex = _tmpMatrixSimplex

    def checkSimplexMatrix(self):
        for i in range(int(len(self.vectorB))):
            if (self.matrixSimplex[i][0] < 0) and (i != int(len(self.vectorB))):
                return True
        return False

    def checkOptimumSimplexMatrix(self):
        for i in range(int(len(self.vectorC)) + 1):
            if (self.matrixSimplex[int(len(self.vectorB))][i] > 0) and (i != 0):
                return True
        return False

    def algorithm(self):
        print("Исходная симплекс таблица имеет вид:")
        self.printSimplexMatrix()
        print("Нахождение опорного решения:")
        while True:
            self._flagSolution = False
            self._flagCheck = self.checkSimplexMatrix()
            if (self._flagCheck == True):
                self.getResolvingElement()
                if (self._flagSolution == False):
                    break
                print("Производим замену:", self.columnStringSimplex[self._resColumn], "<->",
                      self.rowStringSimplex[self._resRow])
                self.countSimplexMatrix()

            else:
                print("Так как элементы S0 неотрицательны -> опорное решение")
                break
            self.printSimplexMatrix()
        if (self._flagSolution == False) and (self._flagCheck == True):
            print("Не имеет опорного решения")
        else:
            print("Нахождение оптимального решения:")
            while True:
                self._flagSolution = False
                self._flagCheck = self.checkOptimumSimplexMatrix()
                if (self._flagCheck == True):
                    self.getOptimumResolvingElement()
                    if (self._flagSolution == False):
                        break
                    print("Производим замену:", self.columnStringSimplex[self._resColumn], "<->",
                          self.rowStringSimplex[self._resRow])
                    self.countSimplexMatrix()
                else:
                    break
                self.printSimplexMatrix()
            if (self._flagSolution == False) and (self._flagCheck == True):
                print("Имеет опорное решение, не имеет оптимального решения")
                return 0
            print("Оптимальное решение:")
            for printIndex in range(int(len(self.columnStringSimplex))):
                if (printIndex != 0):
                    print(self.columnStringSimplex[printIndex], "= 0")
            for printIndex in range(int(len(self.rowStringSimplex))):
                print(self.rowStringSimplex[printIndex], "=", np.round(self.matrixSimplex[printIndex][0], 2))
            print('|||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
            for i in range(int(len(self.vectorB))):
                flagBranch = False
                if(flagBranch == True):
                    break
                if (self.rowStringSimplex[i] == 'X2') or (self.rowStringSimplex[i] == 'X3'):
                    tmpCheckValue = np.round(self.matrixSimplex[i][0] % 1, 1)
                    tmpCheckValue = tmpCheckValue % 1
                    if (tmpCheckValue != 0):
                        self.bottomBorder = np.round(self.matrixSimplex[i][0] - 0.5, 0)
                        self.topBorder = np.round(self.matrixSimplex[i][0] + 0.5, 0)
                        self.bottom = []
                        self.top = []
                        if(self.rowStringSimplex[i] == 'X2'):
                            self.bottom = [0, 1, 0]
                            self.top = [0, -1, 0]
                        if (self.rowStringSimplex[i] == 'X3'):
                            self.bottom = [0, 0, 1]
                            self.top = [0, 0, -1]

                if (i == int(len(self.vectorB)) - 1):
                    break

firstSimplex = Simplex()
firstSimplex.bruteForce()
firstSimplex.firstStep()
firstSimplex.getSimplexMatrix()
firstSimplex.algorithm()

bottomBorder = firstSimplex.bottomBorder
topBorder = firstSimplex.topBorder

secondSimplex = Simplex()
secondSimplex.vectorLimitation.append(firstSimplex.bottom)
secondSimplex.vectorB.append(firstSimplex.bottomBorder)
secondSimplex.columnStringSimplex = ['S0', 'X1', 'X2', 'X3']
secondSimplex.getSimplexMatrix()
secondSimplex.algorithm()

thirdSimplex = Simplex()
thirdSimplex.recountMatrix()
thirdSimplex.vectorLimitation.append(firstSimplex.top)
thirdSimplex.vectorB.append((-1)*firstSimplex.topBorder)
thirdSimplex.columnStringSimplex = ['S0', 'X1', 'X2', 'X3']
thirdSimplex.getSimplexMatrix()
thirdSimplex.algorithm()