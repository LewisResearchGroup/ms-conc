import pandas as pd
import numpy as np
from ms_conc import calibration_curves as cc


def test__file_with_bi_nbr():
    actual = 2+2
    expected = 4

    assert actual == expected # actual.equals(expected), f'\nExpected:\n {expected}\nReceived:\n {actual}'
# class Testing_for_Scalir_app():
    
    
def test__classic_lstsqr_test1():
    x = np.array([0, 1, 2, 3])
    y = np.array([0, 1, 2, 3])
    
    y_interc, residual, r_ini, r_last = cc.classic_lstsqr(x, y)
    
    actual = [y_interc, residual, r_ini, r_last]
    expected = [0, 0, 0, 0]
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'

def test__classic_lstsqr_test2():
    x = np.array([0, 1, 2, 3])
    y = np.array([1, 2, 3, 4])
    
    y_interc, residual, r_ini, r_last = cc.classic_lstsqr(x, y)
    
    actual = [y_interc, residual, r_ini, r_last]
    expected = [1, 0, 0, 0]
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
def test__classic_lstsqr_variable_slope_test1():
    x = np.array([0, 1, 2, 3])
    y = np.array([1, 2, 3, 4])
    
    y_interc, slope , residual, r_ini, r_last = cc.classic_lstsqr_variable_slope(x, y)
    
    actual = [y_interc, slope, residual, r_ini, r_last]
    expected = [1, 1, 0, 0, 0]
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'   
    
def test__classic_lstsqr_variable_slope_test2():
    x = np.array([0, 1, 2, 3])
    y = np.array([2, 4, 6, 8])
    
    y_interc, slope , residual, r_ini, r_last = cc.classic_lstsqr_variable_slope(x, y)
    
    actual = [y_interc, slope, residual, r_ini, r_last]
    expected = [2, 2, 0, 0, 0]
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'    

    
def test__classic_lstsqr_variable_slope_test3():
    x = np.array([0, 1, 2, 3])
    y = np.array([0, .5, 1, 1.5])
    
    y_interc, slope , residual, r_ini, r_last = cc.classic_lstsqr_variable_slope(x, y)
    
    actual = [y_interc, slope, residual, r_ini, r_last]
    expected = [0, .5, 0, 0, 0]
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'    

    
    
def test__classic_lstsqr_variable_slope_interval_test1():
    x = np.array([0, 1, 2, 3])
    y = np.array([1, 2, 3, 4])
    
    y_interc, slope , residual, r_ini, r_last = cc.classic_lstsqr_variable_slope_interval(x, y, [0,2])
    
    actual = [y_interc, slope, residual, r_ini, r_last]
    expected = [1, 1, 0, 0, 0]
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
    
def test__classic_lstsqr_variable_slope_interval_test2():
    x = np.array([0, 1, 2, 3])
    y = np.array([2, 4, 6, 8])
    
    y_interc, slope , residual, r_ini, r_last = cc.classic_lstsqr_variable_slope_interval(x, y, [0,2])
    
    actual = [y_interc, slope, residual, r_ini, r_last]
    expected = [2, 2, 0, 0, 0]  
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
def test__classic_lstsqr_variable_slope_interval_test3():
    x = np.array([0, 1, 2, 3])
    y = np.array([1, 2, 3, 4])
    
    y_interc, slope , residual, r_ini, r_last = cc.classic_lstsqr_variable_slope_interval(x, y, [1,2])
    
    actual = [y_interc, slope, residual, r_ini, r_last]
    expected = [1, 1, 0, 0, 0]  
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'    

    
def test__find_linear_range_test1():
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([1, 2, 3, 4, 5, 6])
    
    y_intercept, x_c, y_c, res = cc.find_linear_range(x, y, 0.1)
    
    actual = [y_intercept, list(x_c), list(y_c), res ]
    expected = [1, list([0, 1, 2, 3, 4, 5]), list([1, 2, 3, 4, 5, 6]), 0]  
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'    

