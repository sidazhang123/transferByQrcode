from tkinter import *
from PIL import Image, ImageTk
import os, time, threading


class Frame:
    def __init__(self):
        self.colors = {'black': '#000000', 'white': '#ffffff'}
        # 创建窗口
        self.window = Tk()
        self.window.title("trigger")
        # self.window.state("zoomed")
        self.window.attributes("-topmost", True)

        # data
        self.pic_list = [i for i in os.listdir('.') if i.endswith('.jpg')]
        self.pic_list.sort(key=lambda x: int(x.split('.jpg')[0]))

        # indicator1
        self.indicator_label_1 = Label(self.window, bg=self.colors['black'], borderwidth=2, relief=SOLID)
        self.indicator_label_1.config(width=10, height=5)
        self.indicator_label_1.grid(row=0, column=0, padx=10, pady=10)

        # indicator2
        self.indicator_label_2 = Label(self.window, bg=self.colors['black'], borderwidth=2, relief=SOLID)
        self.indicator_label_2.config(width=10, height=5)
        self.indicator_label_2.grid(row=1, column=0, padx=10, pady=10)

        # start button
        self.button = Button(self.window, text=f"最大图号：{len(self.pic_list)}【START】", command=self.start)
        self.button.grid(row=2, column=0, padx=10, pady=10)

        # 创建窗口右侧的正方形label
        self.square_label = Label(self.window)
        self.square_label.grid(row=0, column=1, rowspan=3, columnspan=3, padx=10, pady=10)
        self.init_pic()

    def start(self):
        self.button.config(state=DISABLED)
        t = threading.Thread(target=self.poll_pics)
        t.start()

    def chg_color(self):
        color = {self.colors['black']: self.colors['white'], self.colors['white']: self.colors['black']}
        ind1 = color[self.indicator_label_1.cget('bg')]
        ind2 = color[self.indicator_label_2.cget('bg')]

        self.indicator_label_1.configure(bg=ind1)
        self.indicator_label_2.configure(bg=ind2)

    def init_pic(self):
        photo = ImageTk.PhotoImage(Image.open(self.pic_list[0]))
        self.square_label.config(image=photo)
        self.square_label.image = photo

    def poll_pics(self):
        self.indicator_label_1.configure(bg=self.colors['black'])
        self.indicator_label_2.configure(bg=self.colors['white'])

        for i, pic in enumerate(self.pic_list):
            print(pic)
            photo = ImageTk.PhotoImage(Image.open(pic))
            self.square_label.config(image=photo)
            self.square_label.image = photo

            self.chg_color()
            time.sleep(1)
        self.button.config(state=NORMAL)

        self.indicator_label_1.configure(bg=self.colors['white'])
        self.indicator_label_2.configure(bg=self.colors['white'])


if __name__ == "__main__":
    m = Frame()
    m.window.mainloop()
