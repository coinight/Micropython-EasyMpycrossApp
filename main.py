import os
import subprocess
import webbrowser
import tkinter as tk
from tkinter.filedialog import askopenfilenames, askdirectory
from tkinter.messagebox import showerror, showinfo, showwarning

import mpy_cross

HEIGHT = 350
WIDTH = 550
root = tk.Tk()
root.title("Mpy翻译姬 --by阿辰")
root.geometry(f"{WIDTH}x{HEIGHT}")

root.iconphoto(False, tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'title.png')))

root.resizable(False, False)

file_list_len = tk.IntVar()
out_put = os.getcwd()
march_type = tk.IntVar()
march_type.set(7)
# 架构选择列表
march_type_list = [("armv6", 0),
                   ("armv6m", 1),
                   ("armv7m", 2),
                   ("armv7em", 3),
                   ("armv7emsp", 4),
                   ("armv7emdp", 5),
                   ("xtensa", 6),
                   ("xtensawin", 7)]
march_rb = []

emit_type = tk.IntVar()
# 编码选择列表
emit_type_list = [("bytecode", 0),
                  ("native", 1),
                  ("viper", 2)]
emit_rb = []
help_list = [("1", "选择 .py 文件"),
             ("2", "选择编码方式"),
             ("3", "选择架构(可选)"),
             ("4", "生成"),
             ("?", "看文档")]


def change_emit_type():
    """
    改变编码方式

    Returns:

    """
    if emit_type.get():
        for rb in march_rb:
            rb.config(state=tk.ACTIVE)
    else:
        for rb in march_rb:
            rb.config(state=tk.DISABLED)


def generate_mpy():
    """
    生成 MPY 文件
    Returns:

    """
    if not file_list_len.get():
        showerror(title="错误", message="没有选择需要转换的文件")
        return False

    selected_folder = askdirectory(title="选择保存的文件夹", initialdir=out_put)
    if selected_folder == "":
        return False

    success_list = []
    for _ in range(file_list_len.get()):
        fn = file_list_box.get(tk.END)
        file_name = selected_folder + "/" + os.path.basename(fn).split('.')[0]
        res = mpy_cross.run(fn, "-o", f"{file_name + '.mpy'}", f"-march={march_type_list[march_type.get()][0]}",
                            "-X",
                            f"emit={emit_type_list[emit_type.get()][0]}",
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res_err = res.stderr.read()
        res_out = res.stdout.read()
        if res_err == res_out == b'':
            success_list.append(os.path.basename(fn))
        file_list_box.delete(tk.END)

    if not len(success_list):
        showerror(title="错误", message="不兼容的代码")
    elif 0 < len(success_list) < file_list_len.get():
        showwarning(title="部分成功",
                    message=f"{file_list_len.get()}共个文件/成功{len(success_list)}个文件\n{','.join(success_list)}\n文件保存在{selected_folder}")
    else:
        showinfo(title="成功", message=f"共{file_list_len.get()}个文件\n文件保存在{selected_folder}")
    file_list_len.set(0)
    return True


def select_files():
    """
    选择需要转换的文件

    Returns: selected_python_path:list 需要转换的 py 文件路径

    """
    file_list_box.delete(first="0", last=tk.END)
    selected_python_path = askopenfilenames(title="选择 Python 文件", filetypes=(("Python files", "*.py"),))
    for i, file_name in enumerate(selected_python_path):
        file_list_box.insert(i, file_name)
    file_list_len.set(len(selected_python_path))
    return selected_python_path


def show_info():
    """
    显示关于信息

    Returns:

    """
    author_homepage_url = "https://space.bilibili.com/87690728"
    github_url = "https://github.com/coinight/Micropython-EasyMpycrossApp"
    info = tk.Tk()
    info.title("关于")

    tk.Label(info, text="工具版本").pack()
    tk.Label(info, text='Mpy-cross -version 0.2c\n', fg="green").pack()
    tk.Label(info, text="mpy-cross 版本").pack()
    tk.Label(info, text=mpy_cross.run('--version', stdout=subprocess.PIPE).stdout.read().decode(), fg="green").pack()
    tk.Label(info, text="作者主页").pack()
    author_homepage_label = tk.Label(info, text=author_homepage_url, fg="blue", cursor="hand2")
    author_homepage_label.pack()
    tk.Label(info, text="Github").pack()
    github_url_label = tk.Label(info, text=github_url, fg="blue", cursor="hand2")
    github_url_label.pack()

    author_homepage_label.bind("<ButtonRelease-1>", func=lambda _: webbrowser.open_new(author_homepage_url))
    github_url_label.bind("<ButtonRelease-1>", func=lambda _: webbrowser.open_new(github_url))
    info.geometry("400x250")


file_frame = tk.LabelFrame(root, text="需要转换的文件")
file_frame.place(width=WIDTH // 2, height=HEIGHT, x=0, y=0)

file_list_box = tk.Listbox(file_frame, width=WIDTH // 2, height=HEIGHT)
file_list_box.pack()

button_frame = tk.Frame(root)
button_frame.place(width=WIDTH // 2, height=HEIGHT // 5, x=WIDTH // 2, y=0)
tk.Button(button_frame, text="关于", command=show_info).grid(column=1, row=1, padx=20, pady=30)
tk.Button(button_frame, text="选择文件", command=select_files).grid(column=2, row=1, padx=20)
tk.Button(button_frame, text="生成", command=generate_mpy).grid(column=3, row=1, padx=20)

# 选项
# TODO:
#  -s
#  -v
#  -msmall-int-bits
#  -heapsize
option_frame = tk.LabelFrame(root, text="选项")
option_frame.place(width=WIDTH // 2, height=HEIGHT - HEIGHT // 5, x=WIDTH // 2, y=HEIGHT // 4)

# 帮助框
help_frame = tk.LabelFrame(option_frame, text="如何操作?")
help_frame.place(anchor="nw", x=0, y=0, width=WIDTH // 4, height=HEIGHT // 3 + 20)
for _title, _info in help_list:
    tk.Label(help_frame, text=f"{_title}.{_info}").pack(anchor="nw")
# 编码方式
emit_frame = tk.LabelFrame(option_frame, text="编码方式")
emit_frame.place(anchor="nw", x=0, y=HEIGHT // 3 + 20, width=WIDTH // 4, height=HEIGHT // 3)
for name, num in emit_type_list:
    radio_button = tk.Radiobutton(emit_frame, text=name, variable=emit_type, value=num, command=change_emit_type)
    emit_rb.append(radio_button)
    radio_button.pack(anchor='w')

# 架构选择
march_frame = tk.LabelFrame(option_frame, text="架构选择")
march_frame.place(anchor="nw", x=WIDTH // 4, y=0, width=WIDTH // 4, height=HEIGHT - HEIGHT // 5)
for name, num in march_type_list:
    radio_button = tk.Radiobutton(march_frame, text=name, variable=march_type, value=num, state=tk.DISABLED)
    march_rb.append(radio_button)
    radio_button.pack(anchor='w')
root.mainloop()
