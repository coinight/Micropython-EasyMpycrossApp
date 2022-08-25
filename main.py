import tkinter.filedialog
import subprocess
from tkinter import *
import os


def InstallEnvironment():
    r = subprocess.Popen('pip install mpy-cross', shell=True)
    r.wait()


def Select():
    global chooseLabel, chooseFile
    filenames = tkinter.filedialog.askopenfiles()
    print(filenames)
    for f in filenames:
        filename = f.name
        if filename != "" and filename[-3:] == '.py':
            if filename in chooseFile:
                chooseFile.remove(filename)
            else:
                chooseFile.append(filename)
            chooseLabel.config(text='choose:\n' + '\n'.join(map(str, chooseFile)))
    ResetRootSize()


def ResetRootSize():
    global chooseFile, root, w, h, btns,btnPosz
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
btns: list[Button] = []
btnPosz: list[tuple] = []


btn0 = Button(root, text="安装环境", command=InstallEnvironment, width="6")
btn0.place(x=0, y=110)
root.update()

btns.append(btn0)
btnPosz.append((btns[-1].winfo_x(),btns[-1].winfo_y()))


btn1 = Button(root, text="选择文件", command=Select, width="10")
btn1.place(x=100, y=100)
root.update()

btns.append(btn1)
btnPosz.append((btns[-1].winfo_x(),btns[-1].winfo_y()))


btn2 = Button(root, text="输出", command=OutPut, width="10")
btn2.place(x=250, y=100)
root.update()

btns.append(btn2)
btnPosz.append((btns[-1].winfo_x(),btns[-1].winfo_y()))

root.mainloop()
