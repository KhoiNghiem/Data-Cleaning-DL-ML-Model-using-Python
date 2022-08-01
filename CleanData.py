# Import library
import pandas as pd
import numpy as np
import re

# Import Data
df1 = pd.read_excel("raw_data.xlsx")

# Xóa cột "Unnamed"
df2 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]
df2 = df2.drop("Điểm tb", axis = "columns")

# Xóa môn tín bằng 0
df3 = (df2.loc[(df2["Số TC"] != 0)])  

# List các Mã học phần cần xóa
subject_del = ["SSH1110", "SSH1120", "SSH1050", "SSH1130",
                "MIL1110", "MIL1120", "MIL1130", "EM1010", 
                "EM1100", "EM1170", "EM1180", "EM1160", 
                "EM1170", "EM2104", "EM3102", "EM3150", 
                "EM3170", "EM3190", "EM4317", "EM4323", 
                "EM4415", "ED3110", "ED3220", "EV3305"]

# Hàm xóa các mã học phần không cần thiết
def delete_data(x):
    df_out = pd.DataFrame
    df_out = df3.copy()
    for i in range(0, len(x)):
        df_out = (df_out.loc[df_out["Mã HP"] != x[i]])
    return df_out

# Tạo dataframe mới để lưu dữ liệu sau khi xóa các mã học phần
df4 = delete_data(subject_del)

# Hàm tính điểm trung bình của từng học phần
def averange_Point(x, y): 
    result = []
    nan_index = np.where(df4['Điểm QT'].isnull())[0]
    x_arr = x.tolist()
    y_arr = y.tolist()
    for i in range(0, len(x)):
        if(i in nan_index):
            result.append(y_arr[i])    
        else: 
            result.append(0.3*x_arr[i] + 0.7*y_arr[i])
    return result

# Dataframe để lưu điểm trung bình
df5 = df4.copy()
df5["Điểm TB"] = (averange_Point(df4["Điểm QT"], df4["Điểm CK"]))

# Sắp xếp lại theo thứ tự tăng dần của Id sinh viên
df6 = df5.sort_values(by = "Họ và tên" , ascending = True)

# Hàm để tính toán điểm GPA lớn hơn 5
def GPA_above_5(x):
    if(x < 5):
        return 0
    else:
        return 1
df7 = df6.copy()
df7["Điểm TB trên 5"] = df6["Điểm TB"].apply(GPA_above_5)

# Lấy các mã học phần 
value = df7["Mã HP"].tolist()

# Hàm lấy mã viện
def getAlpha(code):
    matches = re.search("([a-zA-Z]+)(\d+)", code)
    if matches is None:
        return ''
    return matches.group(1)

# Hàm lấy mã viện và năm học
def getDigit(code):
    matches = re.search("(([a-zA-Z]+\d))", code)
    if matches is None:
        return ''
    return matches.group(2)

result1 = list(map(getAlpha, value))
result2 = list(map(getDigit, value))

# Lưu mã học phần vào file data1.xlsx 
df8 = df7.copy()
df8["Mã"] = result1

# Lưu mã học phần, năm học vào file data2.xlsx
df9 = df7.copy()
df9["Mã"] = result2

# Lấy các mã học phần cần thiết cho mô hình
df_EE1 = (df9.loc[df9["Mã"] == "EE1"])
df_EE2 = (df9.loc[df9["Mã"] == "EE2"])
df_EE3 = (df9.loc[df9["Mã"] == "EE3"])
df_EE4 = (df9.loc[df9["Mã"] == "EE4"])
df_MI = (df8.loc[df8["Mã"] == "MI"])
df_IT = (df8.loc[df8["Mã"] == "IT"])
df_PH = (df8.loc[df8["Mã"] == "PH"])
df_ME = (df8.loc[df8["Mã"] == "ME"])

# Hàm lấy điểm trung bình lớn nhất của từng mã học phần của từng sinh viên
def max_point(df):
    df_max_point = pd.DataFrame()
    df_name = pd.DataFrame()
    df_MHP = pd.DataFrame()
    for i in range(1, (df["Họ và tên"].unique())[-1] + 1):
        df_name = (df.loc[df["Họ và tên"] == i])
        for j in (df_name["Mã HP"].unique()):
            df_MHP = df_name.loc[df_name["Mã HP"] == j]
            max_point = max(df_MHP['Điểm TB'])
            df_max_point = pd.concat([df_max_point, df_MHP[df_MHP['Điểm TB'] == max_point]])
    return df_max_point

# Lưu điểm vào từng data frame của từng mã
df_EE1 = max_point(df_EE1)
df_EE2 = max_point(df_EE2)
df_EE3 = max_point(df_EE3)
df_EE4 = max_point(df_EE4)
df_MI = max_point(df_MI)
df_IT = max_point(df_IT)
df_PH = max_point(df_PH)
df_ME = max_point(df_ME)

# Hàm tính điểm trung bình của từng mã thu được ở trên
def average_point(df):
    avr = []
    df_test = pd.DataFrame()
    for i in range(1, (df["Họ và tên"].unique())[-1] + 1):
        df_test = (df.loc[df["Họ và tên"] == i])
        avr.append((np.sum(df_test["Điểm TB"]*df_test["Số TC"]))/(np.sum(df_test["Số TC"])))
    return avr

# Do chiều dài của EE4 và ME ít hơn các mã còn lại 1 đơn vị nên phải + 2
def average_point_EE4(df):
    avr = []
    df_test = pd.DataFrame()
    for i in range(1, (df["Họ và tên"].unique())[-1] + 2):
        df_test = (df.loc[df["Họ và tên"] == i])
        avr.append((np.sum(df_test["Điểm TB"]*df_test["Số TC"]))/(np.sum(df_test["Số TC"])))
    return avr

def average_point_ME(df):
    avr = []
    df_test = pd.DataFrame()
    for i in range(1, (df["Họ và tên"].unique())[-1] + 2):
        df_test = (df.loc[df["Họ và tên"] == i])
        avr.append((np.sum(df_test["Điểm TB"]*df_test["Số TC"]))/(np.sum(df_test["Số TC"])))
    return avr

# Tính điểm từng mã
avr1 = average_point(df_EE1)
avr2 = average_point(df_EE2)
avr3 = average_point(df_EE3)
avr4 = average_point_EE4(df_EE4)
avrMI = average_point(df_MI)
avrIT = average_point(df_IT)
avrPH = average_point(df_PH)
avrME = average_point_ME(df_ME)

# Lưu điểm của từng mã của từng sinh viên vào data frame cuối cùng
df_final = pd.DataFrame()
df_final["Họ và tên"] = np.arange(1, 430)
df_final["EE1"] = avr1[0:(len(avr1))]
df_final["EE2"] = avr2[0:len(avr2)]
df_final["EE3"] = avr3[0:len(avr3)]
df_final["MI"] = avrMI[0:len(avrMI)]
df_final["IT"] = avrIT[0:len(avrIT)]
df_final["PH"] = avrPH[0:len(avrPH)]
df_final["ME"] = avrME[0:len(avrME) + 1]
df_final["EE4"] = avr4[0:len(avr4)]

# Xóa điểm NULL và xóa cột họ tên
df_final = df_final.dropna()
df_final = df_final.drop(["Họ và tên"], axis = 'columns')

# Xuất file excel để sử dụng cho model
df_final.to_excel("Final_Data.xlsx")