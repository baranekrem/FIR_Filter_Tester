from numpy import sin, pi
from enum import Enum

class FilterType(Enum):
    LowPass = 0
    HighPass = 1
    BandPass = 2
    BandStop = 3

class Filter(object):
    def __init__(self, type=FilterType.LowPass, sampleCount=20000, order=10, *args):
        self.__type = FilterType(type)
        self.__fs = sampleCount
        self.__order = order

        if len(args) == 0:
            a = 1 # error or default state
        elif len(args) == 1:
            self.__fc = args[0]
        elif len(args) == 2:
            self.__fcl = args[0]
            self.__fch = args[1]

    def GetOrder(self):
        return (self.__order)

    def SetOrder(self, order):
        self.__order = order

    def GetSampleCount(self):
        return (self.__fs)

    def SetSampleCount(self, sampleCount):
        self.__fs = sampleCount

    def GetType(self):
        return (self.__type)

    def SetType(self, type):
        self.__type = FilterType(type)

    def SetLowFrequency(self, fcl):
        self.__fcl = fcl

    def GetLowFrequency(self):
        return (self.__fcl)

    def SetHighFrequency(self, fch):
        self.__fch = fch

    def GetHighFrequency(self):
        return (self.__fch)

    def SetFrequency(self, fc):
        self.__fc = fc

    def GetFrequency(self):
        return (self.__fc)

    def GetCoefficients(self):
        self.__N = int(self.__order + 1)
        self.__M = int(self.__N / 2)
        self.__coeffs = [0] * self.__N

        if self.__type == FilterType.LowPass or self.__type == FilterType.HighPass:
            self.__wc = 2 * pi * self.__fc / self.__fs
        else:
            self.__wcl = 2 * pi * self.__fcl / self.__fs
            self.__wch = 2 * pi * self.__fch / self.__fs

        if self.__type == FilterType.LowPass:
            for n in range(self.__N):
                if (n == self.__M):
                    self.__coeffs[n] = self.__wc / pi
                else:
                    self.__coeffs[n] = sin(self.__wc * (n - self.__M)) / (pi * (n - self.__M))
                    self.__coeffs[n] = round(self.__coeffs[n], 6)

        if self.__type == FilterType.HighPass:
            for n in range(self.__N):
                if (n == self.__M):
                    self.__coeffs[n] = 1.0 - (self.__wc / pi)
                else:
                    self.__coeffs[n] = -sin(self.__wc * (n - self.__M)) / (pi * (n - self.__M))
                    self.__coeffs[n] = round(self.__coeffs[n], 6)

        if self.__type == FilterType.BandPass:
            for n in range(self.__N):
                if (n == self.__M):
                    self.__coeffs[n] = float((self.__wch - self.__wcl) / pi)
                else:
                    k = (n - self.__M)
                    self.__coeffs[n] = (sin(self.__wch * k) / (pi * k)) - (sin(self.__wcl * k) / (pi * k))
                    self.__coeffs[n] = round(self.__coeffs[n], 6)

        if self.__type == FilterType.BandStop:
            for n in range(self.__N):
                if (n == self.__M):
                    self.__coeffs[n] = float(1.0 - ((self.__wch - self.__wcl) / pi))
                else:
                    k = (n - self.__M)
                    self.__coeffs[n] = (sin(self.__wcl * k) / (pi * k)) - (sin(self.__wch * k) / (pi * k))
                    self.__coeffs[n] = round(self.__coeffs[n], 6)

        return (self.__coeffs)

    def FilterApply(self, x):
        self.GetCoefficients()

        y = [0] * self.__fs
        for i in range(int(self.__N), int(self.__fs)):
            for j in range(int(self.__N)):
                y[i] += self.__coeffs[j] * x[i-j]

        return (y)


