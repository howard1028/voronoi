 #      $LAN=python$ 
 # M103040072 吳浩宇 Howard Wu
 # https://github.com/howard1028/voronoi_diagram


from glob import glob
import tkinter as tk
from tkinter.constants import *
from tkinter import filedialog
import math
from operator import itemgetter
import random

window = tk.Tk()
window.title('Voronoi diagram')
window.geometry('800x650')
window.resizable(False, False)
# window.iconbitmap('icon.ico')

gravity=[] #外心
dot_list=[] 
dot_list2=[] #資料點list型態
index=0
data_dot=[] #資料點暫存
edge=[] #voronoi diagram邊 (前4:邊，後4:兩個點)
edge2=[] #排序過的邊
# e_point=[] #形成voronoi diagram邊對應的點
data_dot_sorted=[] #排序過的資料點暫存
border=[] #divide後的邊界
left=[] #divide後左邊點
right=[] #divide後右邊點
CH_edge=[]


class ConvexHull:
	def __init__(self, points):
		if not points:
			self.points = [((random.randint(0,100),random.randint(0,100)) for i in range(50))]
		else:
			self.points = points
		self.hull = self.compute_convex_hull()
        
        #紀錄convex hull邊
		for i in range(len(self.hull)-1):
			CH_edge.append((self.hull[i][0],self.hull[i][1],self.hull[i+1][0],self.hull[i+1][1]))
		CH_edge.append((self.hull[0][0],self.hull[0][1],self.hull[-1][0],self.hull[-1][1]))

    #外積>0，順時針向左
	def get_cross_product(self,p1, p2, p3):
		return ((p2[0] - p1[0])*(p3[1] - p1[1])) - ((p2[1] - p1[1])*(p3[0] - p1[0]))

	def get_slope(self,p1, p2):
		if p1[0] == p2[0]:
			return float('inf')
		else:
			return 1.0*(p1[1]-p2[1])/(p1[0]-p2[0])

	def compute_convex_hull(self):
		hull = []
		self.points.sort(key=lambda x:[x[0],x[1]])
		start = self.points.pop(0)
		hull.append(start)
		self.points.sort(key=lambda p: (self.get_slope(p,start), -p[1],p[0]))

		for pt in self.points:
			hull.append(pt)
			while len(hull) > 2 and self.get_cross_product(hull[-3],hull[-2],hull[-1]) < 0: #外積<0，順時針向右
				hull.pop(-2)
		return hull
    

#已知兩點求直線一般式
def GeneralEquation(x1,y1,x2,y2):
    # 一般式 Ax+By+C=0
    A=y2-y1
    B=x1-x2
    C=x2*y1-x1*y2 
    return A,B,C

#求兩點之間中垂線一般式
def medLine(x1,y1,x2,y2):
    A = 2*(x2-x1)
    B = 2*(y2-y1)
    C = x1**2-x2**2+y1**2-y2**2
    return A,B,C

#求兩線交點by四個點
def GetIntersectPointofLines(x1,y1,x2,y2,x3,y3,x4,y4):
    A1,B1,C1 = GeneralEquation(x1,y1,x2,y2)
    A2,B2,C2 = GeneralEquation(x3,y3,x4,y4)
    m=A1*B2-A2*B1
    if m==0:
        print("無交點")
    else:
        x=(C2*B1-C1*B2)/m
        y=(C1*A2-C2*A1)/m
    return x,y

#兩線交點by方程式
def intersection(A1,B1,C1,A2,B2,C2):
    if A1*B2==A2*B1:
        return float('inf'),float('inf')
    else:
        x,y = (C2*B1-C1*B2)/(A1*B2-A2*B1),(C1*A2-C2*A1)/(A1*B2-A2*B1)
        return x,y

#斜率
def slope(x1,y1,x2,y2):
    if(x1==x2):
        return 100000
    else:
        return (y2-y1)/(x2-x1)

