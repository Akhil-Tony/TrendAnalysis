import streamlit as st
import pandas as pd
import plotly.express as px
import pipreqs
#********* Data Cleaning **************************
filename = 'IBM ICE- Consolidated Student Count.xlsx'
main_data = pd.read_excel(filename)
main_data['University'].ffill(inplace=True)
null_idx = main_data[main_data['Batch'].isnull()].index
main_data.drop(index=null_idx,inplace=True)
main_data.drop(columns='Total',inplace=True)
main_data.Batch = main_data.Batch.astype(dtype="category")
main_data.University = main_data.University.astype(dtype='category')
main_data.iloc[:,2:] = main_data.iloc[:,2:].fillna(value=0)
main_data.iloc[:,2:] = main_data.iloc[:,2:].astype(dtype='int')
#*************** Plotting Functions **********************
def students_per_course(data):
    courses = data.iloc[:,2:].sum(axis=0).index
    students = data.iloc[:,2:].sum(axis=0).values
    count_df = pd.DataFrame({'course':courses,'no of students':students})
    fig = px.pie(count_df,values='no of students',names='course',title='No of Students Per Course')
    fig.update_traces(textposition = 'inside', textinfo='percent+label')
    return fig
def students_per_batch(data):
    hist = data.groupby(['Batch','University']).sum().sum(1).unstack('University').sum(1)
    if any(hist.values):
        hist = hist + .1
    else:
        pass

    fig = px.histogram(x=hist.index,y=hist,height=450,width=610,
    title="Students Per Batch",
    color_discrete_sequence=['skyblue'])
    fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="skyblue" ) )
    return fig
#*****************************************
Universities = list(main_data.University.unique())
Universities.insert(0,'All')
selected_uni = st.selectbox(label = "SELECT THE UNIVERSITY" ,options = Universities)

if selected_uni != 'All':
    st.write(students_per_course(main_data[main_data.University==selected_uni]))
    st.write(students_per_batch(main_data[main_data.University==selected_uni]))
else:
    st.write(students_per_course(main_data))
    st.write(students_per_batch(main_data))