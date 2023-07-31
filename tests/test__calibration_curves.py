import pandas as pd
import numpy as np

from ms_conc import calibration_curves as cc

def test__file_with_bi_nbr():
    
    curve = pd.DataFrame(columns={'peak_label'})
    curve.peak_label = ['M1','M2','M3','M4']
    curve['10nm'] = [10., 20., 50., 5.]
    curve['100nm'] = 10*curve['10nm']
    curve['1000nm'] = 100*curve['10nm']
    curve['10000nm'] = 1000*curve['10nm']
    curve['100000nm'] = 10000*curve['10nm']
    curve['1000000nm'] = 100000*curve['10nm']
    curve['10000000nm'] = 1000000*curve['10nm']
    curve.at[0, '10000000nm'] /= 20.
    curve.at[1, '10nm'] *= 20.
    curve.at[1, '100nm'] /= 5.
    curve.at[2, '10nm'] *=5.
    curve.at[2, '10000000nm'] /=5.
    
    cols = curve.columns
    s0 = pd.DataFrame()

    s0['value'] = curve[cols[1]]
    s0['peak_label'] = curve.peak_label
    s0['conc'] = float(cols[1][:-2])
    s1 = pd.DataFrame()
    i = 1
    for col in cols[2:]:
        s1['value'] = curve[col]
        s1['peak_label'] = curve.peak_label
        s1['conc'] = float(col[:-2])
        i+=1
        s0 = pd.concat([s0,s1], axis = 0)
        
    s0.reset_index(inplace = True)
    s0.drop(['index'], axis = 1, inplace = True)
    
    y_train = np.array(s0.conc)
    x_train = s0.drop(['conc'], axis = 1)

    expected = pd.DataFrame(data, index=[0])
    
    assert actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'