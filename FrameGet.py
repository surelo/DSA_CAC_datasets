# coding=utf-8
import time
import SimpleITK as sitk
from PIL import Image
import pydicom
import numpy as np
import cv2

# 自动提取帧并保存之前，要先生成文件夹

class FrameGet:
    def frame_get(self, patient_name, dcm_folder, savepath, dicom_name, zhenhao, calcium_type):
        print('_______________________________________________________________')
        print('关键帧提取模块')
        start_time = time.time()
        self.dcm_folder = dcm_folder
        num_temp = 0
        for i, name in enumerate(dicom_name):
            for j in zhenhao[i]:
                ds = sitk.ReadImage(dcm_folder + name)
                img_array = sitk.GetArrayFromImage(ds)
                savename = ('%02d' % num_temp) + '_' + patient_name + '_' + dicom_name[i][6:8] + '_' + ('%02d' % int(j)) + '_' + calcium_type[num_temp] + '.png'
                cv2.imwrite(savepath + savename, img_array[int(j)])
                print(savename + ' is saved!')
                num_temp += 1
        end_time = time.time()
        print('帧数已经提取完毕，总用时', '%.2f' % (end_time-start_time),'秒')
        print('______________________________________________________________')





'''
patient_name = 'ZHAO_WEI_BIN'
dcm_folder = '../ZHU_WEI_BIN/2018_7_30_9_19_55/'
savepath = './datafolder_test_v1/frame/ZHU_WEI_BIN/'
dicom_name = ['IMG-0003-00001.dcm', 'IMG-0001-00001.dcm', 'IMG-0005-00001.dcm']
zhenhao = [['0', '1', '2', '3'], ['0', '1', '2', '3'], ['0', '0', '1', '1', '2', '2', '3', '3', '4', '4']]
calcium_type = ['moderate_LM', 'moderate_LM', 'moderate_LM', 'moderate_LM', 'severe_LAD', 'severe_LAD', 'severe_LAD', 'severe_LAD', 'moderate_RCA', 'moderate_RCA', 'moderate_RCA', 'moderate_RCA', 'moderate_RCA', 'moderate_RCA', 'moderate_RCA', 'moderate_RCA', 'moderate_RCA', 'moderate_RCA']


num_temp = 0
for i, name in enumerate(dicom_name):
    for j in zhenhao[i]:
        ds = sitk.ReadImage( dcm_folder + name )
        img_array = sitk.GetArrayFromImage( ds )
        savename = ('%02d' % num_temp) + '_' + patient_name + '_' + dicom_name[i][6:8] + '_' + ('%02d' % int(j)) + '_' + calcium_type[num_temp] + '.png'
        cv2.imwrite( savepath + savename, img_array[int(j)])
        print( savename + ' is saved!' )
        num_temp += 1
'''







