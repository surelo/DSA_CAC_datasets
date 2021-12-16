import os
import time
#from CalciumDataProcessor import DicomInfoReader, LabelReader, FrameGet, FocusGet
import DicomInfoReader, LabelReader, FrameGet, FocusGet


# 只需要把pwd拷贝到这
path_flex = '/Users/surelo/Desktop/calcification_20191231(456-480)-hyf/ZHU_WEN_HUI/2019_10_23_20_05_02'

path_dcm = path_flex + '/IMG-0001-00001.dcm'
path_data = path_flex + '/DiseaseLabelResult_add.data'
dcm_folder = path_flex + '/'

savepath_frame = './datafolder/frame/'
savepath_focus = './datafolder/focus/'
savepath_label = './datafolder/label/'
savepath_mask = './datafolder/mask/'

# 1. 获取DICOM信息 patient_name, patient_id
dicom_reader = DicomInfoReader.DicomInfoReader()
patient_name, patient_id = dicom_reader.dcm_read(path_dcm)
print(patient_id, patient_name)

# 2. 获取.data文件信息
df = LabelReader.LabelReader().data_to_df(path_data)
patient_name, img_name_list, list_frame, calcium_position, type_calcium = LabelReader.LabelReader().label_reader(df)
print(patient_name)
print(img_name_list)
print(list_frame)
print(calcium_position)
print(type_calcium)

# 自动生成对应patient_name的文件目录
os.mkdir(savepath_frame + patient_name + '/')
os.mkdir(savepath_focus + patient_name + '/')
os.mkdir(savepath_label + patient_name + '/')
os.mkdir(savepath_mask + patient_name + '/')

savepath_frame = savepath_frame + patient_name + '/'
savepath_focus = savepath_focus + patient_name + '/'
savepath_label = savepath_label + patient_name + '/'
savepath_mask = savepath_mask + patient_name + '/'
'''
file_name = patient_name +'_'+img_name_list[0][6:8]+'_'+ list_frame[1][2]+'_'+type_calcium[6]
print(file_name)
'''
# 3. 帧数提取模块
FrameGet.FrameGet().frame_get(patient_name, dcm_folder, savepath_frame, img_name_list, list_frame, type_calcium)

# 4. 病灶提取模块
FocusGet.FocusGet().focus_get(savepath_frame, savepath_focus, savepath_label, savepath_mask, calcium_position)


