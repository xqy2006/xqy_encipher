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
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
def read(dir,address,length,f):
    f.seek(address, 0)
    result = f.read(length)
    result = b2a_hex(result)
    result = bytes.decode(result)
    return result
def write(write_bytes,dir,address,f):
    try:
        write_bytes = bytes().fromhex(write_bytes)
    except:
        print(write_bytes)
    f.seek(address, 0)
    result=f.write(write_bytes)
    return result
def realcode1(dir,mima,mima_len,i,num,q,thnum,flagmi):
    def jiamihanshu(mima, readdata, iv):
        secret = mima  # 由用户输入的16位或24位或32位长的初始密码字符串

        # 密钥处理,16的整数倍
        def add_to_16(text):
            while len(text) % 16 != 0:
                text += '\0'
            return (text)

        secret = add_to_16(secret)
        iv = bytes().fromhex(iv)
        cipher = AES.new(secret.encode('utf-8'), AES.MODE_CBC, iv)
        data = readdata  # 16beishu
        data = bytes().fromhex(data)
        encrypt_data = cipher.encrypt(data)  # 输入需要加密的字符串，注意字符串长度要是16的倍数。16,32,48..
        encrypt_data = bytes.decode(b2a_hex(encrypt_data))
        return encrypt_data

    def jiemihanshu(mima, readdata, iv):
        secret = mima  # 由用户输入的16位或24位或32位长的初始密码字符串

        def add_to_16(text):
            while len(text) % 16 != 0:
                text += '\0'
            return (text)

        secret = add_to_16(secret)
        iv = bytes().fromhex(iv)  # 随机获取16位变量
        encrypt_data = bytes().fromhex(readdata)
        cipher = AES.new(secret.encode('utf-8'), AES.MODE_CBC, iv)
        decrypt_data = cipher.decrypt(encrypt_data)
        decrypt_data = bytes.decode(b2a_hex(decrypt_data))
        return decrypt_data

    f = open(dir, "rb+")
    file_stats = os.stat(dir)
    max = int(file_stats.st_size)
    while True:
        if i+1024>=(min(max,10000000)*num)//thnum:
            q.put('done')
            f.close()
            break
        a = read(dir, i,32, f)
        if flagmi == 1:
            abc = jiamihanshu(mima,a,"20060815200608152006081520060815")
        if flagmi == 2:
            abc = jiemihanshu(mima,a,"20060815200608152006081520060815")
        write(abc,dir,i,f)
        i += 1024
        q.put(1024)

