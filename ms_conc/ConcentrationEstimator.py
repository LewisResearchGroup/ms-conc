from . import calibration_curves as cc
import pandas as pd
class ConcentrationEstimator():
    def __init__(self):
        self.params_ = pd.DataFrame()
        self.interval = [0.5,2]
#     def fit(self, X, y):
#         self.params_ = cc.calibration_curves( X , y)
    def set_interval(self, interval):
        self.interval = interval
        
    def fit(self, X, y, v_slope = 'fixed'):
        if v_slope == 'interval':
            self.params_ = cc.calibration_curves_variable_slope_interval( X, y, self.interval)
        if v_slope == 'wide':
            self.params_ = cc.calibration_curves_variable_slope( X , y)
        if v_slope == 'fixed':
            self.params_ = cc.calibration_curves( X , y)
            
    def predict(self, X):
        return cc.transform(X, self.params_ )
#         pass
        
    def score(self, y_pred, y_true):
#         X is the matrix of standard curves.....
        return cc.fitting_score( y_pred , y_true) 
#         pass
    
#     def load(self, fn = 'MINT-conc-parameters.csv'):
#         self.params_ = pd.read_csv(fn)
    
#     def save(self, fn = 'MINT-conc-parameters.csv')
#         self.params_.to_csv(fn)