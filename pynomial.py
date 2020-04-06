class Pynomial:
    def __init__(self, var, *coefs, pname='p'):
        self.__var = var
        self.__coefs = []
        for coef in coefs:
            if len(self.__coefs) == 0 and coef == 0:
                continue
            self.__coefs.append(coef)
        self.__coefs.reverse()
        self.__pname = pname

    def __str__(self):
        result = self.__pname + ' ='
        c = self.__coefs
        c.reverse()
        for index, coef in enumerate(c):
            if coef == 1 and index == 0:
                coef = ' '
            elif coef == 1:
                coef = ' + '
            elif coef == -1:
                coef = ' - '
            elif coef > 0 and index != 0:
                coef = f' + {coef}'
            elif coef < 0:
                coef = f' - {abs(coef)}'
            elif index == 0:
                coef = f' {abs(coef)}'
            else:
                continue
            power = len(self.__coefs) - index -1
            if power == 0:
                result += coef
                continue
            elif power == 1:
                power = ''
            else:
                power = f'^{power}'
            result += f'{coef}{self.__var}{power}'
        return result