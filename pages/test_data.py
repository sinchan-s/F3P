# ! important librabries
import re
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# ! basic configurations
st.set_page_config(
    page_title="testing domain",
    page_icon="❓",
    layout="wide",
    initial_sidebar_state="collapsed")

#! Clean Footer
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden;}
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# ! reading the source file
df = pd.read_csv("main_params_data.csv")
main_df = df.dropna(subset=['Warp Tear    (ASTMD1424)'])

# ! conditional columns
main_df['style'] = [
    'Pigment' if x.startswith('P') or x.startswith('DU') else 'Reactive' if x.startswith('R') else 'Discharge' for x in
    main_df['Print Color']]

# ! an apt heading
st.header("experimentation tab")

#! dropdown lists & dicts
spin_dict = {'All': '\D+',
            'Carded':'K',
            'Carded Compact': 'K.COM', 
            'Combed': 'C', 
            'Combed Compact': 'C.COM', 
            'Vortex':'VOR',
            'Open-End':'OE'}
# all_weaves = articles_df['Weave'].unique()
count_list = [6, 7, 8, 10, 12, 14, 15, 16, 20, 21, 30, 32, 40, 45, 60, 80, 100]
fibre_dict = {'All':"", 'Viscose':"VIS", 'Modal':"MOD", 'CVC':"CVC", 'Polyester':"PET", 'PC-Blend':"PC", 'Nylon':"NYL", 'Spandex/Lycra':"SPX", 'Lyocell':"LYC", 'Organic Cotton':"OG", 'Recycled Cotton':"RECY", 'Multi-Count':"MC"}
weave_list = ['', 'PLAIN', 'TWILL', 'SATIN', 'DOBBY', 'CVT', 'MATT', 'HBT', 'BKT', 'OXFORD', 'DOUBLE CLOTH', 'BEDFORD CORD', 'RIBSTOP', 'WEFTRIB']
effect_dict = {'Normal': "", 'Seer Sucker': 'SUCKER', 'Crepe': 'CREPE', 'Butta-Cut': 'FIL-COUPE', 'Crinkle': 'CRINKLE', 'Slub':"MC"}


#! QTX file uploader
uploaded_file = st.file_uploader("Upload csv format file only:", type=['csv'], accept_multiple_files=False, help="Only upload CSV file")

#! dataframe display
try:
    data_file = pd.read_csv(uploaded_file)
    col_list = list(map(str.lower, data_file.columns))
    if 'construction' in col_list:
        const_index = col_list.index('construction')
        # st.write(const_index)
        data_file['WARP'] = data_file.iloc[:, const_index].str.extract(r'^([\d\w\s+.\/()]*)[*]')
        data_file['WEFT'] = data_file.iloc[:, const_index].str.extract(r'^[\d\w\s+.\/()]*[*]([\d\w\s+.\/()]+)')
        data_file['EPI'] = data_file.iloc[:, const_index].str.extract(r'[-](\d{2,3})[*]')
        data_file['PPI'] = data_file.iloc[:, const_index].str.extract(r'[*](\d{2,3})[-]')
        data_file['WIDTH'] = data_file.iloc[:, const_index].str.extract(r'[-*](\d{3}\.?\d{0,2})-')
        data_file['WEAVE'] = data_file.iloc[:, const_index].str.extract(r'-(\d?\/?\d?[,\s]?[A-Z]+\s?[A-Z]*\(?[A-Z\s]+\)?)')
        data_file['GSM'] = data_file.iloc[:, const_index].str.extract(r'[-\s](\d{3}\.?\d?)[\s$]*$')
        tab1, tab2 = st.tabs(["Selection Data","File Data"])
        with tab1:
            col1, col2, col3 = st.columns(3)
            
            #! selection parameters
            with col1:
                with st.expander('Select Warp Parameters'):
                    warp_fibre_select = st.selectbox("Fibre", list(fibre_dict), help="Dropdown list of fibres used in warp")
                    warp_count_select = str(st.select_slider("Count", count_list, help="Count selector: Warp"))
                    warp_spin_select = st.selectbox("Spin-tech", list(spin_dict),  help="Spinning technology of warp")
                    warp_ply_check = st.checkbox(f'2/{warp_count_select}', key=1, help="Check for doube ply warp yarn")
                    if warp_ply_check:
                        warp_value = '2/' + warp_count_select
                    else:
                        warp_value = warp_count_select
                    warp_regex = '^'+warp_value+spin_dict.get(warp_spin_select)
                same_for_weft = st.checkbox('Same parameters for Weft')
            with col2:
                with st.expander('Select Weft Parameters'):
                    weft_fibre_select = st.selectbox("Fibre", list(fibre_dict), help="Dropdown list of fibres used in weft")
                    weft_count_select = str(st.select_slider("Count", count_list, help="Count selector: Weft"))
                    weft_spin_select = st.selectbox("Spin-tech", list(spin_dict),  help="Spinning technology of weft")
                    weft_ply_check = st.checkbox(f'2/{weft_count_select}', key=2, help="Check for doube ply weft yarn")
                    if same_for_weft:
                        weft_regex = warp_regex
                    else:
                        if weft_ply_check:
                            weft_value = '2/' + weft_count_select
                        else:
                            weft_value = weft_count_select
                        weft_regex = '^'+weft_value+spin_dict.get(weft_spin_select)
            with col3:
                with st.expander('Select Fabric Construction'):
                    epi_range = st.slider('EPI range', 50, 210, (60, 150))
                    ppi_range = st.slider('PPI range', 50, 200, (60, 150))
                    weave_selectbox = st.selectbox("Weave", weave_list, help="Select the fabric weave")
                    effect_selectbox = st.selectbox("Effect", list(effect_dict), help="Select any special effect on fabric")

            #! selecting data based on above parameters
            selection_df = data_file[data_file['WEAVE'].str.contains(weave_selectbox) &
                                    data_file['WEAVE'].str.contains(effect_dict.get(effect_selectbox)) & 
                                    data_file['WARP'].str.contains(warp_regex) &
                                    data_file['WARP'].str.contains(fibre_dict.get(warp_fibre_select)) & 
                                    data_file['WEFT'].str.contains(weft_regex) & 
                                    data_file['WEFT'].str.contains(fibre_dict.get(weft_fibre_select))]

            selection_df = selection_df[selection_df['EPI'].between(epi_range[0], epi_range[1]) & selection_df['PPI'].between(ppi_range[0], ppi_range[1])]
            # selection_df = selection_df.iloc[:, 0:2].set_index('K1')
            df_display = st.table(selection_df)
        with tab2:
                st.dataframe(data_file)

except:
    st.write("Upload a file !")