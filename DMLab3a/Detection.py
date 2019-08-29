from tkinter.filedialog import *
import glob as g
import cv2 as oc
import os
import numpy as n
from pandas import DataFrame
import xlrd
from astropy.stats import median_absolute_deviation
from scipy.stats import skew
from scipy.stats import variation
import math as m


# Define the button operations
def openfile():
    print('Open File Button Clicked')
    global folder_path
    folder_path = askdirectory()
    print('Selected PATH = ' + folder_path)


def save():
    print('Save Button Clicked')
    global folder_content_length, train_mean
    # print(folder_path)
    path = g.glob(folder_path + '/*.png')
    print(path)

    length = 0
    for pathname in path:
        length += 1
    print(length)
    folder_content_length = length  # Assign length to a global variable for later uses

    # List creation
    cv_img = [list() for f in range(length + 1)]

    mean_list = []

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

        # Calculation
        mean_value = n.mean(image_matrix)
        mean_list.append(mean_value)
        min_value = n.min(image_matrix)
        max_value = n.max(image_matrix)
        median_value = n.median(image_matrix)
        first_quartile = n.quantile(image_matrix, .25)
        third_quartile = n.quantile(image_matrix, .75)
        variance = n.var(image_matrix)

        # def meanDeviation(numpy_array, mean):
        #     # mean = n.mean(numpyarray)
        #     f = lambda x: abs(x - mean)
        #     vf = n.vectorize(f)
        #     return (n.add.reduce(vf(numpy_array))) / len(numpy_array)

        # m = list(chain.from_iterable(image_matrix))
        # mm = pd.Series(m)
        # mean_deviation = mm.mad()
        # mean_deviation = meanDeviation(image_matrix, mean_value)

        mean_deviation = median_absolute_deviation(image_matrix)
        # skewness = skew(skew(image_matrix))
        skewness = skew(image_matrix, axis=None)
        # c_variation = variation(variation(image_matrix))
        c_variation = variation(image_matrix, axis=None)

        cv_img[i].append(name)
        cv_img[i].append(min_value)
        cv_img[i].append(max_value)
        cv_img[i].append(median_value)
        cv_img[i].append(first_quartile)
        cv_img[i].append(third_quartile)
        cv_img[i].append(variance)
        cv_img[i].append(mean_deviation)
        cv_img[i].append(skewness)
        cv_img[i].append(c_variation)
        i += 1

    train_mean = mean_list

    df = DataFrame(cv_img, columns=['Label', "Min Value", "Max Value", 'Median', "First Quartile Q1",
                                    "Third Quartile Q2", "Variance", "Mean Deviation", "Skewness", "Variation"])
    export_excel = df.to_excel(r'C:\Users\Toothless\PycharmProjects\DMLab3a\export_dataframe.xlsx', index=None,
                               header=True)
    print("Data Dumped Successfully")


def load():
    print('Load Button Clicked')
    # print(folder_content_length)
    global sheet, excel_path, train_name, train_min,  train_max, train_median, train_q1, train_q3, train_variance, \
        train_mean_deviation, train_skewness, train_c_variation
    name = []
    min_value = []
    max_value = []
    median_value = []
    q1 = []
    q3 = []
    variance = []
    mean_deviation = []
    skewness = []
    c_variation = []
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
        max_value.append(temp)
    train_max = max_value
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 3)
        median_value.append(temp)
    train_median = median_value
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 4)
        q1.append(temp)
    train_q1 = q1
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 5)
        q3.append(temp)
    train_q3 = q3
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 6)
        variance.append(temp)
    train_variance = variance
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 7)
        mean_deviation.append(temp)
    train_mean_deviation = mean_deviation
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 8)
        skewness.append(temp)
    train_skewness = skewness
    for i in range(sheet.nrows - 1):
        temp = sheet.cell_value(i + 1, 9)
        c_variation.append(temp)
    train_c_variation = c_variation

    # Calculation of (sigma A) & ~A
    global train_std_value_list, train_mean_value_list   # train_std_value_list = sigma A & train_mean_value_list = ~A
    temp_std = []
    temp_mean = []

    for i in range(folder_content_length):
        t_std = m.sqrt((train_min[i]**2 + train_max[i]**2 + train_median[i]**2 + train_q1[i]**2 + train_q3[i]**2 +
                       train_variance[i]**2 + train_mean_deviation[i]**2 + train_skewness[i]**2 +
                       train_c_variation[i]**2)-train_mean[i]**2)
        temp_std.append(t_std)
    train_std_value_list = temp_std  # sigma A calculated

    for i in range(folder_content_length):
        t_mean = ((train_min[i] + train_max[i] + train_median[i] + train_q1[i] + train_q3[i] + train_variance[i] +
                  train_mean_deviation[i] + train_skewness[i] + train_c_variation[i])/9)
        temp_mean.append(t_mean)
    train_mean_value_list = temp_mean  # ~A Calculated


