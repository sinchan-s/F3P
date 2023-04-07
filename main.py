
#! important librabries
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

#! basic configurations
st.set_page_config(
    page_title="F3P Main",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

#! Clean Footer
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden;}
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

#! seaborn graph styling
sns.set_style('darkgrid')

#! reading the source file
df = pd.read_csv("main_data.csv")
cover_df = pd.read_csv("Coverage data.csv")

#! an apt heading
st.header("Fabric Physical Parameters Predictor")

#! column-wise split: article selection & finish-style selection
col1, col2, col3 = st.columns(3)

all_articles = df['Article No.'].unique()
with col1:
    article_selectbox = st.selectbox("Select Article:", all_articles)
article_df = df[df['Article No.']==article_selectbox]
with col2:
    finish = st.multiselect("Select Finish Code:", article_df.Finish.unique(), default=article_df.Finish.unique()[0], help="Select one or more finish codes to see the data table")
with col3:
    style = st.radio("Select Style:", article_df.Style.unique())


#! column-wise split: weave display & warp-weft count display
col1, col2, col3 = st.columns(3)
weave = article_df.Weave.unique()[0]
gsm = article_df.GSM.unique()[0]
count_data = article_df['Warp*Weft'].unique()[0].split("*")         #? splits into a list of warp & weft count
tpi_data = article_df['EPI*PPI'].unique()[0].split("*")             #? splits into a list of EPI & PPI
with col1:
    st.metric('Weave || GSM', weave+' || '+str(gsm))                #? diplay weave & gsm
with col2:
    st.metric('Warp || Weft', count_data[0]+' || '+count_data[1])   #? display warp-weft count
with col3:
    st.metric('EPI || PPI', tpi_data[0]+' || '+tpi_data[1])         #? display epi & ppi

#! dataframes merger
selection_df = df.loc[(df['Article No.']==article_selectbox)&(df['Finish'].isin(finish))&(df['Style']==style)]

#! plotting function
def box_plot(df_select, x, y, palette, title, std):
    fig = plt.figure(figsize=(8, 3))
    value_to_plot = sns.boxplot(data=df_select, x=x, y=y, showcaps=False, width=0.5, linewidth=2, whis=1, palette=palette).set(title=title)
    mean_val = df_select[x].mean()
    std_mean_val = df_select[std].mean()
    plt.axvline(mean_val, c='m', ls='--', lw=3)
    plt.axvline(std_mean_val, c='r', ls='-', lw=1)
    #*fig.plot(x = 13, color = 'b', label = '12')
    st.pyplot(fig)

#! tabular construct
tab1, tab2 = st.tabs(["Parameter Plots", "Article Tabular Data"])
    
#! column-wise split: graphical charts
try:
    with tab1:
        tab1.subheader(f'Tear Strength')
        col1, col2 = tab1.columns(2)
        sorted_cover_group = selection_df.sort_values(by=["Coverage group"], ascending=False)
        with col1:
            warp_tear = box_plot(selection_df, 'Warp Tear', sorted_cover_group['Coverage group'], 'winter', 'Warp Tear Range','STD_Warp_Tear')
        with col2:
            weft_tear = box_plot(selection_df, 'Weft Tear', sorted_cover_group['Coverage group'], 'rocket', 'Weft Tear Range','STD_Weft_Tear')

        tab1.subheader(f'Tensile Strength')
        col1, col2 = tab1.columns(2)
        with col1:
            warp_tensile = box_plot(selection_df, 'Warp Tensile', sorted_cover_group['Coverage group'],  'winter', 'Warp Tensile Range','STD_Warp_Tensile')
        with col2:
            weft_tensile = box_plot(selection_df, 'Weft Tensile', sorted_cover_group['Coverage group'],  'rocket', 'Weft Tensile Range','STD_Weft_Tensile')

        tab1.subheader(f'Stretch Parameters')
        col1, col2 = tab1.columns(2)
        with col1:
            growth = box_plot(selection_df, 'Growth', sorted_cover_group['Coverage group'], 'rocket', 'Growth Range', 'Growth')
        with col2:
            elongation = box_plot(selection_df, 'Elongation', sorted_cover_group['Coverage group'], 'winter', 'Elongation Range', 'Elongation')
except ValueError:
    with tab1:
        st.subheader('< no data to display 😵 >')

#! article dataframe display
with tab2:
    st.write(f'Article Selected: {article_selectbox}')
    st.dataframe(selection_df)