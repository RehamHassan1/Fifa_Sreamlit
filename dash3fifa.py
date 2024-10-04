import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("fifa_eda.csv")
df = load_data()

player_count = df.groupby('Nationality')['Name'].count().reset_index()
player_count.columns = ['Country', 'Player_Count']
average_rating_by_position = df.groupby('Position')['Overall'].mean().reset_index()
average_rating_by_position = average_rating_by_position.sort_values(by='Overall', ascending=False)
positions = df['Position'].unique()

st.title("FIFA Player Distribution Dashboard")

tab1, tab2 = st.tabs(["Player Distribution by Country", "Average Rating by Position"])

with tab1:
    st.markdown("### Player Distribution by Country")
    
    selected_countries = st.multiselect(
        label="Select Countries", 
        options=player_count['Country'].tolist(), 
        default=['Egypt']
    )

    if selected_countries:
        filtered_data = player_count[player_count['Country'].isin(selected_countries)]
    else:
        filtered_data = player_count

    fig = px.choropleth(filtered_data, 
                        locations='Country', 
                        locationmode='country names', 
                        color='Player_Count',
                        hover_name='Country',
                        color_continuous_scale='blugrn',
                        title=f'FIFA Players Distribution {", ".join(selected_countries) if selected_countries else ""}')
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        margin={"r":0, "t":50, "l":0, "b":0},
        coloraxis_colorbar=dict(
            title="Player Count",
            tickvals=[filtered_data['Player_Count'].min(), filtered_data['Player_Count'].max()],
            ticks="outside"
        ),
        title_x=0.5,
        title_font=dict(size=20)
    )

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Average Overall Rating by Position")
    
    selected_positions = st.multiselect(
        label="Select Positions", 
        options=positions.tolist(), 
        default=positions.tolist()
    )

    filtered_position_data = average_rating_by_position[average_rating_by_position['Position'].isin(selected_positions)]
    fig2 = px.bar(filtered_position_data, 
                  x='Position', 
                  y='Overall', 
                  title='Average Overall Rating by Position',
                  labels={'Overall': 'Average Overall Rating', 'Position': 'Player Position'},
                  color='Overall',  
                  color_continuous_scale='blugrn',

                  text='Overall')

    fig2.update_layout(
        title_x=0.5,
        margin={"r":0, "t":50, "l":0, "b":0}
    )

    st.plotly_chart(fig2, use_container_width=True)