#兩點畫中垂線
def draw_medLine(x1,y1,x2,y2):
    x_mid,y_mid = (x1+x2)/2,(y1+y2)/2
    
    if ((x1>x2 and y1>y2) or (x1<x2 and y1<y2)): #左上右下
        A1,B1,C1=medLine(x1,y1,x2,y2)
        A2,B2,C2=1,0,0
        xb1,yb1 = intersection(A1,B1,C1,A2,B2,C2)
        cv.create_line(x_mid,y_mid,xb1,yb1)

        A2,B2,C2=0,1,0
        xb2,yb2 = intersection(A1,B1,C1,A2,B2,C2)
        cv.create_line(x_mid,y_mid,xb2,yb2)
        edge.append((xb1,yb1,xb2,yb2,x1,y1,x2,y2))

    elif ((x1>x2 and y1<y2) or (x1<x2 and y1>y2)): #左下右上
        A1,B1,C1=medLine(x1,y1,x2,y2)
        A2,B2,C2=1,0,0
        xb1,yb1 = intersection(A1,B1,C1,A2,B2,C2)
        cv.create_line(x_mid,y_mid,xb1,yb1)

        A2,B2,C2=0,1,-600
        xb2,yb2 = intersection(A1,B1,C1,A2,B2,C2)
        cv.create_line(x_mid,y_mid,xb2,yb2)
        edge.append((xb1,yb1,xb2,yb2,x1,y1,x2,y2))

    elif ((x1>x2 and y1==y2) or (x1<x2 and y1==y2)): #同一橫線

        cv.create_line(x_mid,y_mid,x_mid,0)
        cv.create_line(x_mid,y_mid,x_mid,600)
        edge.append((x_mid,0,x_mid,600,x1,y1,x2,y2))

    elif ((x1==x2 and y1>y2) or (x1==x2 and y1<y2)): #同一直線

        cv.create_line(x_mid,y_mid,0,y_mid)
        cv.create_line(x_mid,y_mid,600,y_mid)
        edge.append((0,y_mid,600,y_mid,x1,y1,x2,y2))


#(x3,y3)如果在(x1,y1)和(x2,y2)的連線上方(圖下方)則>0
def which_side(x1,y1,x2,y2,x3,y3): 
    A,B,C=GeneralEquation(x1,y1,x2,y2)
    return A*x3+B*y3+C

