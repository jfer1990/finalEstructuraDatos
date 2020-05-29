import tkinter
from PIL import Image,ImageTk

class view:
    def __init__(self,root):
        self.root = root
    #    self.root.resizable(False,False)
        self.lienzo = tkinter.Canvas(root,width=1200,height=600)
        self.lienzo.pack(fill="both",expand="true",side="left")
        self.img = Image.open("mapa.pbm")
        self.img = self.img.resize((1200,600),Image.ANTIALIAS)
        self.imgCpy = self.img.copy()
        self.imgBackGround = ImageTk.PhotoImage(self.img)
        self.imagenFondo = self.lienzo.create_image(0,0,anchor="nw",image = self.imgBackGround)

        self.listaPosiciones = [("DireccionFmat-edA", 0.101, .891), ("cheto", .131, .776),("edB",0.082,0.712),("cafeFmat",0.12321,0.681818),
                                ("edC",0.082,0.571),("edD",0.1687,0.5173),("MaqDispensadora-Ed-D",0.13125,0.5735),
                                ("C-Cómputo-Fmat",0.2014,0.821),("Biblioteca",0.269,0.615),("EstacionamientoLabs",0.063,0.4719),
                                ("ed-H",0.1409,0.433),("FI-Renovables",0.2562,0.4768),("FI-Labs-Mecatronica",0.344,0.374),
                                ("FI-Labs-IngCivil",0.503,0.551),("DireccionFI",0.7562,0.292),("CafeFI",0.816,0.143),
                                ("Auditorio gral FI",0.815,0.389)]
        self.listBotones = []


        self.lienzo.bind('<Configure>',self.resizeImg)
        self.lienzo.bind('<Double-Button-1>',self.getRelPos)
        self.lienzo.bind('<Motion>',self.displayPlace)
        self.lienzo.bind('<Button-1>',self.displayPos)


    def resizeImg(self,event):
        new_width = event.width
        new_height = event.height

        self.img = self.imgCpy.resize((new_width, new_height))
        self.imgBackGround = ImageTk.PhotoImage(self.img)
        self.lienzo.itemconfig(self.imagenFondo,image=self.imgBackGround)


    def getRelPos(self,event):
        rad = .003
        x = event.x
        y = event.y


        ySize = self.lienzo.winfo_height()
        xSize = self.lienzo.winfo_width()
        xRel = x/xSize
        yRel = y/ySize


        return (xRel,yRel)
    def getAbsPos(self,tuplaPosiciones):
        x = tuplaPosiciones[0]
        y = tuplaPosiciones[1]
        ySize = self.lienzo.winfo_height()
        xSize = self.lienzo.winfo_width()
        return (x*xSize,y*ySize)


    def displayPlace(self,event):
        rad = .003

        posicion = self.getRelPos(event)
        xRel = posicion[0]
        yRel = posicion[1]

        for tupla in self.listaPosiciones:
            x = tupla[1]
            y = tupla[2]
            val = (xRel - x) ** 2 + (yRel - y) ** 2
            if val <= rad:
                self.dibujarSitio(tupla)
                return tupla
            else:
                for each in self.listBotones:
                    each.destroy()






    def dibujarSitio(self,tuplaPosiciones):
        drawRad=14

        texto = tuplaPosiciones[0]
        xRel = tuplaPosiciones[1]
        yRel = tuplaPosiciones[2]
        pos = self.getAbsPos((xRel, yRel))
        xAbs = pos[0]
        yAbs = pos[1]
        label = tkinter.Label(self.lienzo,text=texto,font=("Helvetica", 16),fg="white")
        label.config(bg='blue')
        label.place(relx=xRel,rely=yRel,anchor="sw")
        self.listBotones.append(label)

        #self.lienzo.create_oval(xAbs - drawRad, yAbs - drawRad, xAbs + drawRad, yAbs + drawRad)
    def displayPos(self,event):
        pos = self.getRelPos(event)
        print(str(pos[0])+","+str(pos[1]))




root = tkinter.Tk()
v = view(root)
root.mainloop()
