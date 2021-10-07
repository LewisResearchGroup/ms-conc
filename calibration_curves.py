import pandas as pd
import numpy as np
import os
# from ms_mint.Mint import Mint

def classic_lstsqr(x_list, y_list):
    """ Computes the least-squares solution to a linear matrix equation by fixing the slope to 1
    its suitable to work on the log-scale.
    """ 
    
    N = len(x_list)
    x_avg = sum(x_list)/N
    y_avg = sum(y_list)/N
    var_x, cov_xy = 0, 0
    for x,y in zip(x_list, y_list):
        temp = x - x_avg
        var_x += temp**2
        cov_xy += temp * (y - y_avg)
    slope = 1.0
    y_interc = y_avg - slope * x_avg
    
    y_hat = y_interc + slope * x_list
    
    residual = sum((y_list - y_hat)**2)/ N
    r_ini = (y_list[0] - y_hat[0])**2
    r_last = (y_list[-1] - y_hat[-1])**2
    
    return y_interc, residual, r_ini, r_last


def classic_lstsqr_variable_slope(x_list, y_list):
    """ Computes the least-squares solution to a linear matrix equation by considering that slope could be different to 1
    its suitable to work on the log-scale.
    """ 
    
    N = len(x_list)
    x_avg = sum(x_list)/N
    y_avg = sum(y_list)/N
    var_x, cov_xy = 0, 0
    for x,y in zip(x_list, y_list):
        temp = x - x_avg
        var_x += temp**2
        cov_xy += temp * (y - y_avg)
        
    slope = cov_xy / var_x 
    y_interc = y_avg - slope * x_avg
    
    y_hat = y_interc + slope * x_list
    
    residual = sum((y_list - y_hat)**2)/N
    
    r_ini = (y_list[0] - y_hat[0])**2
    r_last = (y_list[-1] - y_hat[-1])**2
    
    return y_interc, slope, residual, r_ini, r_last

def classic_lstsqr_variable_slope_interval(x_list, y_list, slope_interval):
    """ Computes the least-squares solution to a linear matrix equation 
    by considering that slope could be different to 1 within an interval defined externally
    its suitable to work on the log-scale.
    """ 
    
    N = len(x_list)
    x_avg = sum(x_list)/N
    y_avg = sum(y_list)/N
    var_x, cov_xy = 0, 0
    for x,y in zip(x_list, y_list):
        temp = x - x_avg
        var_x += temp**2
        cov_xy += temp * (y - y_avg)
        
    slope = cov_xy / var_x
    if slope < slope_interval[0]:
        slope = slope_interval[0]
    if slope > slope_interval[1]:
        slope = slope_interval[1]

    y_interc = y_avg - slope * x_avg
    
    y_hat = y_interc + slope * x_list
    
    residual = sum((y_list - y_hat)**2)/N
    
    r_ini = (y_list[0] - y_hat[0])**2
    r_last = (y_list[-1] - y_hat[-1])**2
    
    return y_interc, slope, residual, r_ini, r_last


def find_linear_range(x , y , th):
    """ this algorith searches the range of x values in which the data behaves linearly with slope 1"""
    """ suitable to work on the log-scale """
    x_c = x
    y_c = y
    y_intercept, res, r_ini, r_last = classic_lstsqr(x_c, y_c)
    while res > th and len(x_c) > 3:
        if r_ini > r_last:
            x_c = x_c[1:]
            y_c = y_c[1:]
        else:
            x_c = x_c[:-1]
            y_c = y_c[:-1]
        y_intercept , res, r_ini, r_last = classic_lstsqr(x_c, y_c)
        
    return y_intercept, x_c, y_c, res