#三點畫中垂線2
def draw_medLine2(x1,y1,x2,y2,x3,y3):
    if(slope(x1,y1,x2,y2) != slope(x1,y1,x3,y3)): #斜率相同=>共線
        if not((x1==x2 and x2==x3)or(y1==y2 and y2==y3)): #不三點共線才有外心
            A1,B1,C1=medLine(x3,y3,x2,y2)
            A2,B2,C2=medLine(x1,y1,x3,y3)
            A3,B3,C3=medLine(x1,y1,x2,y2)
            x,y = intersection(A1,B1,C1,A2,B2,C2) #x,y:外心


            x_mid,y_mid=(x2+x3)/2,(y2+y3)/2 #中點
            if(slope(x2,y2,x3,y3)==0):  #水平點
                xb1,yb1=x_mid,0
                xb2,yb2=x_mid,600
            else:
                A,B,C=1,0,0
                xb1,yb1 = intersection(A1,B1,C1,A,B,C) #和xy軸左上交點
                A,B,C=1,0,-600
                xb2,yb2 = intersection(A1,B1,C1,A,B,C) #和xy軸右下交點

            if((x-x_mid)*(xb1-x_mid)>0 or (y-y_mid)*(yb1-y_mid)>0): #中點到外心和中點到左上交點同向
                if(which_side(x3,y3,x2,y2,x1,y1)*which_side(x3,y3,x2,y2,x,y)>0): #外心和點在同一側
                    cv.create_line(x,y,xb2,yb2)
                    edge.append((x,y,xb2,yb2,x2,y2,x3,y3))
                else:   
                    cv.create_line(x,y,xb1,yb1)
                    edge.append((x,y,xb1,yb1,x2,y2,x3,y3))
            elif ((x-x_mid)*(xb1-x_mid)<0 or (y-y_mid)*(yb1-y_mid)<0):   #反向
                if(which_side(x3,y3,x2,y2,x1,y1)*which_side(x3,y3,x2,y2,x,y)>0): #外心和點在同一側
                    cv.create_line(x,y,xb1,yb1)
                    edge.append((x,y,xb1,yb1,x2,y2,x3,y3))
                else:   
                    cv.create_line(x,y,xb2,yb2)
                    edge.append((x,y,xb2,yb2,x2,y2,x3,y3))
            else:   #外心在線上
                if(which_side(x3,y3,x2,y2,x1,y1)*which_side(x3,y3,x2,y2,xb2,yb2)>0): #點和右下交點在同側，則畫另一邊
                    cv.create_line(x,y,xb1,yb1)
                    edge.append((x,y,xb1,yb1,x2,y2,x3,y3))
                else:   
                    cv.create_line(x,y,xb2,yb2)
                    edge.append((x,y,xb2,yb2,x2,y2,x3,y3))



            x_mid,y_mid=(x1+x3)/2,(y1+y3)/2 #中點
            if(slope(x1,y1,x3,y3)==0):  #水平點
                xb1,yb1=x_mid,0
                xb2,yb2=x_mid,600
            else:
                A,B,C=1,0,0
                xb1,yb1 = intersection(A2,B2,C2,A,B,C) #和xy軸左上交點
                A,B,C=1,0,-600
                xb2,yb2 = intersection(A2,B2,C2,A,B,C) #和xy軸右下交點

            if((x-x_mid)*(xb1-x_mid)>0 or (y-y_mid)*(yb1-y_mid)>0): #中點到外心和中點到左上交點同向
                if(which_side(x3,y3,x1,y1,x2,y2)*which_side(x3,y3,x1,y1,x,y)>0): #外心和點在同一側
                    cv.create_line(x,y,xb2,yb2)
                    edge.append((x,y,xb2,yb2,x1,y1,x3,y3))
                else:   
                    cv.create_line(x,y,xb1,yb1)
                    edge.append((x,y,xb1,yb1,x1,y1,x3,y3))
            elif ((x-x_mid)*(xb1-x_mid)<0 or (y-y_mid)*(yb1-y_mid)<0):   #反向
                if(which_side(x3,y3,x1,y1,x2,y2)*which_side(x3,y3,x1,y1,x,y)>0): #外心和點在同一側
                    cv.create_line(x,y,xb1,yb1)
                    edge.append((x,y,xb1,yb1,x1,y1,x3,y3))
                else:   
                    cv.create_line(x,y,xb2,yb2)
                    edge.append((x,y,xb2,yb2,x1,y1,x3,y3))
            else:   #外心在線上
                if(which_side(x3,y3,x1,y1,x2,y2)*which_side(x3,y3,x1,y1,xb2,yb2)>0): #點和右下交點在同側，則畫另一邊
                    cv.create_line(x,y,xb1,yb1)
                    edge.append((x,y,xb1,yb1,x1,y1,x3,y3))
                else:   
                    cv.create_line(x,y,xb2,yb2)
                    edge.append((x,y,xb2,yb2,x1,y1,x3,y3))



            x_mid,y_mid=(x1+x2)/2,(y1+y2)/2 #中點
            if(slope(x1,y1,x2,y2)==0):  #水平點
                xb1,yb1=x_mid,0
                xb2,yb2=x_mid,600
            else:
                A,B,C=1,0,0
                xb1,yb1 = intersection(A3,B3,C3,A,B,C) #和xy軸左上交點
                A,B,C=1,0,-600
                xb2,yb2 = intersection(A3,B3,C3,A,B,C) #和xy軸右下交點

            if((x-x_mid)*(xb1-x_mid)>0 or (y-y_mid)*(yb1-y_mid)>0): #中點到外心和中點到左上交點同向
                if(which_side(x2,y2,x1,y1,x3,y3)*which_side(x2,y2,x1,y1,x,y)>0): #外心和點在同一側
                    cv.create_line(x,y,xb2,yb2)
                    edge.append((x,y,xb2,yb2,x1,y1,x2,y2))
                else:   
                    cv.create_line(x,y,xb1,yb1)
                    edge.append((x,y,xb1,yb1,x1,y1,x2,y2))
            elif ((x-x_mid)*(xb1-x_mid)<0 or (y-y_mid)*(yb1-y_mid)<0):   #反向
                if(which_side(x2,y2,x1,y1,x3,y3)*which_side(x2,y2,x1,y1,x,y)>0): #外心和點在同一側
                    cv.create_line(x,y,xb1,yb1)
                    edge.append((x,y,xb1,yb1,x1,y1,x2,y2))
                else:   
                    cv.create_line(x,y,xb2,yb2)
                    edge.append((x,y,xb2,yb2,x1,y1,x2,y2))
            else:   #外心在線上
                
                if(which_side(x2,y2,x1,y1,x3,y3)*which_side(x2,y2,x1,y1,xb2,yb2)>0): #點和右下交點在同側，則畫另一邊
                    cv.create_line(x,y,xb1,yb1)
                    edge.append((x,y,xb1,yb1,x1,y1,x2,y2))
                else:   
                    cv.create_line(x,y,xb2,yb2)
                    edge.append((x,y,xb2,yb2,x1,y1,x2,y2))


#(x1,y1)和(x2,y2)邊check字典編排序
def check_and_SWAP(x1,y1,x2,y2):
    if(x1>x2):
        temp_x=x1
        temp_y=y1
        x1=x2
        y1=y2
        x2=temp_x
        y2=temp_y
    elif(x1==x2):
        if(y1>y2):
            temp_x=x1
            temp_y=y1
            x1=x2
            y1=y2
            x2=temp_x
            y2=temp_y
    return x1,y1,x2,y2

#畫外心
def draw_gravity(x1,y1,x2,y2,x3,y3):
    if((slope(x1,y1,x2,y2) != slope(x1,y1,x3,y3)) and (slope(x1,y1,x2,y2) != slope(x2,y2,x3,y3)) and (slope(x3,y3,x2,y2) != slope(x1,y1,x3,y3))): #斜率相同=>共線
        if not((x1==x2 and x2==x3)or(y1==y2 and y2==y3)): #不三點共線才有外心
            A1,B1,C1=medLine(x1,y1,x2,y2)
            A2,B2,C2=medLine(x1,y1,x3,y3)
            x,y = intersection(A1,B1,C1,A2,B2,C2)
            # gravity.append((x,y))
            x1 , y1 = (x-2),(y-2)
            x2 , y2 = (x+2),(y+2)
            cv.create_oval(x1,y1,x2,y2,fill='green')

