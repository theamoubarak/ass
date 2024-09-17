import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Streamlit app configuration
st.set_page_config(page_title=" % of Men vs Women in Lebanon")
st.title("% of Men and Women in Lebanon")

# Load the data
path = "https://linked.aub.edu.lb/pkgcube/data/6ccc6616fbb484c599a4cc560b934c25_20240906_090000.csv"
df = pd.read_csv(path)

# 1. Bar Chart: Percentage of Women in Lebanese Villages
st.title("Percentage of Women in Lebanese Villages")

p1 = go.Bar(x=df['Village'], y=df['Women_Percentage'])
layout = go.Layout(
    yaxis=dict(range=[0, 100]),
    title='Bar Graph showing the Percentage of Women Within Lebanese Villages'
)
fig = go.Figure(data=[p1], layout=layout)
st.plotly_chart(fig)

# 2. Pie Chart: Family Size Distribution
# Make sure the columns you're accessing exist and are used correctly
# Example of accessing relevant family size columns
family_size_cols = ['Family_4_to_6_members', 'Family_7_or_more_members', 'Family_1_to_3_members']
if all(col in df.columns for col in family_size_cols):
    c1 = df['Family_4_to_6_members'].sum()
    c2 = df['Family_7_or_more_members'].sum()
    c3 = df['Family_1_to_3_members'].sum()
    Counts = [c1, c2, c3]
    Names = ['4 to 6 members', '7 or more members', '1 to 3 members']

    p2 = go.Pie(labels=Names, values=Counts)
    layout = go.Layout(title='Pie Chart showing the Family Size Distribution Among Lebanese Villages')
    fig = go.Figure(data=[p2], layout=layout)

    st.title("Family Size Distribution in Lebanese Villages")
    st.plotly_chart(fig)
else:
    st.error("Required family size columns are not available in the dataset.")

# 3. Bubble Chart: Percentage of Elderly and Youth Population based on Percentage of Women
# Ensure the necessary columns exist in the dataframe
if all(col in df.columns for col in ['Percentage_Elderly', 'Percentage_Youth', 'Population_Size', 'Percentage_Women', 'Village']):
    x = df['Percentage_Elderly']
    y = df['Percentage_Youth']
    size = df[df['Population_Size'] <= 100]['Population_Size']  # Size based on population <= 100
    color = df['Percentage_Women']

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
        text=df['Village']
    )

    layout = go.Layout(
        title='Bubble chart showing the Percentage of Elderly and Youth Population based on Percentage of Women Within Lebanese Villages',
        xaxis_title='Percentage of Elderly',
        yaxis_title='Percentage of Youth'
    )

    fig = go.Figure(data=[p3], layout=layout)
    st.title("Interactive Bubble Chart")
    st.plotly_chart(fig)
else:
    st.error("Necessary columns for the bubble chart are missing in the dataset.")

# 4. Scatter Plot: % Men vs % Women in Villages
# Ensure the necessary columns exist
if all(col in df.columns for col in ['Men_Percentage', 'Women_Percentage', 'Village']):
    men = df['Men_Percentage']
    women = df['Women_Percentage']
    cities = df['Village']

    # Scatter plot
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

    fig.update_layout(
        title='Scatter plot % Men vs. % Women in Villages',
        xaxis_title='Men (%)',
        yaxis_title='Women (%)',
        xaxis=dict(range=[0, max(men) * 1.1]),
        yaxis=dict(range=[0, max(women) * 1.1])
    )

    st.plotly_chart(fig)
else:
    st.error("Columns for the scatter plot (% Men and % Women) are missing in the dataset.")