def test__find_linear_range_test2():
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([0, 2, 3, 4, 5, 6])
    
    y_intercept, x_c, y_c, res = cc.find_linear_range(x, y, 0.1)
    
    actual = [y_intercept, list(x_c), list(y_c), res ]
    expected = [1, list([1, 2, 3, 4, 5]), list([2, 3, 4, 5, 6]), 0]  
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'  

def test__find_linear_range_test3():
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([1, 2, 3, 4, 5, 7])
    
    y_intercept, x_c, y_c, res = cc.find_linear_range(x, y, 0.1)
    
    actual = [y_intercept, list(x_c), list(y_c), res ]
    expected = [1, list([0, 1, 2, 3, 4]), list([1, 2, 3, 4, 5]), 0]  
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'

def test__find_linear_range_test4():
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([-7, -6, 1, 4.4, 5, 6])
    
    y_intercept, x_c, y_c, res = cc.find_linear_range(x, y, 0.1)
    
    actual = [list(x_c), list(y_c)]
    expected = [list([ 3, 4, 5]), list([4.4, 5, 6])]  
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'
    
def test__find_linear_range_variable_slope_test1():
    
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([1, 2, 3, 4, 5, 6])
    
    y_intercept, slope, x_c, y_c, res = cc.find_linear_range_variable_slope(x, y, 0.1)
    
    actual = [y_intercept, slope, list(x_c), list(y_c), res ]
    expected = [1, 1, list([0, 1, 2, 3, 4, 5]), list([1, 2, 3, 4, 5, 6]), 0]  
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'    

def test__find_linear_range_variable_slope_test2():
    
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10, 12])
    
    y_intercept, slope, x_c, y_c, res = cc.find_linear_range_variable_slope(x, y, 0.1)
    
    actual = [y_intercept, slope, list(x_c), list(y_c), res ]
    expected = [2, 2, list([0, 1, 2, 3, 4, 5]), list([2, 4, 6, 8, 10, 12]), 0]  
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'  

    
def test__find_linear_range_variable_slope_test2():
    
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10, 12])
    
    y_intercept, slope, x_c, y_c, res = cc.find_linear_range_variable_slope(x, y, 0.1)
    
    actual = [y_intercept, slope, list(x_c), list(y_c), res ]
    expected = [2, 2, list([0, 1, 2, 3, 4, 5]), list([2, 4, 6, 8, 10, 12]), 0]  
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'  
    
def test__find_linear_range_variable_slope_test3():
    
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10, 12])
    
    y_intercept, slope, x_c, y_c, res = cc.find_linear_range_variable_slope(x, y, 0.1)
    
    actual = [y_intercept, slope, list(x_c), list(y_c), res ]
    expected = [2, 2, list([0, 1, 2, 3, 4, 5]), list([2, 4, 6, 8, 10, 12]), 0]  
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'  
    

def test__find_linear_range_variable_slope_test3():
    
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([0, 4.1, 6, 8, 14, 18])
    
    y_intercept, slope, x_c, y_c, res = cc.find_linear_range_variable_slope(x, y, 0.1)
    
    actual = [ list(x_c), list(y_c) ]
    expected = [ list([1, 2, 3,]), list([4.1, 6, 8])]  
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'    


def test__find_linear_range_variable_slope_test4():
    
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([2.5, 4.1, 6, 8, 8.2, 12])
    
    y_intercept, slope, x_c, y_c, res = cc.find_linear_range_variable_slope(x, y, 0.1)
    
    actual = [ list(x_c), list(y_c) ]
    expected = [ list([0, 1, 2, 3,]), list([2.5, 4.1, 6, 8])]  
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}'    


def test__find_linear_range_variable_slope_test5():
    
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([2.5, 4.1, 6, 8, 8.2, 9])
    
    y_intercept, slope, x_c, y_c, res = cc.find_linear_range_variable_slope(x, y, 0.01)
    
    actual = [ list(x_c), list(y_c) ]
    expected = [ list([1, 2, 3,]), list([ 4.1, 6, 8])]  
    
    assert actual == expected, f'\nExpected:\n {expected}\nReceived:\n {actual}' 