def clear():
    cv.delete("all")
    print("\n")

    data_dot_sorted.clear()
    data_dot.clear()
    edge.clear()
    edge2.clear()
    # left_temp.clear()
    # right_temp.clear()
    left.clear()
    right.clear()


def click(event):
    x1 , y1 = (event.x-2),(event.y-2)
    x2 , y2 = (event.x+2),(event.y+2)
    cv.create_oval(x1,y1,x2,y2,fill='red')
    
    global data_dot
    data_dot.append((event.x,event.y))
    # global data_dot_sorted
    # data_dot_sorted = sorted(data_dot,key = itemgetter(0,1))

    print(event.x,event.y)


def draw_line():
    global data_dot_sorted
    data_dot_sorted = sorted(data_dot,key = itemgetter(0,1))
        
    #畫線    
    drawline2(data_dot_sorted)

    #畫外心  
    if(len(data_dot)>2):
        draw_gravity(data_dot_sorted[0][0],data_dot_sorted[0][1],data_dot_sorted[1][0],data_dot_sorted[1][1],data_dot_sorted[2][0],data_dot_sorted[2][1])

    #點輸入檔案
    path = "output.txt"
    f = open(path, 'w')
    for i in range(len(data_dot_sorted)):
        print(f"P {data_dot_sorted[i][0]} {data_dot_sorted[i][1]}", file=f)
  
    #邊輸入檔案
    global edge2
    edge3=[]
    f = open(path, 'a')
    for i in range(len(edge)):
        edge3.append((check_and_SWAP(edge[i][0],edge[i][1],edge[i][2],edge[i][3])))

    edge2 = sorted(edge3,key = itemgetter(0,1,2,3))
    for i in range(len(edge)):
        print(f"E {round(edge2[i][0])} {round(edge2[i][1])} {round(edge2[i][2])} {round(edge2[i][3])}", file=f)    

    f.close()    
    
    data_dot.clear()
    data_dot_sorted.clear()
    edge.clear()
    edge2.clear()

#畫中垂線
def drawline2(temp_list):

    if(len(temp_list)<2):    
        cv.delete("all")
        data_dot.clear()
        temp_list.clear()
        print("Pleae retry.\n")

    elif(len(temp_list)<=2): #兩點一條中垂線
        draw_medLine(temp_list[0][0],temp_list[0][1],temp_list[1][0],temp_list[1][1])   

    elif((temp_list[0][0],temp_list[0][1])==(temp_list[1][0],temp_list[1][1])): #三點排好後，前兩點在同一點，變兩點一條中垂線
        draw_medLine(temp_list[0][0],temp_list[0][1],temp_list[2][0],temp_list[2][1])   

    elif((temp_list[2][0],temp_list[2][1])==(temp_list[1][0],temp_list[1][1])): #三點排好後，後兩點在同一點，變兩點一條中垂線
        draw_medLine(temp_list[0][0],temp_list[0][1],temp_list[1][0],temp_list[1][1])   

    elif(slope(temp_list[0][0],temp_list[0][1],temp_list[1][0],temp_list[1][1]) == slope(temp_list[1][0],temp_list[1][1],temp_list[2][0],temp_list[2][1])): #斜率相同，中垂線只有兩條
        draw_medLine(temp_list[0][0],temp_list[0][1],temp_list[1][0],temp_list[1][1])    
        draw_medLine(temp_list[1][0],temp_list[1][1],temp_list[2][0],temp_list[2][1])

    else: #三角形三條中垂線
        draw_medLine2(temp_list[0][0],temp_list[0][1],temp_list[1][0],temp_list[1][1],temp_list[2][0],temp_list[2][1])        
        

def read_data():
    dot_list.clear()
    dot_list2.clear()    
    global index
    index=0

    file_path = filedialog.askopenfilename()
    file = open(file_path, "r", encoding='utf-8')

    temp_P=[]
    temp_E=[]
    temp_P.clear()
    temp_E.clear()

    #讀測資
    for line in file:
        b=line.strip()
        if (b.startswith("#") == False and len(b)!=0) :
            if (b.startswith("P") == True) :
                temp=b.split()
                temp_P.append(((int(temp[1])),int(temp[2])))
            elif(b.startswith("E") == True):
                temp=b.split()
                temp_E.append((int(temp[1]),int(temp[2])))
                temp_E.append((int(temp[3]),int(temp[4])))
            else:
                dot_list.append(b.split())
        #讀到0，後面都不要
        elif ((b.startswith("0") == True) and (len(b)==1)) :
            break
                
    #印測資
    for i in range(len(dot_list)):
        if (len(dot_list[i])==1):
            dot_list2.append(int(dot_list[i][0]))
        else:
            dot_list2.append((int(dot_list[i][0]),int(dot_list[i][1])))
    print("dot_list2=",dot_list2)

    #印output檔
    print("P:",temp_P)
    print("E:",temp_E)
    for i in range(len(temp_P)):
        x1 , y1 = (temp_P[i][0]-2),(temp_P[i][1]-2)
        x2 , y2 = (temp_P[i][0]+2),(temp_P[i][1]+2)
        cv.create_oval(x1,y1,x2,y2,fill='red')
    for i in range(0,len(temp_E),2):
        cv.create_line(temp_E[i][0],temp_E[i][1],temp_E[i+1][0],temp_E[i+1][1])

    print("read successfully!\n")
    file.close()


