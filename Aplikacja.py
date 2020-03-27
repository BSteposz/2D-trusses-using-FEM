from tkinter import *
import Modul_Klasa
import numpy as np
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure




class App(Frame):
    def __init__(self, master):
        super(App, self).__init__(master)
        self.grid()
        self.liczba_elementow = 0
        self.liczba_wezlow = []
        self.podpory = None
        self.sily = None
        self.KK = None
        self.Przemieszczenia = None
        self.Reakcje = None
        self.SilyW = []
        self.Naprezenia=[]
        self.Sztywnosc_Globalna = None
        self.Wezly = {}

        self.WsporzedneP = []
        self.WsporzedneK = []
        self.dodawanie()
        self.elementy = []
        self.moge=False
        self.podporypodglad = {}
        self.silyX={}
        self.silyY={}

        np.set_printoptions(precision=3)

    def dodawanie(self):

        ##########################################################
        Label(self, text="Moduł Younga [Pa]"
              ).grid(row=4, column=0, sticky=W)
        self.Modul = Entry(self, width=10, )
        self.Modul.grid(row=4, column=1, sticky=W)

        Label(self, text="Pole przekroju [m^2]"
              ).grid(row=5, column=0, sticky=W)
        self.Pole = Entry(self, width=5)
        self.Pole.grid(row=5, column=1, sticky=W)
        ############################################################
        Label(self, text="Węzłeł początkowy i końcowy"
              ).grid(row=6, column=0, columnspan=2, sticky=W)
        self.Wezel1 = Entry(self, width=5)
        self.Wezel1.grid(row=6, column=1, sticky=W)
        self.Wezel1.insert(0, "1")

        self.Wezel2 = Entry(self, width=5)
        self.Wezel2.grid(row=6, column=2, sticky=W)
        self.Wezel2.insert(0, "2")
        ###########################################################
        Label(self, text="Początek (x, y)"
              ).grid(row=7, column=0, sticky=W)

        self.poczatekX = Entry(self, width=5)
        self.poczatekX.grid(row=7, column=1, sticky=W)
        self.poczatekX.insert(0, "0")

        self.poczatekY = Entry(self, width=5)
        self.poczatekY.grid(row=7, column=2, sticky=W)
        self.poczatekY.insert(0, "0")
        ############################################################
        Label(self, text="Koniec (x, y)"
              ).grid(row=8, column=0, sticky=W)

        self.koniecX = Entry(self, width=5)
        self.koniecX.grid(row=8, column=1, sticky=W)
        self.koniecX.insert(0, "0")

        self.koniecY = Entry(self, width=5)
        self.koniecY.grid(row=8, column=2, sticky=W)
        self.koniecY.insert(0, "0")
        ################################################################

        # tablica z dodanymi elementami

        self.naglowki = ["Element", "Początek\n(x, y)", "Koniec\n (x, y)", "Węzły", "Długość\n[m]", "Moduł\nYounga",
                         "Pole\nprzekroju"]
        self.tree = ttk.Treeview(self, columns=self.naglowki, show="headings", height=3)
        for i in self.naglowki:
            self.tree.heading(i, text=i.title())
            self.tree.column(i, minwidth=0, width=65, stretch=TRUE)
        self.tree.grid(column=0, columnspan=6, row=0, rowspan=4, pady=10, padx=5, sticky=(N, S, E, W))

        self.tree_scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.config(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.grid(row=0, rowspan=4, column=6, sticky=N + S)

        Button(self,
               text="Dodaj element",
               command=self.dodanie_elementu
               ).grid(row=9, column=0, pady=5, padx=5, sticky=W)

        Button(self,
               text="Agregacja elementów",
               command=self.Agregacja
               ).grid(row=10, column=0, pady=5, padx=5, sticky=W)

        ################################################################################
        Label(self, text="Dodaj siłe i podporę w węźle"
              ).grid(row=11, column=0, pady=5, sticky=W)

        self.WezelPF = Entry(self, width=5)
        self.WezelPF.grid(row=11, column=1, pady=5, sticky=W)
        self.WezelPF.insert(0, "1")

        Label(self, text="Wprowadź Siłę [N]"
              ).grid(row=12, column=2, pady=5, sticky=W)

        Label(self, text="Siła oś X"
              ).grid(row=13, column=2, sticky=W)
        self.SilaX = Entry(self, width=5)
        self.SilaX.grid(row=13, column=2, padx=70, sticky=W)
        self.SilaX.insert(0, "0")

        Label(self, text="Siła oś Y"
              ).grid(row=14, column=2, sticky=W)
        self.SilaY = Entry(self, width=5)
        self.SilaY.grid(row=14, column=2, padx=70, sticky=W)
        self.SilaY.insert(0, "0")

        Label(self, text="Wybierz podporę:"
              ).grid(row=12, column=0, sticky=W)

        self.PodporaWybor = IntVar(self, 1)
        self.Podpora = {
            "[1]Brak": 1,
            "[2]Podpora nieprzesuwna \n zablokowany X i Y (▲)": 2,
            "[3]Podpora przegubowa \n zablokowany Y (△)": 3,
            "[4]Podpora przegubowa \n zablokowany X (△)": 4,
        }

        for (text, value) in self.Podpora.items():
            Radiobutton(self, text=text, variable=self.PodporaWybor,
                        value=value).grid(row=12 + int(value), column=0, sticky=W)

        Button(self,
               text="Dodaj siłę  i podpore",
               command=self.DodajPF
               ).grid(row=15, column=2, sticky=W)

        Button(self,
               text="Generuj wyniki",
               command=self.Generuj
               ).grid(row=20, column=0, sticky=W)

        Button(self,
               text="Wykres przemieszczeń",
               command=self.Wykres1
               ).grid(row=23, column=7, sticky=W)
        Button(self,
               text="Wykres sił",
               command=self.Wykres2
               ).grid(row=23, column=8, sticky=W)

        Button(self,
               text="Wykres Naprężenia",
               command=self.Wykres3
               ).grid(row=23, column=9, sticky=W)


        Button(self,
               text="Zapisz",
               command=self.zapisz_plik
               ).grid(row=22, column=7, sticky=W)

        Button(self,
               text="Usuń ostatni",
               command=self.Usun
               ).grid(row=9, column=3, sticky=W)

        self.podglad = Canvas(self, width=350, height=300, bg="white")
        self.podglad.grid(row=0, rowspan=10, column=7, columnspan=5, padx=15, sticky=W)
        self.podglad.create_line(5, 0, 5, 295, fill="black", width=3, arrow=FIRST)
        self.podglad.create_text(15, 10, fill="black", text="y")
        self.podglad.create_text(345, 285, fill="black", text="x")
        self.podglad.create_line(5, 295, 345, 295, fill="black", width=3, arrow=LAST)

        self.Komunikat = Text(self, width=50, height=20)
        self.Komunikat.grid(row=11, rowspan=11, column=7, columnspan=5, sticky=N + E + W + S)

        self.text_scroll = Scrollbar(self, command=self.Komunikat.yview, orient=VERTICAL)
        self.text_scroll.config(command=self.Komunikat.yview)
        self.text_scroll.grid(row=11, rowspan=10, column=12, sticky=N + S)
        self.Komunikat.configure(yscrollcommand=self.text_scroll.set)

    def Wykres1(self):

        u={}
        for i in range(len(self.liczba_wezlow)):
            u[i+1]=[self.Przemieszczenia[((i)*2)], self.Przemieszczenia[((i)*2)+1]]


        #węzły bez przemieszczeń
        wx = []
        wy = []
        for i in range(self.liczba_elementow):
            wx.append(self.WsporzedneP[i][0]) #początek
            wx.append(self.WsporzedneK[i][0]) #koniec
            wy.append(self.WsporzedneP[i][1])
            wy.append(self.WsporzedneK[i][1])

        wx1 = []
        wy1 = []
        Nw=[]


        for i in range(len(wx)):
            for n in range(len(self.Wezly)):
                if wx[i] == self.Wezly[n + 1][0] and wy[i] == self.Wezly[n + 1][1]:
                    wx1.extend(wx[i]+(75*(u[n+1][0])))
                    wy1.extend(wy[i]+(75*(u[n+1][1])))

        t = Toplevel(self)
        t.wm_title("Wykres przemieszczeń")
        f = Figure(figsize=(8, 7), dpi=100)
        a = f.add_subplot(111)
        a.set_title("Wykres przemieszczeń")
        a.set_ylabel("Długość [m]")
        a.set_xlabel("Długość [m]")
        w1=a.plot(wx, wy, marker=".", label="Oryginalny")
        for x in range(len(self.Wezly)):
            a.annotate(x+1, (self.Wezly[x+1][0],self.Wezly[x+1][1]))
        w2=a.plot(wx1, wy1, marker=".", label="Przemieszczony")
        a.set_title("Wykres przemieszczeń")
        a.legend(bbox_to_anchor=(1.05, 1), loc='best', borderaxespad=0.)


        canvas = FigureCanvasTkAgg(f, t)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, t)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

    def Wykres2(self):

        Kolumny=[]
        Wartosci=[]
        for i in range(self.liczba_elementow):
            Kolumny.append(str(i+1))
            Wartosci.append(self.SilyW[i])



        t = Toplevel(self)
        t.wm_title("Wykres sił")
        f = Figure(figsize=(7, 6), dpi=100)
        a = f.add_subplot(111)
        a.set_title("Wykres sił")
        a.set_ylabel("Siła [N]")
        a.set_xlabel("Numer elementu")

        a.bar(Kolumny,Wartosci, 0.8)
        a.plot(legend= True)
        a.axhline(y=0)

        #Kolumny.plot(kind='bar', legend=True, ax=a)
        #Kolumny.set_title("Plot")

        canvas = FigureCanvasTkAgg(f, t)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, t)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

    def Wykres3(self):

        Kolumny=[]
        Wartosci=[]
        for i in range(self.liczba_elementow):
            Kolumny.append(str(i+1))
            Wartosci.append(self.Naprezenia[i])


        t = Toplevel(self)
        t.wm_title("Wykres naprężeń")
        f = Figure(figsize=(7, 6), dpi=100)
        a = f.add_subplot(111)
        a.set_ylabel("Naprężenie [Pa]")
        a.set_xlabel("Numer elementu")
        a.set_title("Wykres naprężeń")
        a.bar(Kolumny, Wartosci, 0.8)
        a.plot(legend=True)
        a.axhline(y=0)
        #wy=np.arange(len(self.elementy))
       #wx=self.Naprezenia
       #a.plot( wy, wx,  marker=".")
        #a.set_title("Wykres Naprężeń")

        canvas = FigureCanvasTkAgg(f, t)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, t)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)


    def zapisz_plik(self):
        Nazwa_pliku = filedialog.asksaveasfilename(defaultextension='.txt',
                                                   filetypes=(('Plik tekstowy', '*.txt'), ('All files', '*.*')))
        if Nazwa_pliku == None:
            return
        file = open(Nazwa_pliku, mode='w')
        file.write(self.Komunikat.get("1.0", "end"))
        file.close()
        messagebox.showinfo('Gotowe', 'Plik zapisany')

    def Usun(self):
        self.elementy.pop()
        self.WsporzedneP.pop()
        self.WsporzedneK.pop()
        if self.liczba_elementow < 10:
            self.tree.delete("I"+"0"+"0"+str(self.liczba_elementow))
            messagebox.showinfo(title="Wykonano", message="Pomyślnie usunięto element")
        else:
            messagebox.showinfo(title="Wykonano", message="Pomyślnie usunięto element")
        self.liczba_elementow-=1
        self.Wezly={}
        self.liczba_wezlow=[]
        for i in range(len(self.elementy)):
            if self.elementy[i].WezelP not in self.Wezly:
                self.Wezly[self.elementy[i].WezelP] = [self.elementy[i].Xpoczatkowe, self.elementy[i].Ypoczatkowe]
                self.liczba_wezlow.append(self.elementy[i].WezelP)
            if self.elementy[i].WezelK not in self.Wezly:
                self.Wezly[self.elementy[i].WezelK] = [self.elementy[i].Xkoncowe, self.elementy[i].Ykoncowe]
                self.liczba_wezlow.append(self.elementy[i].WezelK)



        self.rysuj()

        print("liczba elementów: ", len(self.elementy), "\n Wspołrzędne ",self.WsporzedneP, self.WsporzedneK, "\nLiczba elementów", self.liczba_elementow, "\n Węzły:", self.Wezly,"\nLiczba węzłów ", self.liczba_wezlow)


    def dodanie_elementu(self):
        try:

            # Utworzenie obiektu Element
            self.elementy.append(
                Modul_Klasa.Element(float(self.poczatekX.get()), float(self.koniecX.get()), float(self.poczatekY.get()),
                                    float(self.koniecY.get()), float(self.Modul.get()), float(self.Pole.get()),
                                    int(self.Wezel1.get()), int(self.Wezel2.get())))
            self.tree.insert("", "end", values=(
            "Element " + str(self.liczba_elementow + 1), [self.poczatekX.get(), self.poczatekY.get()],
            [self.koniecX.get(), self.koniecY.get()], self.elementy[self.liczba_elementow].Wezly,
            self.elementy[self.liczba_elementow].l, self.Modul.get(), self.Pole.get()))

            self.WsporzedneP.append([float(self.poczatekX.get()), float(self.poczatekY.get())])
            self.WsporzedneK.append([float(self.koniecX.get()), float(self.koniecY.get())])

            if int(self.Wezel1.get()) not in self.Wezly:
                self.Wezly[int(self.Wezel1.get())] = [float(self.poczatekX.get()), float(self.poczatekY.get())]
            if int(self.Wezel2.get()) not in self.Wezly:
                self.Wezly[int(self.Wezel2.get())] = [float(self.koniecX.get()), float(self.koniecY.get())]

            # Zwiększanie liczby unikalnych węzłów
            if int(self.Wezel1.get()) not in self.liczba_wezlow:
                self.liczba_wezlow.append(int(self.Wezel1.get()))
            if int(self.Wezel2.get()) not in self.liczba_wezlow:
                self.liczba_wezlow.append(int(self.Wezel2.get()))

            self.liczba_elementow += 1

            self.rysuj()

            # Wyczyszczenie pól wpisywania
            self.poczatekX.delete(0, "end")
            self.poczatekX.insert(0, self.koniecX.get())
            self.koniecX.delete(0, "end")
            self.koniecX.insert(0, "0")
            self.poczatekY.delete(0, "end")
            self.poczatekY.insert(0, self.koniecY.get())
            self.koniecY.delete(0, "end")
            self.koniecY.insert(0, "0")

            self.Wezel1.delete(0, "end")
            self.Wezel1.insert(0, self.Wezel2.get())
            self.Wezel2.delete(0, "end")
            self.Wezel2.insert(0, str(int(self.Wezel1.get()) + 1))

            self.Komunikat.delete("0.0", END)
            for i in range(0, len(self.elementy)):
                self.Komunikat.insert(END, "Utworzono macierz sztywności  elementu " + str(i + 1) + "\n\n" + str(
                    self.elementy[i].Sztywnosc) + "\n\n")

            print("liczba elementów: ", len(self.elementy), "\n Wspołrzędne ", self.WsporzedneP, self.WsporzedneK,
                  "\nLiczba elementów", self.liczba_elementow, "\n Węzły:", self.Wezly, "\nLiczba węzłów ",
                  self.liczba_wezlow)


        except ValueError:
            messagebox.showwarning(title="Brak wartości", message="Proszę uzupełnić wszystkie pola")
        except ZeroDivisionError:
            messagebox.showerror(title="Brak współrzędnych", message="Proszę wpisać współrzędne początki i końca")

    def Agregacja(self):

        print("liczba elementów: ", len(self.elementy), "\n Wspołrzędne ",self.WsporzedneP, self.WsporzedneK, "\nLiczba elementów", self.liczba_elementow, "\n Węzły:", self.Wezly,"\nLiczba węzłów ", self.liczba_wezlow)


        self.Sztywnosc_Globalna = np.zeros([(2 * len(self.liczba_wezlow)), (2 * len(self.liczba_wezlow))])

        for i in range((self.liczba_elementow)):
            self.Sztywnosc_Globalna = self.Sztywnosc_Globalna + ((
                        self.elementy[i].Bool(self.elementy[i].Wezly, (2 * len(self.liczba_wezlow))).T @ self.elementy[
                    i].Sztywnosc @ (self.elementy[i].Bool(self.elementy[i].Wezly, (2 * len(self.liczba_wezlow))))))
        a = np.copy(self.Sztywnosc_Globalna)
        with np.nditer(a, op_flags=['readwrite']) as it:
            for x in it:
                if x != 0:
                    x[...] = 1
                else:
                    x[...] = 0

        a = a.astype(int)

        self.Komunikat.insert(END, "Utworzono globalną macierz sztywności" + "\n\n" + str(a) + "\n\n")
        self.Komunikat.insert(END,
                              "Utworzono globalną macierz sztywności" + "\n\n" + str(self.Sztywnosc_Globalna) + "\n\n")
        self.podpory = np.zeros([2 * len(self.liczba_wezlow), 1])
        self.sily = np.zeros([2 * len(self.liczba_wezlow), 1])
        self.moge=True

        print(self.Wezly)

    def DodajPF(self):

        try:

            self.sily[int(self.WezelPF.get()) - 1 + int(self.WezelPF.get()) - 1] = float(self.SilaX.get())
            self.sily[int(self.WezelPF.get()) - 1 + int(self.WezelPF.get()) - 1 + 1] = float(self.SilaY.get())

            self.silyX[int(self.WezelPF.get())]=float(self.SilaX.get())
            self.silyY[int(self.WezelPF.get())]=float(self.SilaY.get())

            if self.PodporaWybor.get() == 1:
                self.podpory[int(self.WezelPF.get()) - 1 + int(self.WezelPF.get()) - 1] = 0
                self.podpory[int(self.WezelPF.get()) - 1 + int(self.WezelPF.get()) - 1 + 1] = 0
                self.podporypodglad[int(self.WezelPF.get())]=0



            elif self.PodporaWybor.get() == 2:
                self.podpory[int(self.WezelPF.get()) - 1 + int(self.WezelPF.get()) - 1] = 1
                self.podpory[int(self.WezelPF.get()) - 1 + int(self.WezelPF.get()) - 1 + 1] = 1
                self.podporypodglad[int(self.WezelPF.get())]=1


            elif self.PodporaWybor.get() == 4:
                self.podpory[int(self.WezelPF.get()) - 1 + int(self.WezelPF.get()) - 1] = 1
                self.podpory[int(self.WezelPF.get()) - 1 + int(self.WezelPF.get()) - 1 + 1] = 0
                self.podporypodglad[int(self.WezelPF.get())]=2


            else:
                self.podpory[int(self.WezelPF.get()) - 1 + int(self.WezelPF.get()) - 1] = 0
                self.podpory[int(self.WezelPF.get()) - 1 + int(self.WezelPF.get()) - 1 + 1] = 1
                self.podporypodglad[int(self.WezelPF.get())]=3


            self.rysuj()
            self.Komunikat.insert(END, "Do węzła " + str( self.WezelPF.get()) + " dodano siły o wartości\nX: " + str(float(self.SilaX.get())) + "\nY: " + str(float(self.SilaY.get())) + "\nPodpora nr.: " + str(self.PodporaWybor.get()) + "\n\n\n")

            self.SilaX.delete(0, "end")
            self.SilaX.insert(0, "0")
            self.SilaY.delete(0, "end")
            self.SilaY.insert(0, "0")
            self.PodporaWybor.set(1)
            self.WezelPF.insert(0, str(int(self.WezelPF.get()) + 1))
            self.WezelPF.delete(1, "end")


        except TypeError:
            messagebox.showinfo(title="Brak macierzy globalnej",
                                message="Przed dodaniem sił i podpór należy przeprowadzić agregacje elementów")
        except IndexError:
            messagebox.showwarning(title="Nieistniejący węzeł", message="Wybrany węzeł nie istnieje")
        except ValueError:
            messagebox.showinfo(title="Błąd wartości",
                                message="Podana wartość siły musi być liczbą")

    def Generuj(self):
        I = np.eye(2 * (len(self.liczba_wezlow)))
        Id = np.zeros([2 * (len(self.liczba_wezlow)), 2 * (len(self.liczba_wezlow))])
        for i in range(0, 2 * (len(self.liczba_wezlow))):
            Id[i, i] = self.podpory[i]

        Ip = np.subtract(I, Id)

        self.KK = Ip @ self.Sztywnosc_Globalna @ Ip + Id
        self.Przemieszczenia = np.linalg.inv(self.KK) @ self.sily
        self.Reakcje = self.Sztywnosc_Globalna @ self.Przemieszczenia - self.sily
        np.set_printoptions(precision=3)
        self.Komunikat.insert(END, "Wektor przemieszczeń węzłowych [m]\n" + str(self.Przemieszczenia) + "\n")
        self.Komunikat.insert(END, "\nWektor reakcji podporowych [N]\n" + str(self.Reakcje) + "\n")
        for i in range(len(self.elementy)):
            a = self.elementy[i].Trans @ (self.elementy[i].Sztywnosc @ self.elementy[i].Bool(self.elementy[i].Wezly, (
                        2 * len(self.liczba_wezlow))) @ self.Przemieszczenia)
            self.SilyW.extend(a[1])
            self.Komunikat.insert(END, "\nSiła przywęzłowa elementu " + str(i + 1)  + "\n" + str(a[1]) + " [N]"+ "\n")

        u={}
        for i in range(len(self.liczba_wezlow)):
            u[i+1]=[self.Przemieszczenia[((i)*2)], self.Przemieszczenia[((i)*2)+1]]

            print("Przemieszczenia [m]", self.Przemieszczenia)



        for i in range(len(self.elementy)):
            wynik = self.SilyW[i]/self.elementy[1].PoleP
            self.Naprezenia.append(wynik)
            self.Komunikat.insert(END, "\nNaprężenia elementu " + str(i + 1) + "\n" + str(wynik) + " [Pa]"  + "\n")




    def rysuj(self):
        self.podglad.delete("all")
        for i in range(self.liczba_elementow):
            self.podglad.create_line(20 + 25 * (self.WsporzedneP[i][0]), (150 - 20 * (self.WsporzedneP[i][1])),
                                     20 + 25 * (self.WsporzedneK[i][0]), (150 - 20 * (self.WsporzedneK[i][1])),
                                     fill="darkblue", width=3)
            self.podglad.create_line(5, 0, 5, 295, fill="black", width=3, arrow=FIRST)
            self.podglad.create_text(15, 10, fill="black", text="y")
            self.podglad.create_text(345, 285, fill="black", text="x")
            self.podglad.create_line(5, 295, 345, 295, fill="black", width=3, arrow=LAST)

            if (self.WsporzedneP[i][1]) == 0 and (self.WsporzedneK[i][1]) == 0:
                self.podglad.create_text(20 + ((self.WsporzedneP[i][0]) + (self.WsporzedneK[i][0]) * 12.5), 160 - 20 * (
                        (self.WsporzedneK[i][1]) - (self.WsporzedneK[i][1]) + (self.WsporzedneP[i][1]) * 7.5),
                                         fill="black", font="Times 10 italic bold", text=i + 1)
            elif (self.WsporzedneP[i][1]) != 0 or (self.WsporzedneK[i][1]) > 0:
                self.podglad.create_text(32 + ((self.WsporzedneP[i][0] + self.WsporzedneK[i][0]) * 12.5),
                                         140 - ((self.WsporzedneK[i][1] + self.WsporzedneP[i][1]) * 8.5),
                                         fill="black", font="Times 10 italic bold", text=i + 1)
            elif (self.WsporzedneP[i][1]) != 0 or (self.WsporzedneK[i][1]) < 0:
                self.podglad.create_text(25 + ((self.WsporzedneP[i][0] + self.WsporzedneK[i][0]) * 10.5),
                                         163 - ((self.WsporzedneK[i][1] - self.WsporzedneP[i][1]) * 10.5),
                                         fill="black", font="Times 10 italic bold", text=i + 1)

            continue

        for i in self.Wezly:
            self.podglad.create_text((20 + 25 * self.Wezly[i][0]), (160 - 25 * self.Wezly[i][1]), fill="green",
                                     font="Times 10 italic bold", text=str(i))

        if self.moge==True:
            for i in self.podporypodglad:
                if self.podporypodglad[i] == 1:
                    self.podglad.create_text((20 + 25 * self.Wezly[i][0]),
                                             (158 - 25 * self.Wezly[i][1]), fill="black",
                                             font="Times 13  bold", text="▲")
                elif self.podporypodglad[i] == 2:
                    self.podglad.create_text((20 + 25 * self.Wezly[i][0]),
                                             (158 - 25 * self.Wezly[i][1]), fill="black",
                                             font="Times 14  bold", text="△")
                elif self.podporypodglad[i] == 3:
                    self.podglad.create_text((20 + 25 * self.Wezly[i][0]),
                                             (158 - 25 * self.Wezly[i][1]), fill="black",
                                             font="Times 14  bold", text="△")
                else:
                    pass

            for i in self.silyX:
                if self.silyX[i] <0:
                    self.podglad.create_line(20 + 25 * self.Wezly[i][0], 150 - 25 * self.Wezly[i][1],60 + 25 * self.Wezly[i][0],150 - 25 * self.Wezly[i][1], fill="red", width=2, arrow=FIRST)
                if self.silyX[i] >0:
                    self.podglad.create_line(-20 + 25 * self.Wezly[i][0], 150 - 25 * self.Wezly[i][1],20 + 25 * self.Wezly[i][0],150 - 25 * self.Wezly[i][1],fill="red", width=2, arrow=LAST)

            for i in self.silyY:
                if self.silyY[i] <0:
                    self.podglad.create_line(20 + 25 * self.Wezly[i][0], 120 - 25 * self.Wezly[i][1],20 + 25 * self.Wezly[i][0],150 - 25 * self.Wezly[i][1], fill="red", width=2, arrow=LAST)
                if self.silyY[i] >0:
                    self.podglad.create_line(20 + 25 * self.Wezly[i][0], 120 - 25 * self.Wezly[i][1],20 + 25 * self.Wezly[i][0],150 - 25 * self.Wezly[i][1],fill="red", width=2, arrow=FIRST)



root = Tk()
root.title("Praca inżynierska")
root.geometry("1000x750")
app = App(root)
root.mainloop()
