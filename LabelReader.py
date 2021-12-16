# 目的是读取该文件夹下的data文件并输出匹配内容
# 以ZHU_WEI_BIN/2018_7_30_9_19_55/IMG-0003-00001.dcm 1 0.379630 0.274691 0.426955 0.315844 0 44为例
# ······姓名··········造影时间·········DICOM文件名·····帧数···钙化病灶区域Xmin,Xmax,Ymin,Ymax···没用··血管分支及严重程度
# 思路：data文件直接读取/变为csv文件

import pandas as pd
import numpy as np
import csv
import os
import time

calcium_type_list = [('40', 'mild_LM'), ('41', 'mild_LAD'), ('42', 'mild_LCX'), ('43', 'mild_RCA'),
                         ('44', 'moderate_LM'), ('45', 'moderate_LAD'), ('46', 'moderate_LCX'),
                         ('47', 'moderate_RCA'),
                         ('48', 'severe_LM'), ('49', 'severe_LAD'), ('50', 'severe_LCX'), ('51', 'severe_RCA')]
calcium_type = dict( calcium_type_list )

class LabelReader:

    def data_to_df(self, path):
        df = pd.read_csv(path, header=None)
        df1 = df[0].str.split(expand=True)  # 按空格分离
        df2 = df1.drop(6, axis=1)  # 删除掉无用的信息
        df_right = df2.iloc[:, 1:7]  # 保留右边的列，再对第一列进行'/'分离操作
        df_left = pd.DataFrame(df2.iloc[:, 0])
        df_left = df_left[0].str.split('/', expand=True)
        df_label = pd.concat([df_left, df_right], axis=1)
        df_label.columns = ['Name', 'RadiographyTime', 'ImgName', 'Frame', 'Xmin', 'Xmax', 'Ymin', 'Ymax',
                            'CalciumType']
        return df_label

    def label_reader(self, dataframe):
        # 从上述DataFrame中提取下列信息作为备用
        # patient_name          病人姓名                                string       √
        # img_name_list[]       造影dicom文件名                          list        √
        # frame[]               dicom文件对应的帧数                      list         √
        # calcium_position[]    钙化病灶位置[Xmin, Xmax, Ymin, Ymax]     list         √
        # calcium_type{}        钙化血管分支及严重情况                     dictionary   √

        # patient_name
        patient_name = dataframe.iloc[:, 0][0]

        # img_name_list
        img_name_list = []
        df_label_img = pd.DataFrame(dataframe.iloc[:, 2])
        img_name_df = df_label_img.drop_duplicates(subset=['ImgName'], keep='first')
        for i in img_name_df.iloc[:, 0]:
            img_name_list.append(i)

        # frame
        df_img_frame = dataframe.iloc[:, [2, 3]]
        list_frame = []
        for i in range(len(img_name_list)):
            temp = df_img_frame[df_img_frame['ImgName'] == img_name_list[i]].iloc[:, 1]
            temp1 = np.array(temp)
            temp2 = temp1.tolist()
            list_frame.append(temp2)

        # calcium_position 使用时需要用num变量计数
        df_calcium_position = dataframe.iloc[:, 4:8]
        calcium_position = np.array(df_calcium_position).tolist()

        # type
        type_calcium = []
        df_calcium_type = dataframe.iloc[:, 8]
        for i in df_calcium_type:
            type_calcium.append(calcium_type.get(str(i)))

        return patient_name, img_name_list, list_frame, calcium_position, type_calcium









