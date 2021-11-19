# A*

import math
from tkinter import *
from tkinter.ttk import *
import tkinter
import tkinter.ttk


# noinspection PyAttributeOutsideInit
class AutocompleteCombobox(tkinter.ttk.Combobox):

    def set_completion_list(self, completion_list):
        self.position = 0
        self._hit_index = 0
        self._hits = []
        self._completion_list = sorted(completion_list, key=str.lower)
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list

    def autocomplete(self, delta=0):
        if delta:
            self.delete(self.position, tkinter.END)
        else:
            self.position = len(self.get())
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):
                _hits.append(element)
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        if self._hits:
            self.delete(0, tkinter.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tkinter.END)

    def handle_keyrelease(self, event):
        if event.keysym == "BackSpace":
            self.delete(self.index(tkinter.INSERT), tkinter.END)
            self.position = self.index(tkinter.END)
        if event.keysym == "Left":
            if self.position < self.index(tkinter.END):
                self.delete(self.position, tkinter.END)
            else:
                self.position = self.position-1
                self.delete(self.position, tkinter.END)
        if event.keysym == "Right":
            self.position = self.index(tkinter.END)
        if len(event.keysym) == 1:
            self.autocomplete()


get_estacion_precision = 10  # "error" para seleccionar la estacion origen o destino
h_multiplier = 1000  # multiplicador para cuando hay transbordo
mapa = {'Aghia Paraskevi': [['3'], ['Halandri', 'Nomismatokopio'], 1000000, 1000000, (624, 443)],
        'Aghios Antonios': [['2'], ['Sepolia'], 1000000, 1000000, (143, 386)],
        'Aghios Dimitrias · Alexandros Panogulis': [['2'], ['Dafni'], 1000000, 1000000, (321, 852)],
        'Aghios Eleftherios': [['1'], ['Ano Patissia', 'Kato Patissia'], 1000000, 1000000, (299, 391)],
        'Aghios Ioannis': [['2'], ['Neos Kosmos', 'Dafni'], 1000000, 1000000, (321, 777)],
        'Aghios Nikolaos': [['1'], ['Attiki', 'Kato Patissia'], 1000000, 1000000, (245, 446)],
        'Airport': [['3'], ['Koropi'], 1000000, 1000000, (822, 635)],
        'Akropoli': [['2'], ['Syntagma', 'Sygrou - Fix'], 1000000, 1000000, (321, 664)],
        'Ambelokipi': [['3'], ['Panormou', 'Megaro Moussikis'], 1000000, 1000000, (491, 578)],
        'Ano Patissia': [['1'], ['Perissos', 'Aghios Eleftherios'], 1000000, 1000000, (325, 366)],
        'Attiki': [['1', '2'], ['Victoria', 'Aghios Nikolaos', 'Sepolia', 'Larissa Station'], 1000000, 1000000,
                   (224, 468)],
        'Dafni': [['2'], ['Aghios Ioannis', 'Aghios Dimitrias · Alexandros Panogulis'], 1000000, 1000000, (321, 815)],
        'Doukissis Plokentias': [['3'], ['Halandri', 'Pallini'], 1000000, 1000000, (683, 386)],
        'Egaleo': [['3'], ['Eleonas'], 1000000, 1000000, (67, 506)],
        'Eleonas': [['3'], ['Kerameikos', 'Egaleo'], 1000000, 1000000, (120, 561)],
        'Ethniki Amyna': [['3'], ['Holargos', 'Katehaki'], 1000000, 1000000, (556, 510)],
        'Evangelismos': [['3'], ['Megaro Moussikis', 'Syntagma'], 1000000, 1000000, (400, 614)],
        'Faliro': [['1'], ['Moschato', 'Piraeus'], 1000000, 1000000, (140, 807)],
        'Halandri': [['3'], ['Doukissis Plokentias', 'Aghia Paraskevi'], 1000000, 1000000, (646, 421)],
        'Holargos': [['3'], ['Ethniki Amyna', 'Nomismatokopio'], 1000000, 1000000, (579, 488)],
        'Iraklio': [['1'], ['Nea Ionia', 'Irini'], 1000000, 1000000, (420, 270)],
        'Irini': [['1'], ['Neratziotissa', 'Iraklio'], 1000000, 1000000, (511, 260)],
        'Kallithea': [['1'], ['Tavros', 'Moschato'], 1000000, 1000000, (200, 751)],
        'KAT': [['1'], ['Kifissia', 'Maroussi'], 1000000, 1000000, (636, 168)],
        'Katehaki': [['3'], ['Ethniki Amyna', 'Panormou'], 1000000, 1000000, (534, 532)],
        'Kato Patissia': [['1'], ['Aghios Nikolaos', 'Aghios Eleftherios'], 1000000, 1000000, (273, 418)],
        'Kerameikos': [['3'], ['Monastiraki', 'Eleonas'], 1000000, 1000000, (162, 602)],
        'Kifissia': [['1'], ['KAT'], 1000000, 1000000, (677, 126)],
        'Koropi': [['3'], ['Airport', 'Paiania - Kantza'], 1000000, 1000000, (745, 603)],
        'Larissa Station': [['2'], ['Attiki', 'Metaxourghio'], 1000000, 1000000, (224, 511)],
        'Maroussi': [['1'], ['KAT', 'Neratziotissa'], 1000000, 1000000, (595, 209)],
        'Megaro Moussikis': [['3'], ['Ambelokipi', 'Evangelismos'], 1000000, 1000000, (468, 601)],
        'Metaxourghio': [['2'], ['Omonia', 'Larissa Station'], 1000000, 1000000, (223, 546)],
        'Monastiraki': [['1', '3'], ['Omonia', 'Thissio', 'Kerameikos', 'Syntagma'], 1000000, 1000000, (270, 615)],
        'Moschato': [['1'], ['Kallithea', 'Faliro'], 1000000, 1000000, (172, 779)],
        'Nea Ionia': [['1'], ['Pefkakia', 'Iraklio'], 1000000, 1000000, (396, 294)],
        'Neos Kosmos': [['2'], ['Sygrou - Fix', 'Aghios Ioannis'], 1000000, 1000000, (321, 740)],
        'Neratziotissa': [['1'], ['Irini', 'Maroussi'], 1000000, 1000000, (547, 256)],
        'Nomismatokopio': [['3'], ['Aghia Paraskevi', 'Holargos'], 1000000, 1000000, (602, 466)],
        'Omonia': [['1', '2'], ['Victoria', 'Panepistimio', 'Metaxourghio', 'Monastiraki'], 1000000, 1000000,
                   (269, 570)],
        'Paiania - Kantza': [['3'], ['Koropi', 'Pallini'], 1000000, 1000000, (745, 470)],
        'Pallini': [['3'], ['Paiania - Kantza', 'Doukissis Plokentias'], 1000000, 1000000, (745, 411)],
        'Panepistimio': [['2'], ['Omonia', 'Syntagma'], 1000000, 1000000, (298, 594)],
        'Panormou': [['3'], ['Katehaki', 'Ambelokipi'], 1000000, 1000000, (513, 556)],
        'Pefkakia': [['1'], ['Nea Ionia', 'Perissos'], 1000000, 1000000, (374, 317)],
        'Perissos': [['1'], ['Pefkakia', 'Ano Patissia'], 1000000, 1000000, (348, 341)],
        'Petralona': [['1'], ['Thissio', 'Tavros'], 1000000, 1000000, (258, 692)],
        'Piraeus': [['1'], ['Faliro'], 1000000, 1000000, (27, 821)],
        'Sepolia': [['2'], ['Aghios Antonios', 'Attiki'], 1000000, 1000000, (183, 428)],
        'Sygrou - Fix': [['2'], ['Akropoli', 'Neos Kosmos'], 1000000, 1000000, (321, 702)],
        'Syntagma': [['2', '3'], ['Panepistimio', 'Akropoli', 'Evangelismos', 'Monastiraki'], 1000000, 1000000,
                     (317, 614)],
        'Tavros': [['1'], ['Petralona', 'Kallithea'], 1000000, 1000000, (228, 721)],
        'Thissio': [['1'], ['Monastiraki', 'Petralona'], 1000000, 1000000, (269, 662)],
        'Victoria': [['1'], ['Attiki', 'Omonia'], 1000000, 1000000, (269, 533)]}


