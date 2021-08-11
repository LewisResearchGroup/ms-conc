from ms_mint_conc import calibration_curves as cc
from ms_mint_conc import ConcentrationEstimator as CE
from ms_mint_conc import AppState as AS
from ms_mint_conc import SessionState
from ms_mint_conc.SessionState import get

import os
import pandas as pd
import datetime
import numpy as np
import glob
import re
import altair as alt

import streamlit as st
import base64
from io import BytesIO


def heav(x):
    if x > 0.0:
        return 1.0
    return 0.5

def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


# st.image('linear_range_finder.png', width=800)

st.write('''
         # APP for computing the concentrations by using standard curves
         
         ### this app should be able to process both Mint and Maven results ....
         ####    1) A table with the information of standard samples (metadata) is requiered alongside with the metabolomic results. Upload them by clicking in the left side buttons  
         ####    --> the table should contain the file names of standard samples as column names (without the file extension)
         ####    --> the first column correspond to the peak labels for the metabolites in the standard samples
         ####    --> please make sure that the metabolites in the metadata agree with the metabolites on the results table
         ''')

st.image('picture_4_app.png', width=700, caption = 'Figure 1 example of metadata information table. The file names should be contained in the column names. The column `peak_label` correspond to the compounds in the standard samples.')

st.write('''
         ####    2) When the metadata and the results files are uploaded, a table with the parameters of standard curves and the results with the transformations will be generated automatically
         ####    3) In the case that Mint program is used to generate the results, a selection tab will pop up for selecting the parameter for the intensity measurement, `peak_max` is the defalult value
         ####    4) In the last section you can visulize the standard curves and the linear ranges predicted for each one (dark blue dots)
         ''')
# state = AS.AppState()
st.sidebar.write( '## 1) please upload standard information file ..')
std_info = st.sidebar.file_uploader( 'upload standard information file ..')


try:
    s_st = SessionState.get(std_information = pd.read_csv(std_info))
    st.write('## your standard samples metadata file:')
    st.write(s_st.std_information)
except:
    st.write('## no information file have being uploaded')
    
    
st.sidebar.write('## 2) please upload the dataset and select the program used to generating it')
results_file = st.sidebar.file_uploader("upload the results file ..")

try:
    s_st.raw_results = pd.read_csv(results_file)
    st.write('## your metabolomic results file:')
    st.write(s_st.raw_results)
    
    s_st.program = st.selectbox('''select the program used for generating the data''' , ('Mint', 'Maven'))
    
    if s_st.program == 'Mint':
        s_st.std_results = cc.setting_from_stdinfo(s_st.std_information, s_st.raw_results)
        st.write('''please select the intensity measurement..
                    peak_max will be used as default value''')
        try:
            s_st.by_ = st.selectbox('intensity measurement',('peak_max', 'peak_area'))
        except:
            s_st.by_ = 'peak_max'
        
        s_st.std_results.sort_values(by = ['peak_label','STD_CONC', s_st.by_ ], inplace = True)
        
    if s_st.program == 'Maven':
        s_st.by_ = 'value'
#     ## this line will transform the maven table to the shape of Mint.....
        s_st.raw_results = cc.info_from_Maven(s_st.raw_results)
        s_st.std_results = cc.setting_from_stdinfo(s_st.std_information, s_st.raw_results)
        s_st.std_results.sort_values(by = ['peak_label','STD_CONC', s_st.by_ ], inplace = True)

        
except:
    st.write('## no results file have being uploaded')

try:
    if len(s_st.std_results) > 1:
        s_st.ces = CE.ConcentrationEstimator()
        s_st.x_train, s_st.y_train = cc.training_from_standard_results(s_st.std_results, by = s_st.by_)
    
        s_st.ces.fit(s_st.x_train, s_st.y_train)
        st.write('''the standard curves have being fitted ....
             you can download the parameters of the standard curves....''')
        s_st.linear_scale_parameters = s_st.ces.params_.sort_values(by = ['peak_label']).drop(['slope', 'intercept','lin_range_min', 'lin_range_max'], axis = 1)
        st.write(s_st.linear_scale_parameters)
        
        tmp_download_link = download_link(s_st.linear_scale_parameters, 'parameters.csv', 'Click here to download your standard courves results!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)
            
        
        s_st.X = s_st.raw_results[['ms_file','peak_label', s_st.by_]].rename(columns={s_st.by_:'value'})
#    st.write(s_st.X.sort_values(by = ['peak_label']))
        s_st.X['pred_conc'] = s_st.ces.predict(s_st.X).pred_conc
#     st.write(s_st.X)
#         X['pred_conc'] = ces.predict(X).pred_conc
        st.write(s_st.X)
        tmp_download_link = download_link(s_st.X, 'results.csv', 'Click here to download transformed data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)
        
except:
    st.write('## there are no results to show')
    

try:
    s_st.cp = st.selectbox('select the compound \n' + 
                           s_st.x_train.peak_label.iloc[0] +
                           ' will be used by default', list(np.unique(s_st.x_train.peak_label)))
    st.write(s_st.cp)


    s_st.viz_restult = st.button('''plot results''')

    if s_st.viz_restult:
        
        y_train_corrected = cc.train_to_validation(s_st.x_train, s_st.y_train, s_st.ces.params_ )
        x_viz = s_st.x_train.copy()
    
        x_viz['Concentration'] = s_st.y_train
    
        x_viz['Corr_Concentration'] = y_train_corrected
    
        x_viz = x_viz.fillna(-1.0)
    
        x_viz['in_range'] = x_viz.Corr_Concentration.apply(lambda x: heav(x))

        c = alt.Chart(x_viz[x_viz.peak_label == s_st.cp]).mark_circle().encode(alt.X('Concentration', scale=alt.Scale(type='log')), 
                      alt.Y('value', scale=alt.Scale(type='log')), color='in_range').configure_axis(grid=False, domain=False)
        st.write(c)
except:
    st.write('')