#畫convex hull
def draw_Convexhull(temp_list):
    CH_edge.clear()
    
    h = ConvexHull(temp_list)
    print("Convex_hull=",h.hull)
    for i in range(len(h.hull)-1):
        cv.create_line(h.hull[i][0],h.hull[i][1],h.hull[i+1][0],h.hull[i+1][1],fill="blue",tag="CH")
    cv.create_line(h.hull[0][0],h.hull[0][1],h.hull[-1][0],h.hull[-1][1],fill="blue",tag="CH")

    print("CH_edge=",CH_edge)
    print("\n")

#整理資料
def print_data():
    cv.delete("all")
    data_dot.clear()
    global index
    if (dot_list2[index]!=0):
        if(index!=0):
            index+=1
        temp=dot_list2[index]
        for i in range(temp):
            index+=1
            print(dot_list2[index])
            x=dot_list2[index][0]
            y=dot_list2[index][1]
            data_dot.append((x,y))
            x1 , y1 = (x-2),(y-2)
            x2 , y2 = (x+2),(y+2)
            cv.create_oval(x1,y1,x2,y2,fill='red')
    print("\n")

#step by step
def next_step():
    if (len(data_dot) <= 3):
        draw_line()
    else:
        global data_dot_sorted
        global left
        global right
        data_dot_sorted = sorted(data_dot,key = itemgetter(0,1))

        divide(data_dot_sorted)
        # draw_Convexhull(data_dot_sorted)
        continue_button.wait_variable(var) #wait

        UL,UR,DL,DR=tangent_line(left,right)
        cv.create_line(UL[0],UL[1],UR[0],UR[1],fill="green") 
        print("upperbound=",UL,UR)
        cv.create_line(DL[0],DL[1],DR[0],DR[1],fill="green") 
        print("lowerbound=",DL,DR)

        # draw_Convexhull(left+right)
        hyperplane(UL[0],UL[1],UR[0],UR[1],DL[0],DL[1],DR[0],DR[1])




#divide成左右兩邊
def divide(temp_list):
    left_temp=[] 
    right_temp=[]
    all=[] #記每次left+right
    global left
    global right

    #畫中線
    if(len(temp_list)>3):
        for i in range(len(temp_list)):
            if (i<len(temp_list)/2):
                left_temp.append(temp_list[i])
            else:
                right_temp.append(temp_list[i])
        mid_x=(left_temp[-1][0]+right_temp[0][0])/2
        # cv.create_line(mid_x,0,mid_x,600 , fill="red")
        # border.append((mid_x,0,mid_x,600))

    continue_button.wait_variable(var) #wait
    

    #左遞迴
    if(len(left_temp)>3):
        divide(left_temp)
    else:
        drawline2(left_temp)
        l=ConvexHull(left_temp)
        left_t=l.hull

        continue_button.wait_variable(var) #wait
        for i in range(len(left_t)):
            # left.append(left_temp[i])
            all.append(left_t[i])
        print("left=",left_t)

        left=left_t
        left.append(left_t[0])
        # for i in range(len(left_t)):
        #     left.append(left_t[0])
        draw_Convexhull(left_t)
        
        continue_button.wait_variable(var) #wait
        
    #右遞迴
    if(len(right_temp)>3):  
        divide(right_temp)    
    else:
        drawline2(right_temp)
        r=ConvexHull(right_temp)
        right_t=r.hull

        continue_button.wait_variable(var) #wait
        for i in range(len(right_t)):
            # right.append(right_temp[i])
            all.append(right_t[i])
        print("right=",right_t)
        
        right=right_t
        right.append(right_t[0])

        draw_Convexhull(right_t)
        continue_button.wait_variable(var) #wait
    
    #merge剛divide的convex hull
    if(len(all)>0):
        all_temp=[] #暫存all
        all_temp=all+all_temp
        draw_Convexhull(all)
        # all.clear()
        continue_button.wait_variable(var) #wait
        
        # for i in range(len())
        cv.delete("CH")
        draw_Convexhull(all_temp)
        # hyperplane(left,right)


#外積>0，順時針向左
def get_cross_product(p1, p2, p3):
    return ((p2[0] - p1[0])*(p3[1] - p1[1])) - ((p2[1] - p1[1])*(p3[0] - p1[0]))