def coding(dir,mima,mima_len,flagmi):
    file_stats = os.stat(dir)
    max = int(file_stats.st_size)
    q = Queue()
    threads = []
    thnum = int(ath.get())
    for i in range(int(ath.get())):
        threads.append(multiprocessing.Process(target=realcode1, args=(dir,mima,mima_len,(min(max,10000000)*i)//int(ath.get()),i+1,q,thnum,flagmi,)))
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
    coding(save_dir,mima,mima_len,1)
def jiemi(dir,save_dir,mima,mima_len):
    shutil.copyfile(dir, save_dir)
    coding(save_dir,mima,mima_len,2)
def function1():
    global file2,singleflag
    OpenFile = Tk()   #创建新窗口
    OpenFile.withdraw()
    file_path2 = filedialog.askopenfilenames(filetypes=[('XUQINYANG FILES','.xqy')]) # 获取路径
    a3.configure(state='normal')
    a3.delete(0, 'end')
    a3.insert(INSERT, file_path2)
    a3.configure(state='disable')
    file2 = file_path2
    singleflag = 1
def function2():
    global file1,singleflag
    OpenFile = Tk()   #创建新窗口
    OpenFile.withdraw()
    file_path1 = filedialog.askopenfilenames() # 获取路径
    a2.configure(state='normal')
    a2.delete(0, 'end')
    a2.insert(INSERT, file_path1)
    a2.configure(state='disable')
    file1 = file_path1
    singleflag = 1
def functionjia():
    global file1,singleflag
    OpenFile = Tk()  # 创建新窗口
    OpenFile.withdraw()
    file_path1 = filedialog.askdirectory()
    file1 = ()
    for root1, dirs, files in os.walk(file_path1, topdown=False):
        for a in files:
            newroot = ''
            for evestr in root1:
                if evestr == '\\':
                    newroot+='/'
                else:
                    newroot+=evestr
            file1+=(newroot+'/'+a,)
    a2.configure(state='normal')
    a2.delete(0, 'end')
    a2.insert(INSERT, file_path1)
    a2.configure(state='disabled')
    singleflag = 0
def functionjie():
    global file2,singleflag
    OpenFile = Tk()  # 创建新窗口
    OpenFile.withdraw()
    file_path2 = filedialog.askdirectory()
    file2 = ()
    for root1, dirs, files in os.walk(file_path2, topdown=False):
        for a in files:
            newroot = ''
            for evestr in root1:
                if evestr == '\\':
                    newroot += '/'
                else:
                    newroot += evestr
            file2 += (newroot + '/'+a,)
    a3.configure(state='normal')
    a3.delete(0, 'end')
    a3.insert(INSERT, file_path2)
    a3.configure(state='disabled')
    singleflag = 0
def function3():#jiami
    global file1,log,singleflag
    if singleflag == 0:
        mima = a1.get()
        newmima = ''
        for i in mima:
            newmima = newmima+str(ord(i))
        mima = newmima
        mima_len = len(mima)
        cha = 1024
        save_dir = filedialog.askdirectory(initialdir=a2.get())
        print(save_dir)
        for everypath in file1:
            if save_dir!='':
                log.configure(state='normal')
                log.insert(INSERT, '正在加密'+save_dir+everypath[len(a2.get()):])
                log.configure(state='disabled')
                if not os.path.exists(save_dir+everypath[len(a2.get()):everypath.rfind('/')]):
                    os.makedirs(save_dir+everypath[len(a2.get()):everypath.rfind('/')])
                file_stats = os.stat(everypath)
                bar1['maximum'] = min(int(file_stats.st_size),10000000) + 1
                jiami(everypath,save_dir+everypath[len(a2.get()):]+'.xqy',mima,mima_len)
                bar1['value'] = 0
                log.configure(state='normal')
                log.insert(INSERT, '  完成！' + '\n')
                log.mark_set("insert", "end")
                log.see("insert")
                log.configure(state='disabled')
        log.configure(state='normal')
        log.insert(INSERT, '加密完成！所有文件均输出至' +save_dir+ '\n')
        log.configure(state='disabled')
    elif singleflag==1:
        mima = a1.get()
        newmima = ''
        for i in mima:
            newmima = newmima + str(ord(i))
        mima = newmima
        mima_len = len(mima)
        cha = 1024
        save_dir = filedialog.askdirectory(initialdir=file1[0][:file1[0].rfind('/')])
        for everypath in file1:
            if save_dir != '':
                log.configure(state='normal')
                log.insert(INSERT, '正在加密' + save_dir + everypath[everypath.rfind('/'):])
                log.configure(state='disabled')
                file_stats = os.stat(everypath)
                bar1['maximum'] = min(int(file_stats.st_size), 10000000) + 1
                jiami(everypath, save_dir + everypath[everypath.rfind('/'):] + '.xqy', mima, mima_len)
                bar1['value'] = 0
                log.configure(state='normal')
                log.insert(INSERT, '  完成！' + '\n')
                log.mark_set("insert", "end")
                log.see("insert")
                log.configure(state='disabled')
        log.configure(state='normal')
        log.insert(INSERT, '加密完成！所有文件均输出至' + save_dir + '\n')
        log.configure(state='disabled')
def function4():#jiemi
    global file2,log,singleflag
    if singleflag==0:
        mima = a1.get()
        newmima = ''
        for i in mima:
            newmima = newmima+str(ord(i))
        mima = newmima
        mima_len = len(mima)
        cha = 1024
        save_dir = filedialog.askdirectory(initialdir=a3.get())
        for everypath in file2:
            if save_dir!='':
                if everypath[everypath.rfind('.'):]=='.xqy':
                    log.configure(state='normal')
                    log.insert(INSERT, '正在解密' + save_dir + everypath[len(a3.get()):])
                    log.configure(state='disabled')
                    if not os.path.exists(save_dir + everypath[len(a3.get()):everypath.rfind('/')]):
                        os.makedirs(save_dir + everypath[len(a3.get()):everypath.rfind('/')])
                    file_stats = os.stat(everypath)
                    bar1['maximum'] = min(int(file_stats.st_size),10000000) + 1
                    jiemi(everypath,save_dir+everypath[len(a3.get()):everypath.rfind('.')],mima,mima_len)
                    log.configure(state='normal')
                    log.insert(INSERT, '  完成！' + '\n')
                    log.mark_set("insert", "end")
                    log.see("insert")
                    log.configure(state='disabled')
                    bar1['value'] = 0
        log.configure(state='normal')
        log.insert(INSERT, '解密完成！所有文件均输出至' + save_dir + '\n')
        log.configure(state='disabled')
    elif singleflag==1:
        mima = a1.get()
        newmima = ''
        for i in mima:
            newmima = newmima + str(ord(i))
        mima = newmima
        mima_len = len(mima)
        cha = 1024
        save_dir = filedialog.askdirectory(initialdir=file2[0][:file2[0].rfind('/')])
        for everypath in file2:
            if save_dir != '':
                log.configure(state='normal')
                log.insert(INSERT, '正在解密' + save_dir + everypath[everypath.rfind('/'):])
                log.configure(state='disabled')
                file_stats = os.stat(everypath)
                bar1['maximum'] = min(int(file_stats.st_size), 10000000) + 1
                jiemi(everypath, save_dir + everypath[everypath.rfind('/'):everypath.rfind('.')], mima, mima_len)
                log.configure(state='normal')
                log.insert(INSERT, '  完成！' + '\n')
                log.mark_set("insert", "end")
                log.see("insert")
                log.configure(state='disabled')
                bar1['value'] = 0
        log.configure(state='normal')
        log.insert(INSERT, '解密完成！所有文件均输出至' + save_dir + '\n')
        log.configure(state='disabled')
if __name__ == '__main__':
    multiprocessing.freeze_support()
    singleflag = 2
    root = Tk()
    root.title('xqy_encipher')
    root.minsize(510, 330)
    root.maxsize(510, 330)
    L1 = Label(root, text="密码:",width=10)
    a1 = Entry(root,width=20)
    Lth = Label(root, text="使用进程数:",width=10)
    ath = Entry(root,width=20)
    L2 = Label(root, text="加密:",width=10)
    a2 = Entry(root,width=20)
    b = Button(root,text='浏览文件',command=function2,width=10)
    b1 = Button(root,text='浏览文件夹',command=functionjia,width=10)
    c = Button(root,text='加密',command=function3,width=10)
    L3 = Label(root, text="解密:",width=10)
    a3 = Entry(root,width=20)
    d = Button(root,text='浏览文件',command=function1,width=10)
    d1 = Button(root,text='浏览文件夹',command=functionjie,width=10)
    e = Button(root,text='解密',command=function4,width=10)
    bar1 = tkinter.ttk.Progressbar(root,length = 510)
    log = tkinter.scrolledtext.ScrolledText(root, width=65, height=15)
    L1.grid(row=0,column=0)
    a1.grid(row=0,column=1)  # 将小部件放置到主窗口中
    Lth.grid(row=1, column=0)
    ath.grid(row=1, column=1)
    b.grid(row=2,column=2)
    b1.grid(row=2,column=3)
    c.grid(row=2,column=4)
    d.grid(row=3,column=2)
    d1.grid(row=3, column=3)
    e.grid(row=3,column=4)
    L2.grid(row=2,column=0)
    L3.grid(row=3,column=0)
    a2.grid(row=2,column=1)
    a3.grid(row=3,column=1)
    bar1.grid(row=4,column=0,columnspan=5)
    log.grid(row=5,column=0,columnspan=5)
    ath.insert(INSERT, 4)
    log.configure(state='disabled')
    a3.configure(state='disabled')
    a2.configure(state='disabled')
    root.mainloop()  # 进入消息循环
