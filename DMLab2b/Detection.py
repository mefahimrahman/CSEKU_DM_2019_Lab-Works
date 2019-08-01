from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
import glob as g
import cv2 as oc
import numpy as n
import os
from pandas import DataFrame
import xlrd


# Define the button operations
def openfile():
    print("File Explorer opened")
    global folder_path
    folder_path = askdirectory()
    print(folder_path)


def save():
    global folder_content_length
    path = g.glob(folder_path + "/*.png")
    print(path)

    # length = path.len()
    length = 0
    for pathname in path:
        length += 1
    print(length)
    folder_content_length = length


    # List creation
    cv_img = [list() for f in range(length + 1)]

    i = 0
    for pathname in path:
        image_matrix = oc.imread(pathname)
        image_matrix = oc.cvtColor(image_matrix, oc.COLOR_BGR2GRAY)
        head, tail = os.path.split(pathname)
        # Calculation
        min_value = n.min(image_matrix)
        median_value = n.median(image_matrix)
        first_quartile = n.quantile(image_matrix, .25)
        third_quartile = n.quantile(image_matrix, .75)
        varience = n.var(image_matrix)
        max_value = n.max(image_matrix)
        cv_img[i].append(tail)
        cv_img[i].append(min_value)
        cv_img[i].append(median_value)
        cv_img[i].append(first_quartile)
        cv_img[i].append(third_quartile)
        cv_img[i].append(varience)
        cv_img[i].append(max_value)
        i += 1

    print(cv_img)

    df = DataFrame(cv_img, columns=['Label', "Min Value", 'Median', "First Quartile Q1", "Third Quartile Q2", "Varience", "Max Value"])
    export_excel = df.to_excel(r'C:\Users\Toothless\PycharmProjects\DMLab2b\export_dataframe.xlsx', index=None, header=True)
    print("Data Dumped Successfully")


def load():
    print(folder_content_length)
    global sheet, excel_path, train_name, train_min, train_median, train_q1, train_q3, train_varience, train_max
    name = []
    min_value = []
    median_value = []
    q1 = []
    q3 = []
    varience = []
    max_value = []
    print("In Load")
    excel_path = askopenfilename()
    print(excel_path)
    wb = xlrd.open_workbook(excel_path)
    sheet = wb.sheet_by_index(0)
    print("Excel Imported")
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 0)
        name.append(temp)
    train_name = name
    # print(name)
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 1)
        min_value.append(temp)
    train_min = min_value
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 2)
        median_value.append(temp)
    train_median = median_value
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 3)
        q1.append(temp)
    train_q1 = q1
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 4)
        q3.append(temp)
    train_q3 = q3
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 5)
        varience.append(temp)
    train_varience = varience
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 6)
        max_value.append(temp)
    train_max = max_value


def image_load():
    global test_image, test_min, test_median, test_q1, test_q3, test_varience, test_max
    print(train_name)
    print(train_min)
    print(train_median)
    print(train_q1)
    print(train_q3)
    print(train_varience)
    print(train_max)
    print('Image Load')
    test_image = askopenfilename()
    image_matrix = oc.imread(test_image)
    image_matrix = oc.cvtColor(image_matrix, oc.COLOR_BGR2GRAY)

    # Calculation
    image_matrix = n.array(image_matrix)
    test_min = n.min(image_matrix)
    test_median = n.median(image_matrix)
    test_q1 = n.quantile(image_matrix, .25)
    test_q3 = n.quantile(image_matrix, .75)
    test_varience = n.var(image_matrix)
    test_max = n.max(image_matrix)

    # print(test_min)
    # print(test_median)
    # print(test_q1)
    # print(test_q3)
    # print(test_varience)
    # print(test_max)


def output():
    edlist = [list() for f in range(folder_content_length)]

    for i in range(len(train_name)):
        ed_min = (train_min[i] - test_min) ** 2
        ed_median = (train_median[i] - test_median) ** 2
        ed_q1 = (train_q1[i] - test_q1) ** 2
        ed_q3 = (train_q3[i] - test_q3) ** 2
        ed_varience = (train_varience[i] - test_varience) ** 2
        ed_max = (train_max[i] - test_max) ** 2
        ed = n.sqrt(ed_min + ed_median + ed_q1 + ed_q3 + ed_varience + ed_max)
        edlist[i].append(ed)
        edlist[i].append(train_name[i])

    edlist.sort()
    # print(edlist)
    # print(len(edlist))

    res = edlist[:10]
    for i in res:
        print(i)
    # print(len(res))

    object_class = 'Done'
    message = "Test Object Type: " + object_class
    label.configure(text=message)


# GUI
root = Tk()
root.title("Object Detection")
root.geometry("1080x720")

frame1 = Frame(root, padx=50, pady=50)
frame1.pack(side='top')
label = Label(frame1, text='result:', padx=100, pady=100)
label.grid(row=5, column=10)
frame2 = Frame(root, padx=20, pady=50)
frame2.pack(side='bottom')


b1 = Button(frame2, text="Load Train Images", command=openfile, padx=15, pady=15)
b1.pack(side='left')
b2 = Button(frame2, text="Save the Features", command=save, padx=15, pady=15)
b2.pack(side='left')
b3 = Button(frame2, text="Load Excel", command=load,  padx=15, pady=15)
b3.pack(side='left')
b4 = Button(frame2, text="Load Image", command=image_load, padx=15, pady=15)
b4.pack(side='left')
b5 = Button(frame2, text="Result", command=output,  padx=15, pady=15)
b5.pack(side='left')

root.mainloop()
