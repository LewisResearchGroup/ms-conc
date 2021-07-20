from . import calibration_curves as cc
import pandas as pd
class ConcentrationEstimator():
    def __init__(self):
        self.params_ = pd.DataFrame()
#         self.x_var = x_var
        
    def fit(self, X, y):
        self.params_ = cc.calibration_curves( X , y)
#         pass
#       X here should be the same shape.... 
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