#找convex hull的切線
def tangent_line(c_list_L, c_list_R):
    L = len(c_list_L)
    R = len(c_list_R)

    # 找最左集合最靠右和右集合最靠左的點
    index_L = 0
    for i in range(L):
        if c_list_L[i][0] > c_list_L[index_L][0]:
            index_L = i
        elif c_list_L[i][0] == c_list_L[index_L][0]:
            if c_list_L[i][1] > c_list_L[index_L][1]:
                index_L = i
    index_R = 0
    for j in range(R):
        if c_list_R[j][0] < c_list_R[index_R][0]:
            index_R = j
        elif c_list_R[j][0] == c_list_R[index_R][0]:
            if c_list_R[j][1] < c_list_R[index_R][1]:
                index_R = j

    #找切線
    UL = index_L
    DL = index_L
    UR = index_R
    DR = index_R
    while True:
        i = UL
        j = UR
        while True:
            if clockwise(c_list_L[UL], c_list_R[UR%R], c_list_R[(UR+1)%R]) < 0:
                UR+=1
            else:
                UR = UR%R
                break
        while True:
            if clockwise(c_list_R[UR], c_list_L[UL%L], c_list_L[(UL-1)%L]) > 0:
                UL-=1
            else:
                UL = UL%L
                break
        if UL==i and UR==j:
            break
    while True:
        i = DL
        j = DR
        while True:
            if clockwise(c_list_L[DL], c_list_R[DR%R], c_list_R[(DR-1)%R]) > 0:
                DR-=1
            else:
                DR = DR%R
                break
        while True:
            if clockwise(c_list_R[DR], c_list_L[DL%L], c_list_L[(DL+1)%L]) < 0:
                DL+=1
            else:
                DL = DL%L
                break
        if DL==i and DR==j:
            break

    return c_list_L[UL], c_list_R[UR], c_list_L[DL], c_list_R[DR] #上左點，上右點，下左點，下右點

#畫布上順時針轉(其實真正逆時針轉)=1      
def clockwise(p0, p1, p2):
    cp = get_cross_product(p0,p1,p2)
    if cp > 0:
        return 1 
    elif cp < 0:
        return -1
    else:
        return 0

def printxy(event):
    label_xy.configure(text = f'(x, y): ({event.x}, {event.y})')