def find_linear_range_variable_slope(x , y , th):
    """ this algorith searches the range of x values in which the data behaves linearly with variable slope"""
    """ suitable to work on the log-scale """
    x_c = x
    y_c = y
    y_intercept, slope, res, r_ini, r_last = classic_lstsqr_variable_slope(x_c, y_c)
    while res > th and len(x_c) > 3:
        if r_ini > r_last:
            x_c = x_c[1:]
            y_c = y_c[1:]
        else:
            x_c = x_c[:-1]
            y_c = y_c[:-1]
        y_intercept, slope, res, r_ini, r_last = classic_lstsqr_variable_slope(x_c, y_c)
    return y_intercept, slope, x_c, y_c, res

def find_linear_range_variable_slope_interval(x , y , th, interval):
    """ this algorith searches the range of x values in which the data behaves linearly with variable slope"""
    """ suitable to work on the log-scale """
    x_c = x
    y_c = y
    y_intercept, slope, res, r_ini, r_last = classic_lstsqr_variable_slope_interval(x_c, y_c, interval)
    while res > th and len(x_c) > 3:
        if r_ini > r_last:
            x_c = x_c[1:]
            y_c = y_c[1:]
        else:
            x_c = x_c[:-1]
            y_c = y_c[:-1]
        y_intercept, slope, res, r_ini, r_last = classic_lstsqr_variable_slope_interval(x_c, y_c, interval)
    return y_intercept, slope, x_c, y_c, res


def calibration_curves(x_train, y_train):
    '''this function will return a dataframe with the 
    calibration curves parameters for each compound
    in this case the curve is considered to have slope 1'''
    
    ## building the calibration curves dataframe ##
    calibration_curves = pd.DataFrame(
                    columns=['peak_label', 'slope', 
                             'intercept', 'lin_range_min', 
                             'lin_range_max', 'N_points', 'Residual'] # try this way
                              )
    calibration_curves.peak_label = np.unique(x_train.peak_label)
    
    
    y_inter = 0
    x_c = [-10,-10]
#     std = x_train.copy()

    for col in calibration_curves.peak_label:
#         print('on the cycle')
        x = np.array(x_train.value[x_train.peak_label == col])
        y = np.array(y_train[x_train.peak_label == col])
#         y = conc
#         print(x)
        y = y[x > 0.0000000000001]
        x = x[x > 0.0000000000001]
   
        x = x[y > 0.0000000000001]
        y = y[y > 0.0000000000001]        
#         print(y[0])
        y = np.log(y)
        x = np.log(x)
        if len(x > 2):
            y_inter,  x_c , y_c, res = find_linear_range(x, y, 0.05)
#             print(min(x_c))
        calibration_curves.lin_range_min[calibration_curves.peak_label == col] = min(y_c) 
        calibration_curves.lin_range_max[calibration_curves.peak_label == col] = max(y_c) 
        calibration_curves.intercept[calibration_curves.peak_label == col] = y_inter
        calibration_curves.slope[calibration_curves.peak_label == col] = 1
        calibration_curves.N_points[calibration_curves.peak_label == col] = len(x_c)
        calibration_curves.Residual[calibration_curves.peak_label == col] = res
        
    calibration_curves['LLOQ'] = calibration_curves.lin_range_min.apply(lambda x: np.exp(x))
    calibration_curves['ULOQ'] = calibration_curves.lin_range_max.apply(lambda x: np.exp(x))

#         print(len(calibration_curves))
    return calibration_curves


def calibration_curves_variable_slope(x_train, y_train):
    '''this function will return a dataframe with the 
    calibration curves parameters for each compound
    in this case the curve is considered to allow slope different to one'''
    
    ## building the calibration curves dataframe ##
    calibration_curves = pd.DataFrame(
                    columns=['peak_label', 'slope', 
                             'intercept', 'lin_range_min', 
                             'lin_range_max','N_points','Residual'] # try this way
                              )
    calibration_curves.peak_label = np.unique(x_train.peak_label)
    
    
    y_inter = 0
    x_c = [-10,-10]
#     std = x_train.copy()

    for col in calibration_curves.peak_label:
#         print('on the cycle')
        x = np.array(x_train.value[x_train.peak_label == col])
        y = np.array(y_train[x_train.peak_label == col])
