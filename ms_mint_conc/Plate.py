from lrg_omics.metabolomics.common import metadata_from_worklist, metadata_from_filename, read_plate
from lrg_omics.metabolomics.common import classic_lstsqr, linear_range_finder, read_plate_2
from lrg_omics import LRG_TEST_DATA
import pandas as pd
import numpy as np

class Plate(): # fix start with cappital letter

    def __init__(self, plate_id, direction):
        self._plate_id = plate_id
        self._path = LRG_TEST_DATA + direction
#         self._ms_files = [os.path.basename(x) for x in glob.glob(self._path + '/*.mzXML')]
#         self._worklist = pd.read_csv(self._path + '/LSARP-Full-May2020-Worklist.csv', skiprows=1 )
        self._samples = pd.DataFrame()
#         self._standards = pd.DataFrame()
#         self._MH_POOL = pd.DataFrame()
#         self._SA_POOL = pd.DataFrame()

#     def add(self, x):
#         self.data.append(x)
        
# '''reading the work list'''       
#     def read_worklist(self):
#         worklist = pd.read_csv(self._path + '/LSARP-Full-May2020-Worklist.csv', skiprows=1 )
#         self._worklist = worklist
        
# '''reading all samples'''       
    def read_samples(self):
        worklist = 'LSARP-Full-May2020-Worklist.csv' #this can be optional, maybe readworklist()
        self._samples = read_plate_2(self._plate_id, self._path, worklist)
        
            
    def standards(self):
        standards = self._samples[self._samples.SAMPLE_TYPE == 'ST']
        return pd.DataFrame({'ms_file':standards.FILE_DIR, 'Concentration': standards.STD_CONC})
    
    def non_standards(self):
        non_standards = self._samples[self._samples.SAMPLE_TYPE != 'ST']
        return pd.DataFrame({'ms_file':non_standards.FILE_DIR})
    
    def qc(self):
        qc_samples = self._samples[self._samples.SAMPLE_TYPE == 'QC']
        return pd.DataFrame({'ms_file':qc_samples.FILE_DIR})
    
    def pool_media(self):
        pool_media = self._samples[self._samples.SAMPLE_TYPE == 'PO-MH']
        return pd.DataFrame({'ms_file':pool_media.FILE_DIR})
    
    def pool_samples(self):
        pool_samples = self._samples[self._samples.SAMPLE_TYPE == 'PO-SA']
        return pd.DataFrame({'ms_file':pool_samples.FILE_DIR})
    
