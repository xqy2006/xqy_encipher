from tkinter import *
from tkinter import filedialog
from binascii import a2b_hex
from binascii import b2a_hex
import tkinter.messagebox
import os
import shutil
def read(dir,address,length):
    f = open(dir, "rb+")
    f.seek(address, 0)
    result = f.read(length)
    result = b2a_hex(result)
    result = bytes.decode(result)
    return result
def write(write_bytes,dir,address):
    write_bytes=bytes().fromhex(write_bytes)
    with open(dir, 'rb+') as f:
        f.seek(address, 0)
        return f.write(write_bytes)
def coding(dir,mima,mima_len,cha):
    file_stats = os.stat(dir)
    max = int(file_stats.st_size)
    i = 0
    while True:
        if i+1>=max:
            break
        a=int(read(dir,i,mima_len//2),16)
        abc = str(hex(a^mima))[2:]
        if len(abc)%2!=0:
            abc = '0'+abc
        write(abc,dir,i)
        i += cha
def jiami(dir,save_dir,mima,mima_len,cha):
    shutil.copyfile(dir,save_dir)
    coding(save_dir,mima,mima_len,cha)
def jiemi(dir,save_dir,mima,mima_len,cha):
    shutil.copyfile(dir, save_dir)
    coding(save_dir,mima,mima_len,cha)
def function1():
    global file_path2
    OpenFile = Tk()   #创建新窗口
    OpenFile.withdraw()
    file_path2 = filedialog.askopenfilename(filetypes=[('XUQINYANG FILES','.xqy')]) # 获取路径
    a3.insert(INSERT, file_path2)
def function2():
    global file_path1
    OpenFile = Tk()   #创建新窗口
    OpenFile.withdraw()
    file_path1 = filedialog.askopenfilename() # 获取路径
    a2.insert(INSERT, file_path1)
def function3():#jiami
    mima = int(a1.get())
    mima_len = len(str(mima))
    cha = int(ch.get())
    save_dir = filedialog.asksaveasfilename(initialfile=file_path1+'.xqy',filetypes=[('XUQINYANG FILES','.xqy')])
    if save_dir!='':
        jiami(file_path1,save_dir,mima,mima_len,cha)
        tkinter.messagebox.showinfo('加密','加密完成，保存路径为'+save_dir)
def function4():#jiemi
    mima = int(a1.get())
    mima_len = len(str(mima))
    cha = int(ch.get())
    save_dir = filedialog.asksaveasfilename(initialfile=file_path2[:file_path2.rfind('.')])
    if save_dir!='':
        jiemi(file_path2,save_dir,mima,mima_len,cha)
        tkinter.messagebox.showinfo('解密','解密完成，保存路径为'+save_dir)
def functionWarn():
    tkinter.messagebox.showinfo('加密公差说明', '加密公差与加密速率息息相关，加密公差越大，效率越高，但切记其大小不要超过文件字节数，也不要小于密码位数')
root = Tk()
root.title('xqy_encipher')
root.minsize(410, 110)
root.maxsize(410, 110)
LW = Button(root,text='加密公差说明',command=functionWarn,width=10)
L1 = Label(root, text="密码:",width=10)
a1 = Entry(root,width=20)
Lch = Label(root, text="加密公差:",width=10)
ch = Entry(root,width=20)
L2 = Label(root, text="加密:",width=10)
a2 = Entry(root,width=20)
b = Button(root,text='浏览',command=function2,width=10)
c = Button(root,text='加密',command=function3,width=10)
L3 = Label(root, text="解密:",width=10)
a3 = Entry(root,width=20)
d = Button(root,text='浏览',command=function1,width=10)
e = Button(root,text='解密',command=function4,width=10)
ch.insert(0, '100')
L1.grid(row=0,column=0)
a1.grid(row=0,column=1)  # 将小部件放置到主窗口中
b.grid(row=2,column=2)
c.grid(row=2,column=3)
d.grid(row=3,column=2)
e.grid(row=3,column=3)
L2.grid(row=2,column=0)
L3.grid(row=3,column=0)
a2.grid(row=2,column=1)
a3.grid(row=3,column=1)
Lch.grid(row=1,column=0)
ch.grid(row=1,column=1)
LW.grid(row=1,column=2)
root.mainloop()  # 进入消息循环