#         y = conc
#         print(x)
        y = y[x > 0.0000000000001]
        x = x[x > 0.0000000000001]
   
        x = x[y > 0.0000000000001]
        y = y[y > 0.0000000000001]        
#         print(y[0])
        y = np.log(y)
        x = np.log(x)
        if len(x > 2):
            y_inter, slope,  x_c , y_c, res = find_linear_range_variable_slope(x, y, 0.05)
#             print(min(x_c))
        calibration_curves.lin_range_min[calibration_curves.peak_label == col] = min(y_c) 
        calibration_curves.lin_range_max[calibration_curves.peak_label == col] = max(y_c) 
        calibration_curves.intercept[calibration_curves.peak_label == col] = y_inter
        calibration_curves.slope[calibration_curves.peak_label == col] = slope
        calibration_curves.N_points[calibration_curves.peak_label == col] = len(x_c)
        calibration_curves.Residual[calibration_curves.peak_label == col] = res
        
    calibration_curves['LLOQ'] = calibration_curves.lin_range_min.apply(lambda x: np.exp(x))
    calibration_curves['ULOQ'] = calibration_curves.lin_range_max.apply(lambda x: np.exp(x))
#         print(len(calibration_curves))
    return calibration_curves


def calibration_curves_variable_slope_interval(x_train, y_train, interval):
    '''this function will return a dataframe with the 
    calibration curves parameters for each compound
    in this case the curve is considered to allow slope different to one'''
    
    ## building the calibration curves dataframe ##
    calibration_curves = pd.DataFrame(
                    columns=['peak_label', 'slope', 
                             'intercept', 'lin_range_min', 
                             'lin_range_max', 'N_points', 'Residual'] 
                              )
    calibration_curves.peak_label = np.unique(x_train.peak_label)
    
    
    y_inter = 0
    x_c = [-10,-10]
#     std = x_train.copy()

    for col in calibration_curves.peak_label:
#         print('on the cycle')
        x = np.array(x_train.value[x_train.peak_label == col])
        y = np.array(y_train[x_train.peak_label == col])
#         y = conc
#         print(x)
        y = y[x > 0.0000000000001]
        x = x[x > 0.0000000000001]
   
        x = x[y > 0.0000000000001]
        y = y[y > 0.0000000000001]        
#         print(y[0])
        y = np.log(y)
        x = np.log(x)
        if len(x > 2):
            y_inter, slope,  x_c , y_c, res = find_linear_range_variable_slope_interval(x, y, 0.05, interval)
#             print(min(x_c))
        calibration_curves.lin_range_min[calibration_curves.peak_label == col] = min(y_c) 
        calibration_curves.lin_range_max[calibration_curves.peak_label == col] = max(y_c) 
        calibration_curves.intercept[calibration_curves.peak_label == col] = y_inter
        calibration_curves.slope[calibration_curves.peak_label == col] = slope
        calibration_curves.N_points[calibration_curves.peak_label == col] = len(x_c)
        calibration_curves.Residual[calibration_curves.peak_label == col] = res
        
    calibration_curves['LLOQ'] = calibration_curves.lin_range_min.apply(lambda x: np.exp(x))
    calibration_curves['ULOQ'] = calibration_curves.lin_range_max.apply(lambda x: np.exp(x))
#         print(len(calibration_curves))
    return calibration_curves


def info_from_Maven(maven_):
    '''this function transform maven results to similar shape to the one of Mint.....'''
    out_df = []
    interm = pd.DataFrame()
        
    for col in maven_.columns[15:]:
        interm = pd.DataFrame()
        interm['ms_file'] = col
        interm['peak_label'] = maven_.compoundId
        interm['ms_file'] = col
        interm['value'] = maven_[col]
        out_df.append( interm )
    
    output = pd.concat(out_df, axis = 0).reset_index(drop = True)
    return output
    