def image_load():
    # print(train_name)
    # print(train_min)
    # print(train_max)
    # print(train_median)
    # print(train_q1)
    # print(train_q3)
    # print(train_variance)
    # print(train_mean_deviation)
    # print(train_skewness)
    # print(train_c_variation)
    # print(train_std_value_list)
    # print(train_mean_value_list)
    global test_image, test_min, test_max, test_median, test_q1, test_q3, test_variance, test_mean_deviation, \
        test_skewness, test_c_variation, test_std_value_list, test_mean_value_list

    test_image = askopenfilename()
    print('Test image loaded')
    image_matrix = oc.imread(test_image)
    image_matrix = oc.cvtColor(image_matrix, oc.COLOR_BGR2GRAY)

    # Calculation
    image_matrix = n.array(image_matrix)
    test_min = n.min(image_matrix)
    # print(test_min)
    test_max = n.max(image_matrix)
    # print(test_max)
    test_median = n.median(image_matrix)
    # print(test_median)
    test_q1 = n.quantile(image_matrix, .25)
    # print(test_q1)
    test_q3 = n.quantile(image_matrix, .75)
    # print(test_q3)
    test_variance = n.var(image_matrix)
    # print(test_variance)
    test_mean_deviation = median_absolute_deviation(image_matrix)
    # print(test_mean_deviation)
    # test_skewness = skew(skew(image_matrix))
    test_skewness = skew(image_matrix, axis=None)
    # print(test_skewness)
    # test_c_variation = variation(variation(image_matrix))
    test_c_variation = variation(image_matrix, axis=None)
    # print(test_c_variation)
    test_mean_value = n.mean(image_matrix)
    # print(test_mean_deviation)

    test_std_value_list = m.sqrt((test_min ** 2 + test_max ** 2 + test_median ** 2 + test_q1 ** 2 + test_q3 ** 2 +
                                  test_variance ** 2 + test_mean_deviation ** 2 + test_skewness ** 2 +
                                  test_c_variation ** 2) - test_mean_value ** 2)
    # print(test_std_value_list)
    fahim = (test_min + test_max + test_median + test_q1 + test_q3 + test_variance + test_mean_deviation + test_skewness + test_c_variation)
    test_mean_value_list = fahim/9
    # print(test_mean_value_list)

    global ab
    ab_min = []
    ab_max = []
    ab_median = []
    ab_q1 = []
    ab_q3 = []
    ab_variance = []
    ab_mean_deviation = []
    ab_skewness = []
    ab_c_variation = []
    for i in train_min:
        temp = i * test_min
        ab_min.append(temp)
    for i in train_max:
        temp = i * test_max
        ab_max.append(temp)
    for i in train_median:
        temp = i * test_median
        ab_median.append(temp)
    for i in train_q1:
        temp = i * test_q1
        ab_q1.append(temp)
    for i in train_q3:
        temp = i * test_q3
        ab_q3.append(temp)
    for i in train_variance:
        temp = i * test_variance
        ab_variance.append(temp)
    for i in train_mean_deviation:
        temp = i * test_mean_deviation
        ab_mean_deviation.append(temp)
    for i in train_skewness:
        temp = i * test_skewness
        ab_skewness.append(temp)
    for i in train_c_variation:
        temp = i * test_c_variation
        ab_c_variation.append(temp)
    t = []
    for i in range(len(train_c_variation)):
        sum_a_b = ab_min[i] + ab_max[i] + ab_median[i] + ab_q1[i] + ab_q3[i] + ab_variance[i] + ab_mean_deviation[i] + \
              ab_skewness[i] + ab_c_variation[i]
        t.append(sum_a_b)
    ab = t  # sum(ab) calculated

    # print(test_min)
    # print(test_max)
    # print(test_median)
    # print(test_q1)
    # print(test_q3)
    # print(test_variance)
    # print(test_mean_deviation)
    # print(test_skewness)
    # print(test_c_variation)


def output():
    # print(ab)  # sum(ab)
    # print(train_std_value_list)  # sigma A
    # print(train_mean_value_list)  # A-
    # print(test_std_value_list)   # sigma B
    # print(test_mean_value_list)  # B-
    res = []
    for i in range(folder_content_length):
        temp_res = ((ab[i] - (9*train_mean_value_list[i]*test_mean_value_list))/(9*train_std_value_list[i]*test_std_value_list))
        res.append(temp_res)
    print(res)
    # list = sorted(res)
    lists = sorted(res, reverse=True)
    max_e = lists[0]
    print(max_e)
    lists.sort(reverse=True)
    kk = 0
    for i in res:
        if i == max_e:
            index = kk
        kk += 1
    print(train_name[index])
    print(len(res))
    print(res)
    print(kk)
    print(train_name)

    object_class = train_name[index]
    message = "Test Object Type: " + object_class
    label.configure(text=message)


# GUI
root = Tk()
root.title('Object recognition using DD measures and Correlation')
root.geometry('1080x720')

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
