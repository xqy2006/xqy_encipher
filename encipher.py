from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter.ttk
import threading
from binascii import a2b_hex
from binascii import b2a_hex
import tkinter.messagebox
import os
import shutil
import ctypes
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from multiprocessing import Queue
from multiprocessing import Process
def read(dir,address,length):
    f = open(dir, "rb+")
    f.seek(address, 0)
    result = f.read(length)
    result = b2a_hex(result)
    result = bytes.decode(result)
    f.close()
    return result
def write(write_bytes,dir,address):
    write_bytes=bytes().fromhex(write_bytes)
    f = open(dir, "rb+")
    f.seek(address, 0)
    result=f.write(write_bytes)
    f.close()
    return result
def realcode1(dir,mima,mima_len,i,num,q):
    file_stats = os.stat(dir)
    max = int(file_stats.st_size)
    while True:
        if i+1024>=(max*num)//64:
            q.put('done')
            break
        a=int(read(dir,i,mima_len//2+1),16)
        abc = str(hex(a^mima))[2:]
        while len(abc)<mima_len//2+1:
            abc = '0'+abc
        if len(abc)>mima_len//2+1:
            pass
        else:
            write(abc,dir,i)
        i += 1024
        q.put(1024)

def coding(dir,mima,mima_len):
    file_stats = os.stat(dir)
    max = int(file_stats.st_size)
    q = Queue()
    threads = []
    for i in range(64):
        threads.append(threading.Thread(target=realcode1, args=(dir,mima,mima_len,(max*i)//4,i+1,q,)))
    for i in threads:
        i.start()
    times = 0
    while True:
        stepnum = q.get()
        if stepnum=='done':
            times += 1
            if times == 64:
                bar1.stop()
                break
        else:
            root.update()
    for i in threads:
        i.join()
def jiami(dir,save_dir,mima,mima_len):
    shutil.copyfile(dir,save_dir)
    coding(save_dir,mima,mima_len)
def jiemi(dir,save_dir,mima,mima_len):
    shutil.copyfile(dir, save_dir)
    coding(save_dir,mima,mima_len)
def function1():
    global file_path2
    OpenFile = Tk()   #创建新窗口
    OpenFile.withdraw()
    file_path2 = filedialog.askopenfilename(filetypes=[('XUQINYANG FILES','.xqy')]) # 获取路径
    a3.delete(0, 'end')
    a3.insert(INSERT, file_path2)
def function2():
    global file_path1
    OpenFile = Tk()   #创建新窗口
    OpenFile.withdraw()
    file_path1 = filedialog.askopenfilename() # 获取路径
    a2.delete(0, 'end')
    a2.insert(INSERT, file_path1)
def function3():#jiami
    mima = a1.get()
    newmima = ''
    for i in mima:
        newmima = newmima+str(ord(i))
    mima = int(newmima)
    mima_len = len(str(mima))
    cha = 1024
    save_dir = filedialog.asksaveasfilename(initialfile=file_path1+'.xqy',filetypes=[('XUQINYANG FILES','.xqy')])
    if save_dir!='':
        bar1.start()
        jiami(file_path1,save_dir,mima,mima_len)
        tkinter.messagebox.showinfo('加密','加密完成，保存路径为'+save_dir)
def function4():#jiemi
    mima = a1.get()
    newmima = ''
    for i in mima:
        newmima = newmima+str(ord(i))
    mima = int(newmima)
    mima_len = len(str(mima))
    cha = 1024
    save_dir = filedialog.asksaveasfilename(initialfile=file_path2[:file_path2.rfind('.')])
    if save_dir!='':
        bar1.start()
        jiemi(file_path2,save_dir,mima,mima_len)
        tkinter.messagebox.showinfo('解密','解密完成，保存路径为'+save_dir)
if __name__ == '__main__':
    multiprocessing.freeze_support()

    root = Tk()
    root.title('xqy_encipher')
    root.minsize(410, 110)
    root.maxsize(410, 110)
    L1 = Label(root, text="密码:",width=10)
    a1 = Entry(root,width=20)
    L2 = Label(root, text="加密:",width=10)
    a2 = Entry(root,width=20)
    b = Button(root,text='浏览',command=function2,width=10)
    c = Button(root,text='加密',command=function3,width=10)
    L3 = Label(root, text="解密:",width=10)
    a3 = Entry(root,width=20)
    d = Button(root,text='浏览',command=function1,width=10)
    e = Button(root,text='解密',command=function4,width=10)
    bar1 = tkinter.ttk.Progressbar(root,length = 400,mode='indeterminate')
    L1.grid(row=0,column=0)
    a1.grid(row=0,column=1)  # 将小部件放置到主窗口中
    b.grid(row=1,column=2)
    c.grid(row=1,column=3)
    d.grid(row=2,column=2)
    e.grid(row=2,column=3)
    L2.grid(row=1,column=0)
    L3.grid(row=2,column=0)
    a2.grid(row=1,column=1)
    a3.grid(row=2,column=1)
    bar1.grid(row=3,column=0,columnspan=4)
    root.mainloop()  # 进入消息循环