def info_from_Mint(mint_, by):
    '''this function removes unused Mint columns and rename the selected 
    column to value for further calculations.....'''
    
    out_df = mint_[['ms_file', 'peak_label', by]].rename(columns={by:'value'})
    
    return out_df

def info_from_Mint_dense(mint_):
    '''this function reads mint dense shape format dataframe and transforms it to the full results format'''
    
    out_df = mint_.melt(id_vars=["peak_label"],  var_name="cp",  value_name="peak_max")
    out_df.rename(columns={'peak_label':'ms_file', 'cp':'peak_label'}, inplace = True)
    return out_df


def setting_from_stdinfo(std_info, results_):
    ''' this function reads the standard information table 
        and put that info in the results table, 
        the resulting table serves for training purpose'''
    
    output = results_.copy()
    try:
        output.ms_file = output.ms_file.apply(lambda x: os.path.basename(x).replace('.mzXML', ''))
    except:
        pass
#     getting concentration values from the std_info
    output['STD_CONC'] = np.nan
    
    for file in np.unique(output.ms_file):
        for cp in np.unique(output.peak_label):
            try:
#                 print(file)
                output.STD_CONC[(output.ms_file == file) & (output.peak_label == cp)] = \
                std_info[file][std_info.peak_label == cp].iloc[0]
#                 print(cp)
            except:
                continue
#     this will remove the rows corresponding to non-standard samples
    output = output[output['STD_CONC'].notna()]            
    return output        


def training_from_standard_results(std_results, by='peak_max'):
    x_train = std_results[['peak_label', by ]]
    x_train.rename(columns= {by:'value'}, inplace = True)
    y_train = np.array(std_results.STD_CONC)
    
    return x_train, y_train


def conc_from_matrix(matrix):
    '''this function reads a dataframe with the information of the concentrations
    is used on the dataset with the shape of LSARP ......'''
    c = np.array(matrix.columns[1:])
    conc = []
    for i in range(len(c)):
        conc.append(float(c[i][:-2]))
#     print(conc)
    return np.array(conc)



def standard_matrix(mint, by = 'peak_max'):
    mat = mint.crosstab(by).reset_index()
    # instead of get mint result work with a cross tab... fix it
    ## non-standard columns
    ns_cols = []
    for col in mat.columns[1:]: ## start in 1 to keep the peaklabel column
        if ('dard' in col) == False:
            ns_cols.append(col)
    mat = mat.drop(ns_cols, axis = 1)
    
    ## renaming the columns
    new_cols = ['peak_label']
    for col in mat.columns[1:]:
        new_cols.append(col.split('/')[-1].split('dard-')[-1].split('nm')[0] + 'nm')
    mat.columns = new_cols
    
    return mat


def non_standard_matrix(mint, by = 'peak_max'):
    mat = mint.crosstab(by).reset_index()
    ## non-standard columns
#     ns_cols = []
#     for col in mat.columns[1:]: ## start in 1 to keep the peaklabel column
#         if ('dard' in col) == True:
#             ns_cols.append(col)
#     mat = mat.drop(ns_cols, axis = 1)
    
    ## renaming the columns
    new_cols = ['peak_label']
    for col in mat.columns[1:]:
        new_cols.append(col.split('/')[-1])
    mat.columns = new_cols
    
    return mat
        
def to_conc(slope, intercept, point_vector):
    '''this function makes the transformation to log-scale , 
    adds the intercept and makes the back-transformation 
    to linear scale...
    '''
    return np.exp(slope * np.log(point_vector + 0.000000000001) + intercept)

