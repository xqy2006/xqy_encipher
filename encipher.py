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
import tkinter.scrolledtext
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
def realcode1(dir,mima,mima_len,i,num,q,thnum):
    file_stats = os.stat(dir)
    max = int(file_stats.st_size)
    while True:
        if i+1024>=(min(max,10000000)*num)//thnum:
            q.put('done')
            break
        a=read(dir,i,mima_len//2+2)
        abc = str(hex(int(a,16)^mima))[2:]
        while len(abc) < len(a):
            abc = '0' + abc
        if len(abc) == len(a):
            write(abc,dir,i)
        i += 1024
        q.put(1024)

def coding(dir,mima,mima_len):
    file_stats = os.stat(dir)
    max = int(file_stats.st_size)
    q = Queue()
    threads = []
    thnum = int(ath.get())
    for i in range(int(ath.get())):
        threads.append(multiprocessing.Process(target=realcode1, args=(dir,mima,mima_len,(min(max,10000000)*i)//int(ath.get()),i+1,q,thnum,)))
    for i in threads:
        i.start()
    times = 0
    while True:
        stepnum = q.get()
        if stepnum=='done':
            times += 1
            if times == int(ath.get()):
                break
        else:
            bar1.step(stepnum)
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
    global file2
    OpenFile = Tk()   #创建新窗口
    OpenFile.withdraw()
    file_path2 = filedialog.askopenfilenames(filetypes=[('XUQINYANG FILES','.xqy')]) # 获取路径
    a3.delete(0, 'end')
    a3.insert(INSERT, file_path2)
    file2 = file_path2
def function2():
    global file1
    OpenFile = Tk()   #创建新窗口
    OpenFile.withdraw()
    file_path1 = filedialog.askopenfilenames() # 获取路径
    a2.delete(0, 'end')
    a2.insert(INSERT, file_path1)
    file1 = file_path1
def function3():#jiami
    global file1,log
    mima = a1.get()
    newmima = ''
    for i in mima:
        newmima = newmima+str(ord(i))
    mima = int(newmima)
    mima_len = len(str(mima))
    cha = 1024
    save_dir = filedialog.askdirectory(initialdir=file1[0][:file1[0].rfind('/')])
    for everypath in file1:
        if save_dir!='':
            log.configure(state='normal')
            log.insert(INSERT, '正在加密'+save_dir+everypath[everypath.rfind('/'):])
            log.configure(state='disabled')
            file_stats = os.stat(everypath)
            bar1['maximum'] = min(int(file_stats.st_size),10000000) + 1
            jiami(everypath,save_dir+everypath[everypath.rfind('/'):]+'.xqy',mima,mima_len)
            bar1['value'] = 0
            log.configure(state='normal')
            log.insert(INSERT, '  完成！' + '\n')
            log.configure(state='disabled')
    log.configure(state='normal')
    log.insert(INSERT, '加密完成！所有文件均输出至' +save_dir+ '\n')
    log.configure(state='disabled')
def function4():#jiemi
    global file2,log
    mima = a1.get()
    newmima = ''
    for i in mima:
        newmima = newmima+str(ord(i))
    mima = int(newmima)
    mima_len = len(str(mima))
    cha = 1024
    save_dir = filedialog.askdirectory(initialdir=file2[0][:file2[0].rfind('/')])
    for everypath in file2:
        if save_dir!='':
            log.configure(state='normal')
            log.insert(INSERT, '正在解密' + save_dir + everypath[everypath.rfind('/'):])
            log.configure(state='disabled')
            file_stats = os.stat(everypath)
            bar1['maximum'] = min(int(file_stats.st_size),10000000) + 1
            jiemi(everypath,save_dir+everypath[everypath.rfind('/'):everypath.rfind('.')],mima,mima_len)
            bar1['value'] = 0
    log.configure(state='normal')
    log.insert(INSERT, '加密完成！所有文件均输出至' + save_dir + '\n')
    log.configure(state='disabled')
if __name__ == '__main__':
    multiprocessing.freeze_support()

    root = Tk()
    root.title('xqy_encipher')
    root.minsize(410, 330)
    root.maxsize(410, 330)
    L1 = Label(root, text="密码:",width=10)
    a1 = Entry(root,width=20)
    Lth = Label(root, text="使用进程数:",width=10)
    ath = Entry(root,width=20)
    L2 = Label(root, text="加密:",width=10)
    a2 = Entry(root,width=20)
    b = Button(root,text='浏览',command=function2,width=10)
    c = Button(root,text='加密',command=function3,width=10)
    L3 = Label(root, text="解密:",width=10)
    a3 = Entry(root,width=20)
    d = Button(root,text='浏览',command=function1,width=10)
    e = Button(root,text='解密',command=function4,width=10)
    bar1 = tkinter.ttk.Progressbar(root,length = 410)
    log = tkinter.scrolledtext.ScrolledText(root, width=55, height=15)
    L1.grid(row=0,column=0)
    a1.grid(row=0,column=1)  # 将小部件放置到主窗口中
    Lth.grid(row=1, column=0)
    ath.grid(row=1, column=1)
    b.grid(row=2,column=2)
    c.grid(row=2,column=3)
    d.grid(row=3,column=2)
    e.grid(row=3,column=3)
    L2.grid(row=2,column=0)
    L3.grid(row=3,column=0)
    a2.grid(row=2,column=1)
    a3.grid(row=3,column=1)
    bar1.grid(row=4,column=0,columnspan=4)
    log.grid(row=5,column=0,columnspan=4)
    ath.insert(INSERT, 4)
    log.configure(state='disabled')
    root.mainloop()  # 进入消息循环