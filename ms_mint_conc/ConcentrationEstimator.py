from . import calibration_curves as cc
import pandas as pd
class ConcentrationEstimator():
    def __init__(self):
        self.params_ = pd.DataFrame()
        
#     def fit(self, X, y):
#         self.params_ = cc.calibration_curves( X , y)

    def fit(self, X, y, v_slope = False):
        if v_slope:
            self.params_ = cc.calibration_curves_variable_slope( X , y)
        else:
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