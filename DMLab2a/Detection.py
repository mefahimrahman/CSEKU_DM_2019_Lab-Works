from tkinter import *
from tkinter.filedialog import askdirectory
import glob as g
import cv2 as oc
import os
import numpy as n
import xlwt
from tkinter.filedialog import askopenfilename
import xlrd


# Define the button operations
def openfile():
    global folder_path
    folder_path = askdirectory()


def save():
    print(folder_path)
    path = g.glob("E:/Academic/4-2/DM Lab/Train and test ETH 80 dataset/TrainETH80data2952/*.png")
    print(path)

    # length = path.len()
    length = 0
    for pathname in path:
        length += 1
    # print(length)

    # List creation
    cv_img = [list() for f in range(length + 1)]
    cv_img[0].append("Label")
    cv_img[0].append("Mean")
    cv_img[0].append("Median")
    cv_img[0].append("Mid Range")
    cv_img[0].append("Standard Deviation")

    i = 0
    for pathname in path:
        image_matrix = oc.imread(pathname)
        image_matrix = oc.cvtColor(image_matrix, oc.COLOR_BGR2GRAY)
        head, tail = os.path.split(pathname)
        name = ""
        for w in tail:
            if w == '0' or w == '1' or w == '2' or w == '3' or w == '4' or w == '5' or w == '6' or w == '7' or w == '8' or w == '9':
                break
            else:
                name += w

        mean_value = n.mean(image_matrix)
        median_value = n.median(image_matrix)
        min_value = n.min(image_matrix)
        max_value = n.max(image_matrix)
        mid_range = (max_value - min_value) / 2
        deviation = n.std(image_matrix)
        cv_img[i + 1].append(name)
        cv_img[i + 1].append(mean_value)
        cv_img[i + 1].append(median_value)
        cv_img[i + 1].append(mid_range)
        cv_img[i + 1].append(deviation)
        i += 1

    x = 0
    workbook = xlwt.Workbook()
    excel = workbook.add_sheet("Sheet")
    for x in range(length + 1):
        excel.write(x, 0, cv_img[x][0])
        excel.write(x, 1, cv_img[x][1])
        excel.write(x, 2, cv_img[x][2])
        excel.write(x, 3, cv_img[x][3])
        excel.write(x, 4, cv_img[x][4])
    workbook.save("outputData.xls")
    print("Data Dumped Successfully!")


def load():
    global sheet, excel_path, train_name, train_mean, train_median, train_mid, train_std_dev
    name = []
    mean_value = []
    median_value = []
    mid_value = []
    std_dev = []
    print("In Load")
    excel_path = askopenfilename()
    print(excel_path)
    wb = xlrd.open_workbook(excel_path)
    sheet = wb.sheet_by_index(0)
    print("Excel Imported")
    for i in range(sheet.nrows-1):
        temp = sheet.cell_value(i+1, 0)
        name.append(temp)
    train_name = name
    # print(name)
    for i in range(sheet.nrows-1):
        temp = sheet.cell_value(i+1, 1)
        mean_value.append(temp)
    train_mean = mean_value
    for i in range(sheet.nrows-1):
        temp = sheet.cell_value(i+1, 2)
        median_value.append(temp)
    train_median = median_value
    for i in range(sheet.nrows-1):
        temp = sheet.cell_value(i+1, 3)
        mid_value.append(temp)
    train_mid = mid_value
    for i in range(sheet.nrows-1):
        temp = sheet.cell_value(i+1, 4)
        std_dev.append(temp)
    train_std_dev = std_dev


def image_load():
    global test_image, test_mean, test_median, test_mid, test_std_dev
    test_image = askopenfilename()
    image_matrix = oc.imread(test_image)
    image_matrix = oc.cvtColor(image_matrix, oc.COLOR_BGR2GRAY)
    # Calculation
    image_matrix = n.array(image_matrix)
    test_mean = n.mean(image_matrix)
    test_median = n.median(image_matrix)
    min_value = n.min(image_matrix)
    max_value = n.max(image_matrix)
    test_mid = (max_value - min_value) / 2
    test_std_dev = n.std(image_matrix)
    print("Image Loaded")


def output():
    ctrl = 0
    while ctrl < 1:
        ed_mean = (train_mean[ctrl] - test_mean) ** 2
        ed_median = (train_median[ctrl] - test_median) ** 2
        ed_mid = (train_mid[ctrl] - test_mid) ** 2
        ed_std_dev = (train_std_dev[ctrl] - test_std_dev) ** 2
        min_ed = n.sqrt(ed_mean + ed_median + ed_mid + ed_std_dev)
        # print(min)
        ctrl += 1

        for i in range(len(train_name)):
            ed_mean = (train_mean[i] - test_mean) ** 2
            ed_median = (train_median[i] - test_median) ** 2
            ed_mid = (train_mid[i] - test_mid) ** 2
            ed_std_dev = (train_std_dev[i] - test_std_dev) ** 2
            ed = n.sqrt(ed_mean + ed_median + ed_mid + ed_std_dev)
            if ed < min_ed:
                min_ed = ed
                index = i
        print(min_ed)
        object_class = train_name[index]
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
