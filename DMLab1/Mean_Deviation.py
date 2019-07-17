import glob as g
import cv2 as oc
import os
import numpy as n
import xlwt

path = g.glob("E:/Academic/4-2/Data Warehouse and Mining/dmlab/Train and test ETH 80 dataset/TrainETH80data2952/*.png")
# print(path)

# length = path.len()
length = 0
for pathname in path:
    length += 1
# print(length)

# List creation
cv_img = [list() for f in range(length+1)]
cv_img[0].append("Label")
cv_img[0].append("Mean")
cv_img[0].append("Standard Deviation")


i = 0
for pathname in path:
    image_matrix = oc.imread(pathname)
    image_matrix = oc.cvtColor(image_matrix, oc.COLOR_BGR2GRAY)
    head, tail = os.path.split(pathname)
    name = ""
    for w in tail:
        if w == '.':
            break
        else:
            name += w

    meanvalue = n.mean(image_matrix)
    deviation = n.std(image_matrix)
    cv_img[i+1].append(name)
    cv_img[i+1].append(meanvalue)
    cv_img[i+1].append(deviation)
    i += 1


x = 0
workbook = xlwt.Workbook()
excel = workbook.add_sheet("Sheet")
for x in range(length+1):
    excel.write(x, 0, cv_img[x][0])
    excel.write(x, 1, cv_img[x][1])
    excel.write(x, 2, cv_img[x][2])
workbook.save("outputData.xls")
print("Data Dumped Successfully!")
