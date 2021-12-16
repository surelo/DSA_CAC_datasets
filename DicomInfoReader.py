# 读取dicom文件中的病例名与病人ID
from pydicom import dcmread


class DicomInfoReader:

    def dcm_read(self, path):
        ds = dcmread(path)
        return ds.PatientName, ds.PatientID