def hyperplane(x1,y1,x2,y2,x3,y3,x4,y4):
    edge_equation=[]
    edge_equation.clear()
    edge_intersection=[] #存有交到的
    edge_intersection.clear() 
    edge_inter2=[] #存一次全部交點
    edge_inter2.clear()
    edge_inter3=[] #存全部交點
    # edge_inter3.clear()
    to_print=[]

    A,B,C=medLine(x1,y1,x2,y2) #上切線的垂直線一般式
    xi,yi=intersection(A,B,C,0,1,100000) #和邊界的交點

    # for i in range(len(e_point)):
    #     check_and_SWAP(e_point[i][0],e_point[i][1],e_point[i][2],e_point[i][3])
    for i in range(len(edge)):
        edge[i] = list(map(int,edge[i]))
    print("edge=",edge)

    #存edge方程式
    for i in range(len(edge)):
        A1,B1,C1=GeneralEquation(edge[i][0],edge[i][1],edge[i][2],edge[i][3])
        edge_equation.append((A1,B1,C1))
    # print("edge equation=",edge_equation)

    #存edge交點，並判斷是在線段上還是線段延伸上
    for i in range(len(edge)):
        x,y=intersection(A,B,C,edge_equation[i][0],edge_equation[i][1],edge_equation[i][2])
        edge_inter2.append((x,y))
        if (x-edge[i][0])*(x-edge[i][2])<0 and (y-edge[i][1])*(y-edge[i][3])<0: #邊的兩點和交點是反向，則真的有交到
            edge_intersection.append((x,y))
    for i in range(len(edge_inter2)):
        edge_inter2[i] = list(map(int,edge_inter2[i]))
    for i in range(len(edge_intersection)):
        edge_intersection[i] = list(map(int,edge_intersection[i]))
    print("edge intersection=",edge_intersection)

    #印出第一條hyperplane
    index=0
    temp=100000
    #找最上面交點的
    for i in range(len(edge_intersection)):
        if edge_intersection[i][1]>0 and edge_intersection[i][1]<temp:
            temp=edge_intersection[i][1]
            for j in range(len(edge_inter2)):
                if edge_inter2[j]==edge_intersection[i]:
                    index=j
    print("top=",(edge_inter2[index][0],edge_inter2[index][1]))
    p1x,p1y,p2x,p2y = xi,yi,edge_inter2[index][0],edge_inter2[index][1]
    cv.create_line(p1x,p1y,p2x,p2y,fill="red")
    edge_inter3.append((xi,yi))
    edge_inter3.append((edge_inter2[index][0],edge_inter2[index][1]))


    print("(x1,y1,x2,y2)=",(x1,y1,x2,y2))
    print("edge[index]=",edge[index])
    
    # #new_e:下一個要畫中垂線的兩點
    if edge[index][4]-x1<0.05 and edge[index][5]-y1<0.05:
        new_e=(x2,y2,edge[index][6],edge[index][7])

    elif edge[index][4]-x2<0.05 and edge[index][5]-y2<0.05:
        new_e=(x1,y1,edge[index][6],edge[index][7])
        
    elif edge[index][6]-x1<0.05 and edge[index][7]-y1<0.05:
        new_e=(x2,y2,edge[index][4],edge[index][5])

    elif edge[index][6]-x2<0.05 and edge[index][7]-y2<0.05:
        new_e=(x1,y1,edge[index][4],edge[index][5])
        
    A,B,C=medLine(new_e[0],new_e[1],new_e[2],new_e[3])
    print("new_2=",new_e)
    continue_button.wait_variable(var) #wait


    while True:
        print("\n")
        #2
        edge_equation.clear()
        edge_intersection.clear() 
        edge_inter2.clear()

        #存edge方程式
        for i in range(len(edge)):
            A1,B1,C1=GeneralEquation(edge[i][0],edge[i][1],edge[i][2],edge[i][3])
            edge_equation.append((A1,B1,C1))
        #存edge交點，並判斷是在線段上還是線段延伸上
        for i in range(len(edge)):
            x,y=intersection(A,B,C,edge_equation[i][0],edge_equation[i][1],edge_equation[i][2])
            edge_inter2.append((x,y))
            if (x-edge[i][0])*(x-edge[i][2])<0 and (y-edge[i][1])*(y-edge[i][3])<0: #邊的兩點和交點是反向，則真的有交到
                edge_intersection.append((x,y))
        for i in range(len(edge_inter2)):
            edge_inter2[i] = list(map(int,edge_inter2[i]))
        for i in range(len(edge_intersection)):
            edge_intersection[i] = list(map(int,edge_intersection[i]))
        #印出第一條hyperplane
        last_index=index
        index=0
        temp=100000
        count=0
        #找最上面交點的index
        for i in range(len(edge_intersection)):
            if edge_intersection[i][1]>p2y and edge_intersection[i][1]<temp:
                temp=edge_intersection[i][1]
                count+=1
                for j in range(len(edge_inter2)):
                    if edge_inter2[j]==edge_intersection[i]:
                        index=j

        if count==0:
            print("if")
            Ad,Bd,Cd=medLine(x3,y3,x4,y4) #下切線的垂直線一般式
            xd,yd=intersection(Ad,Bd,Cd,0,1,-100000) #和邊界的交點
            cv.create_line(xd,yd,edge_inter2[last_index][0],edge_inter2[last_index][1],fill="red")
            edge_inter3.append((edge_inter2[last_index][0],edge_inter2[last_index][1]))
            edge_inter3.append((xd,yd))

            print("top=",(edge_inter2[last_index][0],edge_inter2[last_index][1]))
            
            cv.create_line(p2x,p2y,edge_inter2[last_index][0],edge_inter2[last_index][1],fill="red")
            continue_button.wait_variable(var) #wait
            break

        else:
            
            print("top=",(edge_inter2[index][0],edge_inter2[index][1]))
            
            p1x,p1y = p2x,p2y
            p2x,p2y = edge_inter2[index][0],edge_inter2[index][1]
            cv.create_line(p1x,p1y,p2x,p2y,fill="red")
            edge_inter3.append((edge_inter2[index][0],edge_inter2[index][1]))
            


            # new_e:下一個要畫中垂線的兩點
            if edge[index][4]-new_e[0]<0.05 and edge[index][5]-new_e[1]<0.05:
                new_e=(new_e[2],new_e[3],edge[index][6],edge[index][7])

            elif edge[index][4]-new_e[2]<0.05 and edge[index][5]-new_e[3]<0.05:
                new_e=(new_e[0],new_e[1],edge[index][6],edge[index][7])

            elif edge[index][6]-new_e[0]<0.05 and edge[index][7]-new_e[1]<0.05:
                new_e=(new_e[2],new_e[3],edge[index][4],edge[index][5])

            elif edge[index][6]-new_e[2]<0.05 and edge[index][7]-new_e[3]<0.05:
                new_e=(new_e[0],new_e[1],edge[index][4],edge[index][5])
                
            A,B,C=medLine(new_e[0],new_e[1],new_e[2],new_e[3])
            print("new_2=",new_e)
            continue_button.wait_variable(var) #wait


    # print("\n")
    # #3
    # edge_equation.clear()
    # edge_intersection.clear() 
    # edge_inter2.clear()

    # #存edge方程式
    # for i in range(len(edge)):
    #     A1,B1,C1=GeneralEquation(edge[i][0],edge[i][1],edge[i][2],edge[i][3])
    #     edge_equation.append((A1,B1,C1))
    # #存edge交點，並判斷是在線段上還是線段延伸上
    # for i in range(len(edge)):
    #     x,y=intersection(A,B,C,edge_equation[i][0],edge_equation[i][1],edge_equation[i][2])
    #     edge_inter2.append((x,y))
    #     if (x-edge[i][0])*(x-edge[i][2])<0 and (y-edge[i][1])*(y-edge[i][3])<0: #邊的兩點和交點是反向，則真的有交到
    #         edge_intersection.append((x,y))
    # for i in range(len(edge_inter2)):
    #     edge_inter2[i] = list(map(int,edge_inter2[i]))
    # for i in range(len(edge_intersection)):
    #     edge_intersection[i] = list(map(int,edge_intersection[i]))
    # #印出第一條hyperplane
    # last_index=index
    # index=0
    # temp=100000
    # count=0
    # #找最上面交點的index
    # for i in range(len(edge_intersection)):
    #     if edge_intersection[i][1]>p2y and edge_intersection[i][1]<temp:
    #         temp=edge_intersection[i][1]
    #         count+=1
    #         for j in range(len(edge_inter2)):
    #             if edge_inter2[j]==edge_intersection[i]:
    #                 index=j
    # if count==0:
    #     print("if")
    #     Ad,Bd,Cd=medLine(x3,y3,x4,y4) #下切線的垂直線一般式
    #     xd,yd=intersection(Ad,Bd,Cd,0,1,-100000) #和邊界的交點
    #     cv.create_line(xd,yd,edge_inter2[last_index][0],edge_inter2[last_index][1],fill="red")
    #     edge_inter3.append((edge_inter2[last_index][0],edge_inter2[last_index][1]))
    #     edge_inter3.append((xd,yd))

    #     print("top=",(edge_inter2[last_index][0],edge_inter2[last_index][1]))
        
    #     cv.create_line(p2x,p2y,edge_inter2[last_index][0],edge_inter2[last_index][1],fill="red")
    #     continue_button.wait_variable(var) #wait

    # else:
        
    #     print("top=",(edge_inter2[index][0],edge_inter2[index][1]))
        
    #     p1x,p1y = p2x,p2y
    #     p2x,p2y = edge_inter2[index][0],edge_inter2[index][1]
    #     cv.create_line(p1x,p1y,p2x,p2y,fill="red")
    #     edge_inter3.append((edge_inter2[index][0],edge_inter2[index][1]))




    
    # for i in range(len(edge_inter3)-1):
    #     print("edge_inter3=",edge_inter3)
    #     cv.create_line(edge_inter3[i][0],edge_inter3[i][1],edge_inter3[i+1][0],edge_inter3[i+1][1],fill="green")


    


