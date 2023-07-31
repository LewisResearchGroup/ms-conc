import pandas as pd


class AppState():
    def __init__(self):
        self.standard_info = pd.DataFrame()
        self.raw_results = pd.DataFrame()
        self.program = 'Mint'
        self.int_par = 'peak_max'
        self.transf_results = pd.DataFrame()
        self.parameters = pd.DataFrame()
        self.transfomed_results = pd.DataFrame()
        
    def get_std_info(self, std_):
        self.standard_info = std_

    def get_raw_result(self, raw_):
        self.raw_results = raw_
        
    def get_program(self, prog):
        self.program = prog
        
    def get_int_par(self, parameter):
        self.int_par = parameter
        
    def get_transf_resutls(self, trans_results):
        self.transf_results = trans_results
        
    def get_parameters(self, params):
        self.parameters = params
        
    def get_transformed_results(self, t_res):
        self.transfomed_results = t_res