# Calcula la distancia eucídea entre 2 pixeles.
def distancia(a, b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)


# Resetea los valores de g y f del mapa (para poder hacer llamadas sucesivas a aStar).
def reset():
    for e in mapa.keys():
        ee = mapa.get(e)
        ee[2] = 1000000
        ee[3] = 1000000


# Implementacion del algoritmo A*.
def aStar(start, end):
    openSet = [start]
    closed_set = []
    cameFrom = {}
    mapa.get(start)[2] = 0
    mapa.get(start)[3] = int(distancia(mapa.get(start)[4], mapa.get(end)[4]))
    current = openSet[0]
    while len(openSet) > 0:
        current = openSet[0]
        for e in openSet:
            if mapa.get(e)[3] < mapa.get(current)[3]:
                current = e
        if current == end:
            break
        openSet.remove(current)
        closed_set.append(current)
        for e in mapa.get(current)[1]:
            if e in closed_set:
                continue
            tentative = mapa.get(current)[2] + distancia(mapa.get(current)[4], mapa.get(e)[4])
            if e not in openSet or tentative < mapa.get(e)[2]:
                cameFrom[e] = current
                lineaFutura = [-1]
                if current != start:
                    lineaActual = ([value for value in mapa.get(current)[0] if value in mapa.get(cameFrom[current])[0]])
                    lineaFutura = ([value for value in lineaActual if value in mapa.get(e)[0]])
                aux = ([value for value in mapa.get(e)[0] if value in mapa.get(end)[0]])
                if len(lineaFutura) == 0:
                    if len(aux) >= 1:
                        h = 1.5
                    else:
                        h = h_multiplier
                else:
                    if len(aux) >= 1:
                        h = 0.4
                    else:
                        h = 1
                mapa.get(e)[2] = tentative
                mapa.get(e)[3] = tentative + h * distancia(mapa.get(e)[4], mapa.get(end)[4])
                if e not in openSet:
                    openSet.append(e)
    if current != end:
        print("no hay camino")  # No deberia pasar
    # Reconstruir camino.
    camino = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        camino.insert(0, current)
    return camino


