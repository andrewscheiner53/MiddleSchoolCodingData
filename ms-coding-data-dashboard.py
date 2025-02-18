#Packages
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#Set page config (only once, first command)
st.set_page_config(
    page_title="Middle School Participation in CS",
    page_icon=":school:",
    layout="wide",
    initial_sidebar_state="expanded")

#Title test
st.title('Middle School Participation in CS Data Dashboard')
st.write('An interactive Streamlit dashboard visualizing \
          recent trends in both participation and access data across \
          related to middle school computer science education in the \
          United States. Collected from Code.org, this dashboard shows \
         exploratory data analysis amongst demographics across the country \
         with the choropleth map helping highlight important findings in \
            the data. Designed by Andrew Scheiner.')

alt.themes.enable("dark")

#Load in data
# Load the entire workbook
excel_file_path = 'MiddleSchoolData.xlsx'
xl = pd.ExcelFile(excel_file_path)

# If you want to read all sheets into a dictionary of DataFrames
dfs = {sheet_name: xl.parse(sheet_name) for sheet_name in xl.sheet_names}

#store data on state and year its data was collected
yearData = dfs['Most Recent Access Data'][['State','School Year']]

#user chooses which data to see
data_option = st.selectbox(
    "Which data topic would you like to see?",
    (xl.sheet_names)
)
st.write("You selected:", data_option)

#replace "-" with 0s
selected_data = dfs[data_option].replace("-", 0)

#df for selected data
selected_data_pct = selected_data.copy()
selected_data_tot = selected_data.copy()
#keep only state and pct
selected_data_pct = selected_data_pct.filter(regex='^(Percent|State)')
#keep only state and totals
selected_data_tot = selected_data_tot.filter(regex='^(State|Total|Number)')
#get columns, remove state
selected_data_pct_cols = selected_data_pct.columns[1:]

#EDA for selected data
# Create two columns
col1, col2 = st.columns(2)
# Display dataframes in separate columns
with col1:
    st.subheader('Summary of Percentage Data')
    st.dataframe(selected_data_pct.describe())
with col2:
    st.subheader('Summary of Totals Data')
    st.dataframe(selected_data_tot.describe())

#column option per df
col_option = st.selectbox(
    f"Which data for {data_option} would you like to see plotted on the map?",
    (selected_data_pct.columns[1:])
)
st.write("You selected:", col_option)

#choropleth map fx
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale=input_color_theme,
                               range_color=(input_column.min(), input_column.max()),
                               scope="usa"
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    choropleth.update_layout(coloraxis_colorbar=dict(
        title="Percentage [0,1]"
    ))
    return choropleth

chorop1 = make_choropleth(selected_data_pct, selected_data_pct['State'],\
                selected_data_pct[col_option],\
                    'greens')

col3, col4 = st.columns([1,2.5])
with col3:
    st.subheader('Year Each State Collected Their Data')
    st.dataframe(yearData)
with col4:
    st.subheader('USA Map of Selected Data')
    st.plotly_chart(chorop1, use_container_width=True)

st.write("© Andrew Scheiner 2025")