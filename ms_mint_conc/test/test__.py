import os
import pandas as pd
import datetime
import numpy as np

from ms_mint_conc.calibration_curves import info_from_Mint, info_from_Maven
from ms_mint_conc import MS_CONC_TEST_DATA

class Testing_MS_Conc():
    def test__info_with_peak_area(self):
        fn = os.path.join(MS_CONC_TEST_DATA, 
                         'test_Mint_1.csv')
        actual = info_from_Mint(pd.read_csv(fn),'peak_area')
        data = {
                'ms_file': ['this_is_file_1','this_is_file_1','this_is_file_1','this_is_file_2','this_is_file_2'],
                'peak_label': ['compound_1','compound_2','compound_3','compound_1','compound_3'], 
                'value': [10,20,15,100,1500]
        }
        expected = pd.DataFrame(data, index=[0])
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
        
def test__info_with_peak_max(self):
        fn = os.path.join(MS_CONC_TEST_DATA, 
                         'test_Mint_1.csv')
        actual = info_from_Mint(pd.read_csv(fn),'peak_max')
        data = {
                'ms_file': ['this_is_file_1','this_is_file_1','this_is_file_1','this_is_file_2','this_is_file_2'],
                'peak_label': ['compound_1','compound_2','compound_3','compound_1','compound_3'], 
                'value': [100,100,150,1000,15000]
        }
        expected = pd.DataFrame(data, index=[0])
        assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'