#Packages
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#Set page config (only once, first command)
st.set_page_config(
    page_title="Middle School Coding Data Dashboard",
    page_icon=":school:",
    layout="wide",
    initial_sidebar_state="expanded")

#Title test
st.write('Middle School Coding Data Dashboard')

alt.themes.enable("dark")

#Load in data
# Load the entire workbook
excel_file_path = 'MiddleSchoolData.xlsx'
xl = pd.ExcelFile(excel_file_path)

# List all sheet names
st.write(xl.sheet_names)

# Read a specific sheet into a DataFrame
#df_sheet1 = pd.read_excel(excel_file_path, sheet_name='Sheet1')

# If you want to read all sheets into a dictionary of DataFrames
dfs = {sheet_name: xl.parse(sheet_name) for sheet_name in xl.sheet_names}

#EDA for most recent access data
mostRecentAccessData = dfs['Most Recent Access Data']
st.write(mostRecentAccessData.describe())

#choropleth map fx
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, 1),
                               scope="usa"
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth

chorop1 = make_choropleth(mostRecentAccessData, mostRecentAccessData['State'],\
                mostRecentAccessData['Percent of Schools that Provided Data'],\
                    'greens')
st.plotly_chart(chorop1, use_container_width=True)