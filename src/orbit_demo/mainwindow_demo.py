# -*- coding: utf-8 -*- 
from PIL import Image, ImageTk, ImageDraw
from tkinter import Tk, Text, BOTH, W, N, E, S, Canvas, NW
from tkinter.ttk import Frame, Button, Label, Style

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)          
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        
        lbl = Label(self, text="Map") # заголовок слоя с картой
        lbl.grid(sticky=W, pady=4, padx=5)
        
        self.original = Image.open("img.gif") # открытие рисунка
        self.image = ImageTk.PhotoImage(self.original)
        
              
                 
        self.display = Canvas(self, bd=0, highlightthickness=0) # создаем слой для рисунка
        self.display.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")
        self.display.grid(row=1, column=0, columnspan=2, rowspan=4, 
            padx=5, sticky=W+E+N+S) # подстраивание размера слоя под свободное место
        self.pack(fill=BOTH, expand=1)
        self.bind("<Configure>", self.resize) # подстраивание размера фонового рисунка под размер слоя
        
        # Кнопки
        
        lbla = Label(self, text="Trajectory parameters:")
        lbla.grid(row=5, column=0, padx=5)
        
        abtn = Button(self, text="Open")
        abtn.grid(row=1, column=3)

        cbtn = Button(self, text="Calculate")
        cbtn.grid(row=2, column=3, pady=4)
        
        hbtn = Button(self, text="Show trajectory")
        hbtn.grid(row=3, column=3)

        obtn = Button(self, text="Help")
        obtn.grid(row=4, column=3)  
        
    def resize(self, event): # изменения размера окна
        size = (event.width, event.height) # изменения ширины и высоты
        resized = self.original.resize(size,Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized) # изменение размера фонового рисунка
        self.display.delete("IMG")
        self.display.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")
        
        
def main():
    root = Tk() #Производим инициализацию нашего графического интерфейса
    root.title("Orbit") # заголовок окна
    root.geometry("640x510") # первоначальные размеры окна
    app = Example(root) # передаем обьекту Example root
    root.mainloop() # Создаем постоянный цикл
  
if __name__ == '__main__':
    main()