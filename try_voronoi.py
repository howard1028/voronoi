# import tkinter as tk

# window = tk.Tk()
# window.title('GUI')
# window.geometry('380x400')
# window.resizable(False, False)
# # window.iconbitmap('icon.ico')

# def show():
#     password = test2.get()
#     print(password)

# test = tk.Button(text="測試", command=show)
# test.pack()

# test2 = tk.Entry(show="*")
# test2.pack()

# window.mainloop()

# list1=[]
# list1.append((1,2))
# list1.append((3,4))
# print(list1[0][1])


# #已知兩點求直線一般式
# def GeneralEquation(x1,y1,x2,y2):
#     # 一般式 Ax+By+C=0

#     A=y2-y1
#     B=x1-x2
#     C=x2*y1-x1*y2
#     return A,B,C

# print(GeneralEquation(0,0,1,1)) 

# #求兩點之間中垂線一般式
# def medLine(x1,y1,x2,y2):
#     A = 2*(x2-x1)
#     B = 2*(y2-y1)
#     C = x1**2-x2**2+y1**2-y2**2
#     return A,B,C

# print(medLine(0,2,-2,0)) 

# def GetIntersectPointofLines(x1,y1,x2,y2,x3,y3,x4,y4):

#     A1,B1,C1=GeneralEquation(x1,y1,x2,y2)
#     A2, B2, C2 = GeneralEquation(x3,y3,x4,y4)
#     m=A1*B2-A2*B1
#     if m==0:
#         print("無交點")
#     else:
#         x=(C2*B1-C1*B2)/m
#         y=(C1*A2-C2*A1)/m
#     return x,y


# from turtle import dot
# file = open("data.txt", "r")
# dot_list = file.readlines()
# for i in range(len(dot_list)):
#     print(dot_list[i].split())


# a=[]
# file = open("data2.txt", "r", encoding='utf-8')
# # a = file.readlines()
# for line in file:
#     b=line.strip()
#     if (b.startswith("#") == False) :
#         a.append(b.split())
# print(a)


# edge=[]
# temp=[]
# temp.append((1,2))
# temp.append((3,4))
# print(temp)
# for i in range(len(temp)):
#     edge.append((temp[i][0],temp[i][1]))
# print(edge)

# temp.append((1,2))
# temp.append((3,4))
# print(temp)
# for i in range(len(temp)):
#     edge.append((temp[i][0],temp[i][1]))
# print(edge)

#(x1,y1)和(x2,y2)check字典編排序
# def check_and_SWAP(x1,y1,x2,y2):
#     if(x1>x2):
#         temp_x=x1
#         temp_y=y1
#         x1=x2
#         y1=y2
#         x2=temp_x
#         y2=temp_y
#     elif(x1==x2):
#         if(y1>y2):
#             temp_x=x1
#             temp_y=y1
#             x1=x2
#             y1=y2
#             x2=temp_x
#             y2=temp_y
#     return x1,y1,x2,y2

# a=5,2,3,4
# print(check_and_SWAP(5,2,3,4))

from tkinter import filedialog
file_path = filedialog.askopenfilename()

temp_P=[]
temp_E=[]
file = open(file_path, "r", encoding='utf-8')
for line in file:
    c=line.strip()
    if (c.startswith("P") == True) :
        temp=c.split()
        temp_P.append(((int(temp[1])),int(temp[2])))
    elif(c.startswith("E") == True):
        temp=c.split()
        temp_E.append((int(temp[1]),int(temp[2])))
        temp_E.append((int(temp[3]),int(temp[4])))
print(temp_P)
print(temp_E)

