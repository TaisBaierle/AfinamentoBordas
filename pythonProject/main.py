from PIL import ImageTk
import PIL.Image
from tkinter import *
from tkinter import filedialog

PIXEL_BRANCO = 1
PIXEL_PRETO = 0

class Afinamento:
    def __init__(self, master=None):
        self.topContainer = Frame(master)
        self.topContainer.pack(side='top')
        self.bottomContainer = Frame(master)
        self.bottomContainer.pack(side='bottom')

        self.imgPathContainer = Frame(self.topContainer)
        self.imgPathContainer.pack(side='top')
        self.labelPath = Label(self.imgPathContainer, text="Selecione a imagem.")
        self.labelPath.pack(side='left')

        self.btnPath = Button(self.imgPathContainer, text='...', command=self.filedialog)
        self.btnPath.pack(side='right')

        self.imgOriginalContainer = Frame(self.bottomContainer)
        self.imgOriginalContainer.pack(side='left')
        self.imgEditadaContainer = Frame(self.bottomContainer)
        self.imgEditadaContainer.pack(side='right')

        self.imgOriginal = Label(self.imgOriginalContainer)
        self.imgOriginal.pack(side="bottom", fill="both")
        self.labelOriginal = Label(self.imgOriginalContainer, text='Imagem original:')
        self.labelOriginal.pack(side="top", fill="both")

        self.imgEditada = Label(self.imgEditadaContainer)
        self.imgEditada.pack(side="bottom", fill="both")
        self.labelEditada = Label(self.imgEditadaContainer, text='Nova imagem:')
        self.labelEditada.pack(side="top", fill="both")

    def filedialog(self):
        novaImagem = filedialog.askopenfile(initialdir='/', title='Selecione o quadro.',
                                               filetype=(
                                                   ('jpeg', '*.jpg'), ('png', '*.png'), ('Todos os tipos', '*.*')))
        if(novaImagem):
            self.labelPath['text'] = novaImagem.name
            self.atualizarImg(novaImagem.name)

    def atualizarImg(self, path=None):
        if path is None:
            self.img = PIL.Image.new('1', (300, 300))
            self.photo = ImageTk.PhotoImage(self.img)
            self.imgOriginal['image'] = self.photo
            self.imgEditada['image'] = self.photo
            self.labelPath['text'] = 'Selecione um quadro.'
        else:
            self.img = PIL.Image.open(path)
            self.photo = ImageTk.PhotoImage(self.img)
            self.imgOriginal['image'] = self.photo
            self.imgEditada['image'] = self.photo
            self.zhangSuen()

    def binaria(self, img, meio):
        old = img.load()
        new = PIL.Image.new('1', (img.width, img.height))
        pixel = new.load()
        for x in range(img.width):
            for y in range(img.height):
                media = round((old[x, y][0] + old[x, y][1] + old[x, y][2]) / 3)
                pixel[x, y] = PIXEL_BRANCO if media > meio else PIXEL_PRETO
        return new

    def vizinhos(self, x, y, img):
        p2 = img[x, y - 1]
        p3 = img[x + 1, y - 1]
        p4 = img[x + 1, y]
        p5 = img[x + 1, y + 1]
        p6 = img[x, y + 1]
        p7 = img[x - 1, y + 1]
        p8 = img[x - 1, y]
        p9 = img[x - 1, y - 1]
        return [p2, p3, p4, p5, p6, p7, p8, p9]

    def qtdeVizinhosPretos(self, vizinhos):
        result = 0
        for v in vizinhos:
            if v == PIXEL_PRETO:
                result += 1
        return result

    def conectividade(self, vizinhos):
        result = 0
        v = vizinhos + vizinhos[0:1]  # P2, ... P9, P2
        for i in range(len(vizinhos)):
            result = (result + 1) if (v[i] == PIXEL_BRANCO and v[i+1] == PIXEL_PRETO) else result
        return result

    def zhangSuen(self):
        width = self.img.width
        height = self.img.height
        new = self.binaria(self.img, 123)
        img = new.load()

        iteracao1 = iteracao2 = [(-1, -1)]
        while iteracao1 or iteracao2:
            iteracao1 = []
            for x in range(1, width - 1):
                for y in range(1, height - 1):
                    if img[x, y] == 0:
                        vizinhos = P2, P3, P4, P5, P6, P7, P8, P9 = self.vizinhos(x, y, img)
                        if (self.conectividade(vizinhos) == 1  # 1
                            and 2 <= self.qtdeVizinhosPretos(vizinhos) < 7  # 2
                            and (P2 == PIXEL_BRANCO or P4 == PIXEL_BRANCO or P6 == PIXEL_BRANCO)  # 3
                            and (P4 == PIXEL_BRANCO or P6 == PIXEL_BRANCO or P8 == PIXEL_BRANCO)  # 4
                        ):
                            iteracao1.append((x, y))
            for x, y in iteracao1:
                img[x, y] = 1
            #
            iteracao2 = []
            for x in range(1, width - 1):
                for y in range(1, height - 1):
                    if img[x, y] == 0:
                        vizinhos = P2, P3, P4, P5, P6, P7, P8, P9 = self.vizinhos(x, y, img)
                        if(self.conectividade(vizinhos) == 1  # 1
                            and 2 <= self.qtdeVizinhosPretos(vizinhos) <= 6  # 2
                            and (P2 == PIXEL_BRANCO or P4 == PIXEL_BRANCO or P8 == PIXEL_BRANCO)  # 3
                            and (P2 == PIXEL_BRANCO or P6 == PIXEL_BRANCO or P8 == PIXEL_BRANCO)  # 4
                        ):
                            iteracao2.append((x, y))
            for x, y in iteracao2:
                img[x, y] = 1
        self.novaImg = new.convert('RGB')
        self.photoNew = ImageTk.PhotoImage(self.novaImg)
        self.imgEditada['image'] = self.photoNew


if __name__ == "__main__":
    root = Tk()
    root.state('zoomed')
    Afinamento(root)
    root.mainloop()
