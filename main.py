import tkinter.filedialog
import subprocess
from tkinter import *
import os
import webbrowser

def SupportAuthor():
    webbrowser.open_new('https://space.bilibili.com/87690728')
def ShowInfo():
    global root
    infoWindow = Tk()
    infoWindow.title("关于")
    # info windows
    infoLog = Label(infoWindow, text='Mpy-cross -version 0.2c\n',fg="green")
    support = Button(infoWindow, text="-点我支持作者-", fg="red",command=SupportAuthor)
    infoLog2 = Label(infoWindow, text='支持esp32 esp32s3 esp32s2 rpi-pico\n'
                                      'esp选择xtensa\n'
                                      'rpi-pico选择armv7emdp')

    infoLog.pack()
    infoLog2.pack()
    support.pack()
    infoWindow.update()
    SetPos(infoWindow,infoWindow.winfo_width(),infoWindow.winfo_height(),root.winfo_x(),root.winfo_y())

def InstallEnvironment():
    global log, root
    log.config(text='安装环境中，请等待')
    root.update()
    r = subprocess.Popen('pip install mpy-cross', shell=True)
    r.wait()
    log.config(text='必须有python环境；再次选择同一文件反选')


def Select():
    global chooseLabel, chooseFile
    filenames = tkinter.filedialog.askopenfiles(filetypes=(("python files", "*.py"),))
    print(filenames)
    for f in filenames:
        filename = f.name
        if filename != "":
            if filename in chooseFile:
                chooseFile.remove(filename)
            else:
                chooseFile.append(filename)
            chooseLabel.config(text='choose:\n' + '\n'.join(map(str, chooseFile)))
    ResetRootSize()


def SetPos(windows: Tk, w, h, x, y):
    windows.geometry(f"{w}x{h}+{x}+{y}")


def ResetRootSize():
    global chooseFile, root, w, h, btns, btnPosz
    size = len(chooseFile)
    x, y = root.winfo_x(), root.winfo_y()
    sizeW, sizeH = w, h
    sizeH = h + 20 * size
    root.geometry(f"{sizeW}x{sizeH}+{x}+{y}")
    i = 0
    for btn in btns:
        btn.winfo_x()
        btn.place(x=btnPosz[i][0], y=btnPosz[i][1] + 20 * size)
        print(btnPosz[i])
        i += 1


def OutPut():
    global chooseLabel, chooseFile, v
    filename = tkinter.filedialog.askdirectory()
    if filename != "":
        if filename[-1] != "/":
            filename += "/"
        for m in chooseFile:
            t = 'mpy-cross ' + m + ' -o ' + filename + m.split('/')[-1].split('.')[0] + '.mpy'
            if v.get() == 0:
                t += ' -march=xtensa'
            elif v.get() == 1:
                t += ' -march=armv7emdp'
            elif v.get() == 2:
                t += ' -march=x86'
            elif v.get() == 3:
                t += ' -march=x64'
            print('输出', t)
            subprocess.run(t)

            # mpy-cross button.py - o e:\1.mpy
        chooseFile = []
        chooseLabel.config(text='')
        print(isOpenFold.get())
        if isOpenFold.get():
            os.startfile(filename)
    else:
        return
    ResetRootSize()


w, h = 550, 140
outDir = ''
chooseFile: list[str] = []
root = Tk()

root.title("Mpy翻译姬 --by阿辰")

root.geometry("550x140+700+500")
root.iconphoto(False, tkinter.PhotoImage(file='title.png'))
size = 0, 0
root.resizable(*size)

log = Label(root, text='必须有python环境；再次选择同一文件反选')
log.pack()
chooseLabel = Label(root, text='')
chooseLabel.pack()

v = tkinter.IntVar()
v.set(0)
tkinter.Radiobutton(root, text='xtensa', variable=v, value=0).place(x=450, y=20)
tkinter.Radiobutton(root, text='armv7emdp', variable=v, value=1).place(x=450, y=40)
tkinter.Radiobutton(root, text='x86', variable=v, value=2).place(x=450, y=60)
tkinter.Radiobutton(root, text='x64', variable=v, value=3).place(x=450, y=80)

# mpy-cross支持架构 x86, x64, armv6, armv6m, armv7m, armv7em, armv7emsp, armv7emdp, xtensa, xtensawin
# s3 esp32 xtensa
# rpi pico armv7emdp
btns: list[Widget] = []
btnPosz: list[tuple] = []

btn0 = Button(root, text="安装环境", command=InstallEnvironment, width="6")
btn0.place(x=0, y=110)
root.update()

btns.append(btn0)
btnPosz.append((btns[-1].winfo_x(), btns[-1].winfo_y()))

btn1 = Button(root, text="选择文件", command=Select, width="10")
btn1.place(x=150, y=100)
root.update()

btns.append(btn1)
btnPosz.append((btns[-1].winfo_x(), btns[-1].winfo_y()))

btn2 = Button(root, text="输出", command=OutPut, width="10")
btn2.place(x=270, y=100)
root.update()

btns.append(btn2)
btnPosz.append((btns[-1].winfo_x(), btns[-1].winfo_y()))

btn3 = Button(root, text="关于", command=ShowInfo, width="6")
btn3.place(x=0, y=80)
root.update()

btns.append(btn3)
btnPosz.append((btns[-1].winfo_x(), btns[-1].winfo_y()))

isOpenFold =tkinter.IntVar()
checkb = Checkbutton(text='转换后打开文件夹',variable=isOpenFold)
checkb.place(x=400, y=100)
root.update()

btns.append(checkb)
btnPosz.append((btns[-1].winfo_x(), btns[-1].winfo_y()))

root.mainloop()
