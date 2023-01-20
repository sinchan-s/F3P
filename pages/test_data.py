# ! important librabries
import re
import pandas as pd
import streamlit as st
import seaborn as sns
from io import StringIO
import matplotlib.pyplot as plt

# ! basic configurations
st.set_page_config(
    page_title="testing domain",
    page_icon="❓",
    layout="wide",
    initial_sidebar_state="collapsed")

# ! seaborn graph styling
sns.set_style('darkgrid')

# ! reading the source file
df = pd.read_csv("main_params_data.csv")
main_df = df.dropna(subset=['Warp Tear    (ASTMD1424)'])

# ! conditional columns
main_df['style'] = [
    'Pigment' if x.startswith('P') or x.startswith('DU') else 'Reactive' if x.startswith('R') else 'Discharge' for x in
    main_df['Print Color']]

# ! an apt heading
st.header("experimentation tab")

# ! column-wise split: article selection & finsih-style selection
col1, col2, col3 = st.columns(3)

try:
    all_articles = main_df['Article No.'].unique()
    article_selectbox = col1.multiselect("Select Article:", sorted(all_articles), default=all_articles[0],
                                         help="Choose one or more articles to see the data table")
    article_df = main_df[main_df['Article No.'].isin(article_selectbox)]
    finish = col2.multiselect("Select Finish Code:", article_df.Pattern.unique(),
                              default=article_df.Pattern.unique()[0],
                              help="Choose one or more finish codes to see the data table")
    style = col3.radio("Select Style:", article_df['style'].unique(), help="Choose any print style")
    # st.write(f"debug : {finish}")
    selection_df = main_df.loc[(main_df['Article No.'].isin(article_selectbox)) & (main_df['Pattern'].isin(finish)) & (
            main_df['style'] == style)]
except:
    st.error("Please select data to display 👆")

# ! dataframe display
with st.expander("Data Tables", expanded=False):
    tab1, tab2 = st.tabs(["Selected Data", "All Data"])
    try:
        df_display = tab1.dataframe(selection_df)
    except:
        st.warning("No data to show but still you can see All Data")
    finally:
        df_display = tab2.dataframe(main_df)

# QTX file uploader
qtx_file = st.file_uploader("Upload QTX format file only:", type=['qtx'], accept_multiple_files=False,
                            help="Only upload QTX file")

# QTX file opener
try:
    # converting qtx data to raw string
    stringio = StringIO(qtx_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    with st.expander('Raw data: ', expanded=False):
        st.write(string_data)
    # values extraction using regex
    std_name = re.findall("STD_NAME=(.+)", string_data)
    list_ref_low = re.findall("STD_REFLLOW=(\d+),", string_data)
    list_ref_pts = re.findall("STD_REFLPOINTS=(\d+),", string_data)
    list_ref_int = re.findall("STD_REFLINTERVAL=(\d+),", string_data)
    list_ref_vals = re.findall("STD_R[=,](.+)", string_data)
    # color std selection & graph display
    name_select = st.selectbox("Select Color", std_name)
    std_i = std_name.index(name_select)
    ref_low, ref_pts, ref_int = int(list_ref_low[std_i]), int(list_ref_pts[std_i]), int(list_ref_int[std_i])
    ref_max = ref_low + ref_pts * ref_int
    y_ref_val_list = str(list_ref_vals[std_i]).split(',')
    x_wave_list = [k for k in range(ref_low, ref_max, ref_int)]
    sd_df = pd.DataFrame(y_ref_val_list, index=x_wave_list, columns=[name_select])
    sd_df[name_select] = sd_df[name_select].astype('float64')
    st.line_chart(sd_df)
except:
    st.write("Upload a file !")