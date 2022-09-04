# Micropython-EasyMpycrossApp
Auto translate `.py` file in disk (select) and output `.mpy`file to disk (output)

一个自动转换`.py`文件为`.mpy`文件的脚本

### 作用

本脚本是为了方便(或复杂)的操作`mpy-cross`来转换`.py`文件.

`mpy-cross`会将`.py`文件进行预编码,编码后的文件可以像普通文件一样导入.

>  预编码的格式有三种`bytecode`,`native`和`viper`
>
> `bytecode`:类似于`pyc`的字节码,兼容性最好的编码格式,不需要区分CPU架构,可直接替代`.py`文件
>
> `native`:将`.py`文件转换为操作码,目前不支持`riscv`架构
>
> `viper`:机器码,兼容性最差,需要进行代码修改,同样不支持`riscv`架构

### 简单上手

1. 克隆代码到本地

   ```bash
   git clone https://github.com/coinight/Micropython-EasyMpycrossApp.git
   cd Micropython-EasyMpycrossApp
   # 安装依赖项
   python -m pip install requirements.txt
   # 运行
   python main.py
   ```

   > 如果无法使用`git`或没有`python`环境可以下载打包好的脚本程序,并运行

2. 选择需要生成的`.py`文件,可以看到选择的文件在左半部分显示

3. 编码选择`bytecode`,选择要保存到的文件夹,点击生成

4. 将编译好的`.mpy`上传到开发板进行测试

---

### 加速代码

#### 确认你的芯片架构及`.mpy`版本

```python
import sys

try:
    sys_mpy = sys.implementation.mpy
except:
    sys_mpy = sys.implementation._mpy
arch = [None, 'x86', 'x64',
        'armv6', 'armv6m', 'armv7m', 'armv7em', 'armv7emsp', 'armv7emdp',
        'xtensa', 'xtensawin'][sys_mpy >> 10]
print('mpy version:', sys_mpy & 0xff)
print('mpy flags:', end='')
if arch:
    print(' -march=' + arch, end='')
if sys_mpy & 0x100:
    print(' -mcache-lookup-bc', end='')
if not sys_mpy & 0x200:
    print(' -mno-unicode', end='')
```

在开发板运行以上代码,可以知道你的芯片架构,如下

```bash
# rp 2040
>>> ...
mpy version: 6
mpy flags: -march=armv6m -mno-unicode
```

没有显示`march`则不支持`native`和`viper`

脚本生成的`.mpy`文件仅支持`v6`版本`mpy`,请确认你的`micropython`版本符合下表的规定,如果需要生成早期版本的`.mpy`需要自行`pip`下载

| `MicroPython`版本 | .mpy版本 |
| ----------------- | -------- |
| v1.19 及更高版本  | 6        |
| v1.12 - v1.18     | 5        |
| v1.11             | 4        |
| v1.9.3-v1.10      | 3        |
| v1.9-v1.92        | 2        |
| v1.5.1-v1.8.7     | 1        |

#### native

`native`会将代码转换为`CPU操作码`,因此你需要选择架构(参见上一节)为符合的架构

> `native`不兼容的代码
>
> 1. 上下文`With`
> 2. 生成器
> 3. 调用装饰器时不会传入被装饰函数
> 4. 自己发掘...

由此可见大部分代码可以直接编译为`native`而不需要或仅需要少量更改代码,因此建议使用`native`作为加速代码的主要方式

#### Viper

`viper`会将代码转换为`机器码`,因此你不仅需要选择架构而且需要更改大部分代码,

参见[最大化Micropython速度 — Micropython 1.19.1 文档 (micropython.org)](https://docs.micropython.org/en/latest/reference/speed_python.html#id14)

本篇不再赘述

### 打包为可执行文件

如果你的电脑没有`python`环境,可以使用已打包好的可执行文件,打包方式如下:

1. 拥有`Python`环境的电脑

2. 运行

   ```bash
   # 安装基本依赖项
   python -m pip install -r requirements.txt
   # 安装打包工具
   python -m pip install pyinstaller
   # 打包
   python build.py
   ```

3. 打开目录下的`dist/`目录,就可以看到打包好的应用

