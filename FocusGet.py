import os
import time
import cv2
import csv
import numpy as np
import pandas as pd

class FocusGet:
    def focus_get(self, frame_folder, savepath_focus, savepath_label, savepath_mask, calcium_position):
        print('病灶处理模块')
        start_time = time.time()
        path_list = os.listdir(frame_folder)
        path_list.sort()
        for i, file in enumerate( path_list ):
            if file != '.DS_Store':
                print( '第', i, '张图片开始处理' )
                print( file )
                img_array = cv2.imread( frame_folder + file )

                # cv2.imshow('test', img_array)
                # cv2.waitKey(2000)
                print( img_array.shape )

                focus_name = os.path.splitext( file )[0] + '_focus.png'
                label_name = os.path.splitext( file )[0] + '_label.png'
                mask_name = os.path.splitext( file )[0] + '_mask.png'
                print(focus_name)
                print(label_name)
                print(mask_name)

                Xmin = int( float( calcium_position[i - 1][0] ) * 512 )
                Ymin = int( float( calcium_position[i - 1][1] ) * 512 )
                Xmax = int( float( calcium_position[i - 1][2] ) * 512 )
                Ymax = int( float( calcium_position[i - 1][3] ) * 512 )
                print( Xmin, Xmax, Ymin, Ymax )

                img_array = cv2.resize( img_array, (512, 512) )
                print( img_array.shape )
                crop = img_array[Ymin:Ymax, Xmin:Xmax]
                print( crop.shape )
                # cv2.imshow('test_crop', crop)

                print( savepath_focus + focus_name )
                cv2.imwrite( (savepath_focus + focus_name)[2:], crop )  # 保存focus图
                print( '第', i, '张focus图已制作' )

                # 保存label图
                img_rec = cv2.rectangle( img_array, (Xmin, Ymin), (Xmax, Ymax), (0, 255, 0),
                                         1 )  # BGR颜色，(255, 0, 0)是蓝色, 1是矩形框的宽度为1个pixel
                cv2.imwrite( (savepath_label + label_name), img_rec )
                print( '第', i, '张label图已制作' )

                # 保存mask图
                mask = np.zeros( (512, 512), dtype=np.uint8 )  # 512*512背景 默认黑色
                cv2.rectangle( mask, (Xmin, Ymin), (Xmax, Ymax), (255, 255, 255), thickness=-1 )  # 在钙化位置生成白色矩形
                cv2.imwrite( savepath_mask + mask_name, mask )
                print( '第', i, '张mask图已制作' )
                print( '#########################################' )
        end_time = time.time()
        print( '病灶区域、label图、mask图已完成，总用时', '%.2f' % (end_time-start_time),'秒！' )


'''
# 保存路径

frame_folder = './datafolder_test_v1/frame/ZHU_WEI_BIN/'
savepath_focus = './datafolder_test_v1/focus/ZHU_WEI_BIN/'
savepath_label = './datafolder_test_v1/label/ZHU_WEI_BIN/'
savepath_mask = './datafolder_test_v1/mask/ZHU_WEI_BIN/'


path_list = os.listdir(frame_folder)
path_list.sort()
calcium_position = [['0.378601', '0.269547', '0.423868', '0.314815'], ['0.379630', '0.274691', '0.426955', '0.315844'], ['0.381687', '0.272634', '0.421811', '0.311728'], ['0.381687', '0.279835', '0.412551', '0.314815'], ['0.302734', '0.130658', '0.722222', '0.263374'], ['0.281250', '0.117188', '0.718750', '0.250000'], ['0.293210', '0.118313', '0.729424', '0.250000'], ['0.294239', '0.115226', '0.726337', '0.246914'], ['0.078189', '0.267490', '0.267578', '0.498047'], ['0.146091', '0.515432', '0.504115', '0.645062'], ['0.080247', '0.270576', '0.272634', '0.490741'], ['0.123457', '0.497942', '0.467078', '0.652263'], ['0.078189', '0.281893', '0.286008', '0.495885'], ['0.137860', '0.503086', '0.474280', '0.659465'], ['0.080247', '0.274691', '0.278807', '0.493827'], ['0.145062', '0.497942', '0.461934', '0.653292'], ['0.068930', '0.273663', '0.266461', '0.490741'], ['0.120370', '0.496914', '0.458984', '0.658203']]

for i, file in enumerate(path_list):
    if file != '.DS_Store':
        print('第', i, '张图片开始处理')
        print(file)
        img_array = cv2.imread(frame_folder+file)
        
        #cv2.imshow('test', img_array)
        #cv2.waitKey(2000)
        print(img_array.shape)

        focus_name = os.path.splitext(file)[0] + '_focus.png'
        label_name = os.path.splitext(file)[0] + '_label.png'
        mask_name = os.path.splitext(file)[0] + '_mask.png'
        print(focus_name, label_name, mask_name)

        Xmin = int(float(calcium_position[i-1][0]) * 512)
        Ymin = int(float(calcium_position[i-1][1]) * 512)
        Xmax = int(float(calcium_position[i-1][2]) * 512)
        Ymax = int(float(calcium_position[i-1][3]) * 512)
        print(Xmin, Xmax, Ymin, Ymax)

        img_array = cv2.resize( img_array, (512, 512) )
        print(img_array.shape)
        crop = img_array[Ymin:Ymax, Xmin:Xmax]
        print(crop.shape)
        #cv2.imshow('test_crop', crop)

        print(savepath_focus + focus_name)
        cv2.imwrite( (savepath_focus + focus_name)[2:], crop ) # 保存focus图
        print( '第', i , '张focus图已制作' )

        # 保存label图
        img_rec = cv2.rectangle( img_array, (Xmin, Ymin), (Xmax, Ymax), (0, 255, 0),1 )  # BGR颜色，(255, 0, 0)是蓝色, 1是矩形框的宽度为1个pixel
        cv2.imwrite( (savepath_label+label_name), img_rec )
        print('第', i,'张label图已制作')

        # 保存mask图
        mask = np.zeros( (512, 512), dtype=np.uint8 )  # 512*512背景 默认黑色
        cv2.rectangle( mask, (Xmin, Ymin), (Xmax, Ymax), (255, 255, 255), thickness=-1 )  # 在钙化位置生成白色矩形
        cv2.imwrite( savepath_mask + mask_name, mask )
        print( '第', i , '张mask图已制作' )
        print('#########################################')

print('DONE!')

'''

