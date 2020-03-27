import numpy as np
import math

class Element():

    def __init__(self, Xpoczatkowe, Xkoncowe, Ypoczatkowe, Ykoncowe, ModulYounga, PoleP, WezelP, WezelK ):
        self.Xpoczatkowe=Xpoczatkowe
        self.Xkoncowe=Xkoncowe
        self.Ypoczatkowe=Ypoczatkowe
        self.Ykoncowe=Ykoncowe
        self.ModulYounga=ModulYounga
        self.PoleP=PoleP
        self.WezelP=WezelP
        self.WezelK=WezelK
        self.Wezly=np.array([[WezelP,WezelK]])

        self.l=self.dlugosc(self.Xpoczatkowe, self.Xkoncowe,self.Ypoczatkowe,self.Ykoncowe)
        self.cos = self.cosinus(self.Xpoczatkowe, self.Xkoncowe,self.l)
        self.sin = self.sinus(self.Ypoczatkowe,self.Ykoncowe,self.l)
        self.Trans= self.Transormacja(self.cos, self.sin)
        self.Sztywnosc = self.sztywnosc(self.ModulYounga, self.PoleP, self.l, self.cos, self.sin)

    def cosinus(self, Xpoczatkowe, Xkoncowe, dlugosc):
        cos=((Xkoncowe-Xpoczatkowe)/dlugosc)
        return cos


    def sinus(self,Ypoczatkowe, Ykoncowe, dlugosc):
        sin=((Ykoncowe-Ypoczatkowe)/dlugosc)
        return sin


    def dlugosc(self,Xpoczatkowe, Xkoncowe, Ypoczatkowe, Ykoncowe):
        l= math.sqrt(((Ykoncowe-Ypoczatkowe)**2)+((Xkoncowe-Xpoczatkowe)**2))
        return l


    def Transormacja(self,cosinus, sinus):
        T=np.array([[cosinus, sinus, 0, 0], [0, 0, cosinus, sinus]])
        return T

    def sztywnosc(self,ModulYounga, PolePrzekroju, DlugoscElementu, Cosinus, Sinus):
        # tworzy macierz sztywności elementu w układzie lokalnym
        k = np.array(([Cosinus * Cosinus, Cosinus * Sinus, -Cosinus * Cosinus, -Cosinus * Sinus],
                      [Cosinus * Sinus, Sinus * Sinus, -Cosinus * Sinus, -Sinus * Sinus],
                      [-Cosinus * Cosinus, -Cosinus * Sinus, Cosinus * Cosinus, Cosinus * Sinus],
                      [-Cosinus * Sinus, -Sinus * Sinus, Cosinus * Sinus, Sinus * Sinus]))
        wynik = ((ModulYounga * PolePrzekroju) / DlugoscElementu) * k
        return wynik

    def Sztywnosc2(self, Top):
        k= Top.T@Top
        return k



    def Bool(self,Top, liczba_elementow):
        B = np.zeros([4, liczba_elementow])
        for i in range(0, 2):
            B[i, (((2 * (Top[0, 0])) - 2) + i)] = 1
            B[i + 2, (((2 * (Top[0, 1])) - 2) + i)] = 1
        return B