def get_estacion(x, y):
    index = 0
    for e in mapa:
        elem = mapa[e]
        if elem[4][0] in range(x-get_estacion_precision, x+get_estacion_precision) \
                and elem[4][1] in range(y-get_estacion_precision, y+get_estacion_precision):
            return index, e
        index = index+1
    return -1


def main():
    # Ventana.
    root = Tk()
    root.title("Plano Metro Atenas")
    root.geometry("900x908")  # Dimensiones de la imagen de fondo (mapa.png).
    root.resizable(False, False)
    canvas = Canvas(root, width=900, height=986)
    canvas.pack()
    bg = PhotoImage(file='mapa.png')
    luces = PhotoImage(file='luces.png')
    canvas.create_image(450, 454, image=bg)  # Establecer mapa.png como fondo.
    canvas.create_image(495, 50, image=luces)
    # Decoraciones.
    canvas.create_rectangle(40, 120, 320, 268)

    # Desplegables.
    values = [*mapa]  # Valores de los desplegables.

    # Origen.
    selOrigen = AutocompleteCombobox(root, height=15)
    selOrigen.set_completion_list(values)
    selOrigen.place(x=50, y=135)

    # Destino.
    selDestino = AutocompleteCombobox(root, height=15)
    selDestino.set_completion_list(values)
    selDestino.place(x=50, y=165)

    # Accion del boton.
    borrar_linea = []  # Entidades de la linea del camino anterior para borrar.

    def dale():
        start = selOrigen.get()
        end = selDestino.get()
        if start == "":
            print("Seleccione estacion origen.")
        elif end == "":
            print("Seleccione estacion destino.")
        else:
            if start in values and end in values:
                # Resetear los valores de f y g del mapa.
                reset()
                # Borrar los caminos antiguos del mapa.
                for e in borrar_linea:
                    canvas.delete(e)
                borrar_linea.clear()
                # Calcular el camino.
                path = aStar(start, end)
                prev = path[0]
                # Representar el camino.
                for i in path[1:]:
                    c_curr = mapa.get(i)[4]
                    c_prev = mapa.get(prev)[4]
                    if i in ["Iraklio", "Irini"] and prev in ["Iraklio", "Irini"]:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 433, 260,
                                                               fill='#ff9100', width=4))
                        borrar_linea.append(canvas.create_line(433, 260, c_curr[0], c_curr[1],
                                                               fill='#ff9100', width=4))
                    elif i in ["Victoria", "Attiki"] and prev in ["Victoria", "Attiki"]:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 268, 514,
                                                               fill='#ff9100', width=4))
                        borrar_linea.append(canvas.create_line(268, 514, c_curr[0], c_curr[1],
                                                               fill='#ff9100', width=4))
                    elif i in ["Metaxourghio", "Omonia"] and prev in ["Metaxourghio", "Omonia"]:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 228, 565,
                                                               fill='#ff9100', width=4))
                        borrar_linea.append(canvas.create_line(228, 565, c_curr[0], c_curr[1],
                                                               fill='#ff9100', width=4))
                    elif i in ["Kerameikos", "Monastiraki"] and prev in ["Kerameikos", "Monastiraki"]:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 180, 612,
                                                               fill='#ff9100', width=4))
                        borrar_linea.append(canvas.create_line(180, 612, c_curr[0], c_curr[1],
                                                               fill='#ff9100', width=4))
                    elif i in ["Thissio", "Petralona"] and prev in ["Thissio", "Petralona"]:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 267, 679,
                                                               fill='#ff9100', width=4))
                        borrar_linea.append(canvas.create_line(267, 679, c_curr[0], c_curr[1],
                                                               fill='#ff9100', width=4))
                    elif i in ["Piraeus", "Faliro"] and prev in ["Piraeus", "Faliro"]:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 125, 820,
                                                               fill='#ff9100', width=4))
                        borrar_linea.append(canvas.create_line(125, 820, c_curr[0], c_curr[1],
                                                               fill='#ff9100', width=4))
                    elif i in ["Syntagma", "Akropoli"] and prev in ["Syntagma", "Akropoli"]:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 321, 630,
                                                               fill='#ff9100', width=4))
                        borrar_linea.append(canvas.create_line(321, 630, c_curr[0], c_curr[1],
                                                               fill='#ff9100', width=4))
                    elif i in ["Evangelismos", "Megaro Moussikis"] and prev in ["Evangelismos", "Megaro Moussikis"]:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 453, 613,
                                                               fill='#ff9100', width=4))
                        borrar_linea.append(canvas.create_line(453, 613, c_curr[0], c_curr[1],
                                                               fill='#ff9100', width=4))
                    elif i in ["Doukissis Plokentias", "Pallini"] and prev in ["Doukissis Plokentias", "Pallini"]:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 736, 391,
                                                               fill='#ff9100', width=4))
                        borrar_linea.append(canvas.create_line(736, 391, c_curr[0], c_curr[1],
                                                               fill='#ff9100', width=4))
                    elif i in ["Koropi", "Airport"] and prev in ["Koropi", "Airport"]:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 756, 635,
                                                               fill='#ff9100', width=4))
                        borrar_linea.append(canvas.create_line(756, 635, c_curr[0], c_curr[1],
                                                               fill='#ff9100', width=4))
                    else:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], c_curr[0], c_curr[1],
                                                               fill='#ff9100', width=4))
                    prev = i
            else:
                print("Nombre de estacion incorrecto.")

    def showInfo():
        info_root = Tk()
        info_root.geometry("385x300")
        info_root.title("Información sobre el grupo")
        Label(info_root, text="Grupo 29:", font="Calibri 15 bold").pack(anchor=W)
        Label(info_root, text="Bolinches Segovia, Jorge", font="Calibri 12 bold").pack(anchor=W)
        Label(info_root, text="\tnºmatrícula: a180113\n\t"
                              "j.bolinches@alumnos.upm.es", font="Calibri 12").pack(anchor=W)
        Label(info_root, text="Cerezo Pomykol, Jan (coordinador)", font="Calibri 12 bold").pack(anchor=W)
        Label(info_root, text="\tnºmatrícula: a180305\n\t"
                              "j.cerezo@alumnos.upm.es", font="Calibri 12").pack(anchor=W)
        Label(info_root, text="Garcillán Bartolomé, Ignacio", font="Calibri 12 bold").pack(anchor=W)
        Label(info_root, text="\tnºmatrícula: z170361\n\t"
                              "ignacio.garcillan.bartolome@alumnos.upm.es", font="Calibri 12").pack(anchor=W)
        Label(info_root, text="Moreno Nuñez, Pablo", font="Calibri 12 bold").pack(anchor=W)
        Label(info_root, text="\tnºmatrícula: a180053\n\t"
                              "pablo.moreno.nunez@alumnos.upm.es", font="Calibri 12").pack(anchor=W)
        info_root.mainloop()

    # Botones
    b1 = tkinter.Button(root, text="Calcular camino", command=dale)
    b1.place(x=50, y=195)

    b2 = tkinter.Button(root, text="Mostrar información sobre el grupo", command=showInfo)
    b2.place(x=50, y=230)

    def get_origen(event):
        x = event.x
        y = event.y
        estacion = get_estacion(x, y)
        if estacion != -1:
            selOrigen.current(estacion[0])
        canvas.unbind("<Button 1>")
        b3.config(bg="SystemButtonFace")

    def pick_origen():
        b3.config(bg="cyan")
        canvas.bind("<Button 1>", get_origen)

    def get_destino(event):
        x = event.x
        y = event.y
        estacion = get_estacion(x, y)
        if estacion != -1:
            selDestino.current(estacion[0])
        canvas.unbind("<Button 1>")
        b4.config(bg="SystemButtonFace")

    def pick_destino():
        b4.config(bg="cyan")
        canvas.bind("<Button 1>", get_destino)

    b3 = tkinter.Button(root, text="Seleccionar origen", command=pick_origen)
    b3.place(x=200, y=132)
    b4 = tkinter.Button(root, text="Seleccionar destino", command=pick_destino)
    b4.place(x=200, y=162)

    root.mainloop()


if __name__ == '__main__':
    main()