def mint_train_set(mint_results, by = 'peak_max'):
    '''this function takes the results of mint and returns the training X and Y sets 
    as well as the whole dataset with the shape of X'''
    X = mint_results[['peak_label', by]]
    X['value'] = X[by]
    X.drop([by], axis = 1, inplace = True)
    X.reset_index(inplace = True)
    X.drop(['index'], axis = 1, inplace = True)
    X_train = mint_results[mint_results.ms_file.str.contains('Standard')].set_index('ms_file')[['peak_label', by]]
    X_train['value'] = X_train[by]
    X_train.drop([by], axis = 1, inplace = True)
    grab_conc = lambda x: float(x.split('dard-')[-1].split('nm')[0])
    y_train = [ grab_conc(x) for x in X_train.index]
    X_train.reset_index(inplace = True)
    X_train.drop(['ms_file'], axis =1 , inplace = True)
    return X, X_train, np.array(y_train)

     

def transform(X, calibration_curves):
    calibration_curve = calibration_curves[['peak_label', 'slope', 'intercept', 'lin_range_min', 'lin_range_max']]
    X0 = X.copy().fillna(0)
    r_min = 0
    r_max = 0
    
    results = []
    for ndx, (peak_label, slope, intercept, lin_range_min, lin_range_max)\
            in calibration_curve.iterrows():
        
        value = X0.loc[X0.peak_label == peak_label, 'value']
        conc = to_conc(slope, intercept, value)
        inrange = np.ones(len(conc))
        
        df = pd.DataFrame({'value': value, 'pred_conc': conc, 'in_range': inrange})
        
        df.loc[df.pred_conc < np.exp(lin_range_min), 'in_range'] = 0
        df.loc[df.pred_conc > np.exp(lin_range_max), 'in_range'] = 0
        df['peak_label'] = peak_label
       
        results.append(df)
        
    df_conc = pd.concat(results).loc[X0.index, ['peak_label', 'pred_conc', 'in_range']]
    return df_conc

def train_to_validation(X, Y, curves):
    '''this function is to take into cosideration that some points on the training set 
    are out of the linear range and therefore should not be taken into consideration for
    the scoring'''
    X0 = X.copy()
    X0['true_conc'] = Y
    
    curves0= curves.copy().fillna(0.0000000000001)
    curves0['Y_min'] = np.exp( curves0.lin_range_min)
    curves0['Y_max'] = np.exp( curves0.lin_range_max)
    
    X0['Y_min'] = 0.0
    X0['Y_max'] = 0.0
    
    for cp in np.unique(X0.peak_label):
        X0.Y_min[X0.peak_label == cp] = curves0.Y_min[curves0.peak_label == cp].iloc[0]
        X0.Y_max[X0.peak_label == cp] = curves0.Y_max[curves0.peak_label == cp].iloc[0]
        
    X0.loc[X0.true_conc < X0.Y_min, 'true_conc'] = None
    X0.loc[X0.true_conc > X0.Y_max, 'true_conc'] = None
    
    return np.array(X0.true_conc)
        
        
def rmsd(col1, col2):
    colt = np.maximum(col1, col2)
    return np.sum((col1-col2)*(col1-col2)/(len(col1)*colt*colt))

# this function turns the matrix from horizontal
def matrix_transpose(matrix):
#     transforming the matrix to work with columns
#     im trying to assign values to the rows but it didnt work
    result = matrix.T
    result.columns = result.iloc[0]
    return result[1:]


def fitting_score(est_conc , true_corr_conc):
    '''this function will compute the score accounting for the differences between '''
    result = pd.DataFrame({'peak_label': np.unique(est_conc.peak_label)})
#     result['peak_label'] = matrix1.peak_label
    est_conc_c = est_conc.copy()
    est_conc_c['true_corr_conc'] = true_corr_conc
    est_conc_c = est_conc_c.dropna()
    Rmsd = []
    x1 = []
    x2 = []
    for metab in np.unique(est_conc_c.peak_label):
#         print(metab)
#         print(np.array(Rmsd(matrix1[metab], concentrations)))
        x1 = np.array(est_conc_c.pred_conc[est_conc_c.peak_label == metab])
        x2 = np.array(est_conc_c.true_corr_conc[est_conc_c.peak_label == metab])
#         print(x2)
        Rmsd.append(1 - rmsd(x1, x2))
    result['score'] = Rmsd
    return result
