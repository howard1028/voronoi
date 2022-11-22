# import random

# """
# Computes the Convex Hull with the Graham Scan algorithm
# Use:
# 	h = ConvexHull()
# 	print(h.hull)
# """

# class ConvexHull:
# 	def __init__(self, points):
# 		if not points:
# 			self.points = [((random.randint(0,100),random.randint(0,100)) for i in range(50))]
# 		else:
# 			self.points = points
# 		self.hull = self.compute_convex_hull()
    
# 	def get_cross_product(self,p1, p2, p3):
# 		return ((p2[0] - p1[0])*(p3[1] - p1[1])) - ((p2[1] - p1[1])*(p3[0] - p1[0]))

# 	def get_slope(self,p1, p2):
# 		if p1[0] == p2[0]:
# 			return float('inf')
# 		else:
# 			return 1.0*(p1[1]-p2[1])/(p1[0]-p2[0])

# 	def compute_convex_hull(self):
# 		hull = []
# 		self.points.sort(key=lambda x:[x[0],x[1]])
# 		start = self.points.pop(0)
# 		hull.append(start)
# 		self.points.sort(key=lambda p: (self.get_slope(p,start), -p[1],p[0]))
# 		for pt in self.points:
# 			hull.append(pt)
# 			while len(hull) > 2 and self.get_cross_product(hull[-3],hull[-2],hull[-1]) < 0:
# 				hull.pop(-2)
# 		return hull

# h = ConvexHull([(1,3),(2,2),(3,1)])
# print(h.hull)


# list1=[(1,1),(2,2)]
# list2=[(3,3),(4,4)]
# list=list1+list2
# # list.append(list1)
# # list.append(list2)
# print(list)

# left=(0,1)
# a=(2,4)
# left=a
# print(left)

# a=[(1,3),(2,2),(3,1)]
# for i in a:
#     print(i)


# a=[1,2,3,4,5,6]
# for i in range(3,len(a)):
#     print(i)

# a=[]
# a.append((1,2,3,4))
# a.append((5,6,7,8))
# print(a)


start= [(195, 221), (423, 228)]
l= [(206, 373), (195, 221), (82, 367)]
print(start+l)