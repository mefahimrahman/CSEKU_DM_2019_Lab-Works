from tkinter.filedialog import *
import glob as g
import cv2 as oc
import os
from pandas import DataFrame
import xlrd
from skimage.feature import greycomatrix, greycoprops
import numpy as n


def openfile():
    print('Open File Button Clicked')
    global folder_path
    folder_path = askdirectory()
    print('Selected PATH = ' + folder_path)


def save():
    print('Save Button Clicked')
    global folder_content_length
    print(folder_path)
    path = g.glob(folder_path + '/*.png')
    print(path)

    length = 0
    for pathname in path:
        length += 1
    print(length)
    folder_content_length = length  # Assign length to a global variable for later uses

    # List creation
    cv_img = [list() for f in range(length + 1)]

    i = 0
    for pathname in path:
        image_matrix = oc.imread(pathname)
        image_matrix = oc.cvtColor(image_matrix, oc.COLOR_BGR2GRAY)
        glcm = greycomatrix(image_matrix, [1], [0], levels=256, symmetric=True, normed=True)
        head, tail = os.path.split(pathname)

        # Calculation
        max_probability = n.max(glcm)
        correlation = greycoprops(glcm, 'correlation')
        contrast = greycoprops(glcm, 'contrast')
        energy = greycoprops(glcm, 'energy')
        homogeneity = greycoprops(glcm, 'homogeneity')
        entropy = n.sum(glcm * n.log2(glcm + (glcm == 0)))

        cv_img[i].append(tail)
        cv_img[i].append(max_probability)
        cv_img[i].append(correlation[0][0])
        cv_img[i].append(contrast[0][0])
        cv_img[i].append(energy[0][0])
        cv_img[i].append(homogeneity[0][0])
        cv_img[i].append(entropy)

        i += 1

    df = DataFrame(cv_img, columns=['Label', "Max Probability", "Correlation", 'Contrast', "Energy", "Homogeneity",
                                    "Entropy"])
    export_excel = df.to_excel(r'C:\Users\Toothless\PycharmProjects\DMLab3b\export_dataframe.xlsx', index=None,
                               header=True)
    print("Data Dumped Successfully")


def load():
    print('Load Button Clicked')
    print(folder_content_length)
    global sheet, excel_path, train_name, train_max_probability, train_correlation, train_contrast, train_energy, \
        train_homogeneity, train_entropy
    name = []
    max_probability = []
    correlation = []
    contrast = []
    energy = []
    homogeneity = []
    entropy = []

    # open excel file
    excel_path = askopenfilename()
    print(excel_path)

    wb = xlrd.open_workbook(excel_path)
    sheet = wb.sheet_by_index(0)

    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 0)
        name.append(temp)
    train_name = name
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 1)
        max_probability.append(temp)
    train_max_probability = max_probability
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 2)
        correlation.append(temp)
    train_correlation = correlation
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 3)
        contrast.append(temp)
    train_contrast = contrast
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 4)
        energy.append(temp)
    train_energy = energy
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 5)
        homogeneity.append(temp)
    train_homogeneity = homogeneity
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 6)
        entropy.append(temp)
    train_entropy = entropy

    print(train_name)


def image_load():
    global test_image, test_max_probability, test_correlation, test_contrast, test_energy, \
        test_homogeneity, test_entropy, res

    test_image = askopenfilename()
    print('Test Image Loaded')
    image_matrix = oc.imread(test_image)
    image_matrix = oc.cvtColor(image_matrix, oc.COLOR_BGR2GRAY)
    glcm = greycomatrix(image_matrix, [1], [0], levels=256, symmetric=True, normed=True)

    # Calculation
    test_max_probability = n.max(glcm)
    test_correlation = greycoprops(glcm, 'correlation')
    test_contrast = greycoprops(glcm, 'contrast')
    test_energy = greycoprops(glcm, 'energy')
    test_homogeneity = greycoprops(glcm, 'homogeneity')
    test_entropy = n.sum(glcm*n.log2(glcm + (glcm == 0)))

    canberrea_distance = [list() for f in range(folder_content_length)]

    for item in range(len(train_name)):
        f1 = (abs(train_max_probability[item] - test_max_probability) / (abs(train_max_probability[item])
                                                                         + abs(test_max_probability)))
        f2 = (abs(train_correlation[item] - test_correlation) / (abs(train_correlation[item]) + abs(test_correlation)))
        f3 = (abs(train_contrast[item] - test_contrast) / (abs(train_contrast[item]) + abs(test_contrast)))
        f4 = (abs(train_energy[item] - test_energy) / (abs(train_energy[item]) + abs(test_energy)))
        f5 = (abs(train_homogeneity[item] - test_homogeneity) / (abs(train_homogeneity[item]) + abs(test_homogeneity)))
        f6 = (abs(train_entropy[item] - test_entropy) / (abs(train_entropy[item]) + abs(test_entropy)))

        temp_canberrea_distance = f1 + f2 + f3 + f4 + f5 + f6
        canberrea_distance[item].append(temp_canberrea_distance)
        canberrea_distance[item].append(train_name[item])

    canberrea_distance.sort()
    res = canberrea_distance[:10]


def output():
    print('output')
    for i in res:
        print(i)


# main execution
root = Tk()
root.title('Similar Image Retrieval using Canberra Distance')
root.geometry('1080x720')

frame1 = Frame(root, padx=50, pady=50)
frame1.pack(side='top')
label = Label(frame1, text='result', padx=100, pady=100)
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
