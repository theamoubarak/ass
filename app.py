import pandas as pd
import numpy as np
import scipy as sp
import plotly.offline as py
import plotly.figure_factory as ff
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title=" %of Men vs Women in Lebanon")
st.title("% of Men and Women in Lebanon")

path="https://linked.aub.edu.lb/pkgcube/data/6ccc6616fbb484c599a4cc560b934c25_20240906_090000.csv"
df= pd.read_csv(path) 

data = {'Village': ['Village A', 'Village B', 'Village C'],
        'Women_Percentage': [75, 60, 85]}
df = pd.DataFrame(data)

p1 = [go.Bar(x=df['Village'], y=df['Women_Percentage'])]
layout = go.Layout(yaxis=dict(range=[0, 100]), title='Bar Graph showing the Percentage of Women Within Lebanese Villages')
fig = go.Figure(data=p1, layout=layout)

st.title("Percentage of Women in Lebanese Villages")
st.plotly_chart(fig)

c1 = (df.iloc[:, 0] == 1).sum()  # Count of families with 4 to 6 members
c2 = (df.iloc[:, 1] == 1).sum()  # Count of families with 7 or more members
c3 = (df.iloc[:, 2] == 1).sum()  # Count of families with 1 to 3 members
Counts = [c1, c2, c3]
Names = ['4 to 6 members', '7 or more members', '1 to 3 members']

p2 = go.Pie(labels=Names, values=Counts)
layout = go.Layout(title='Pie Chart showing the Family Size Distribution Among Lebanese Villages')
fig = go.Figure(data=[p2], layout=layout)

st.title("Family Size Distribution in Lebanese Villages")
st.plotly_chart(fig)

x = df['Percentage_Elderly']
y = df['Percentage_Youth']
size = df[df['Population_Size'] <= 100]['Population_Size']  # Size based on population <= 100
color = df['Percentage_Women']

# Create the bubble chart
p3 = go.Scatter(
    x=x,
    y=y,
    mode='markers',
    marker=dict(
        size=size,
        opacity=0.6,
        color=color,
        colorscale='Viridis',
        colorbar=dict(title='Percentage of Women')
    ),
    text=df['Village_Name']
)

layout = go.Layout(
    title='Bubble chart showing the Percentage of Elderly and Youth Population based on Percentage of Women Within Lebanese Villages',
    xaxis_title='Percentage of Elderly',
    yaxis_title='Percentage of Youth'
)

fig = go.Figure(data=[p3], layout=layout)


st.title("Interactive Bubble Chart")
st.plotly_chart(fig)

women = df['Women_Percentage']
men = df['Men_Percentage']
cities = df['Village_Name']

# Create the scatter plot
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=men, 
    y=women, 
    mode='markers', 
    text=cities, 
    textposition='top center',
    marker=dict(
        size=12,
        color='blue',
        line=dict(width=2, color='black')
    ),
    hoverinfo='text'
))

# Update layout for the plot
fig.update_layout(
    title='Scatter plot % Men vs. % Women in Villages',
    xaxis_title='Men (%)',
    yaxis_title='Women (%)',
    xaxis=dict(range=[0, max(men) * 1.1]),
    yaxis=dict(range=[0, max(women) * 1.1])
)

# Display the scatter plot in Streamlit
st.title("Interactive Scatter Plot: % Men vs. % Women in Villages")
st.plotly_chart(fig)