cv = tk.Canvas(window,bg='white',height=600,width=600,relief=RIDGE)
cv.pack(anchor='nw')

#clear按鈕
clear_button = tk.Button(text="clear",command=clear)
clear_button.pack(side="left")

#點擊滑鼠
cv.bind("<Button-1>" , click)

#run按鈕
run_button = tk.Button(text="draw",command=draw_line)
run_button.pack(side="left")

#讀檔
read_button = tk.Button(text="read data",command=read_data)
read_button.pack(side="left")

#印檔案
print_button = tk.Button(text="print data",command=print_data)
print_button.pack(side="left")

#全部算完，再靠continue button下一步
step_button = tk.Button(text="start",command=next_step)
step_button.pack(side="left")

#滑鼠移動時執行printxy()
label_xy = tk.Label(window, text = '(x, y): ')
label_xy.place(x = 610, y = 580)
cv.bind('<Motion>', printxy) 

#Step by step
var = tk.IntVar()
continue_button = tk.Button(window, text="Click Me for next step.", command=lambda: var.set(1))
continue_button.pack(side="left")


# print("1")
# print("waiting...")
# continue_button.wait_variable(var)
# print("2")
# print("done waiting.")

# step=0
# if(step==0):
#     step_button = tk.Button(text="next step",command=next_step)
#     step_button.pack(side="left") 
# else:
#     var = tk.IntVar()
#     step_button = tk.Button(window, text="next step", command=lambda: var.set(1))
#     step_button.pack(side="left")


window.mainloop()


############################################################################

#Credit to:
#https://www.itread01.com/articles/1476674425.html
#https://lvngd.com/blog/convex-hull-graham-scan-algorithm-python/
#https://krisonepiece.github.io/VoronoiDiagram/
#https://stackoverflow.com/questions/44790449/making-tkinter-wait-untill-button-is-pressed
#https://www.twblogs.net/a/5b7f92792b717767c6b03e55
#https://web.ntnu.edu.tw/~algo/ConvexHull.html
#https://blog.csdn.net/python1639er/article/details/115386039