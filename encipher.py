from tkinter import *
from tkinter import filedialog
from binascii import a2b_hex
from binascii import b2a_hex
import tkinter.messagebox
def read(dir):
    f = open(dir, "rb")
    result = f.read()
    result = b2a_hex(result)
    result = bytes.decode(result)
    return result
def write(write_bytes,dir='defult.bin'):
    write_bytes=bytes().fromhex(write_bytes)
    with open(dir, 'wb') as f:
        return f.write(write_bytes)
def coding(dir,max=10000):
    s=read(dir)

    i = 0
    while True:
        if i+1==len(s) or i+1==max:
            break
        a=int(s[i],16)
        if i != 0:
            s = s[0:i] + str(hex(a^7))[2:] + s[i + 1:]
        else:
            s = str(hex(a ^ 7))[2:] + s[i + 1:]
        i += 1
    s = s.lower()
    return s
def jiami(dir,max,save_dir):
    write(coding(dir,max),save_dir)
def jiemi(dir,max,save_dir):
    write(coding(dir,max),save_dir)
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
    max = a1.get()
    save_dir = filedialog.asksaveasfilename(initialfile=file_path1+'.xqy',filetypes=[('XUQINYANG FILES','.xqy')])
    if save_dir!='':
        jiami(file_path1,max,save_dir)
        tkinter.messagebox.showinfo('加密','加密完成，保存路径为'+save_dir)
def function4():#jiemi
    max = a1.get()
    save_dir = filedialog.asksaveasfilename(initialfile=file_path2[:file_path2.rfind('.')])
    if save_dir!='':
        jiemi(file_path2, max,save_dir)
        tkinter.messagebox.showinfo('解密','解密完成，保存路径为'+save_dir)
root = Tk()
root.title('注意密码不要设的太大，会影响加/解密效率！')
root.minsize(410, 80)
root.maxsize(410, 80)
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
a1.insert(0, '100')
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
root.mainloop()  # 进入消息循环
