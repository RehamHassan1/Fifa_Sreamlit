import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FIFA Player Distribution Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center;'>FIFA Data Analysis</h1>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("fifa_eda.csv")
df = load_data()
average_rating_by_position = df.groupby('Position')['Overall'].mean().reset_index()
average_rating_by_position = average_rating_by_position.sort_values(by='Overall', ascending=False)
positions = df['Position'].unique()
col1, col2 = st.columns([3,2])
with col1:
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
                  #title='Average Overall Rating by Position',
                  labels={'Overall': 'Average Overall Rating', 'Position': 'Player Position'},
                  color='Overall',  
                  color_continuous_scale='blugrn',
                  text='Overall')
    fig2.update_layout(
        #title_x=0.5,
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    st.plotly_chart(fig2, use_container_width=True)
with col2:
    st.markdown("### Top 10 Nationalities Distribution")
    largest_n = df['Nationality'].value_counts().nlargest(10)
    selected_nationalities = st.multiselect(
        label="Select Nationalities", 
        options=largest_n.index.tolist(), 
        default=largest_n.index.tolist()
    )
    filtered_nationality_data = largest_n[largest_n.index.isin(selected_nationalities)]
    fig_nationality = px.bar(
        filtered_nationality_data, 
        x=filtered_nationality_data.index, 
        y=filtered_nationality_data.values,
        #title='Top 10 Nationalities',
        labels={'y': 'Player Count', 'x': 'Nationality'},
        text=filtered_nationality_data.values,
    )
    fig_nationality.update_traces(marker_color='#5FBB9C') 
    fig_nationality.update_layout(
        #title_x=0.5,
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )
    st.plotly_chart(fig_nationality, use_container_width=True)
st.markdown("### Top 10 Nationalities by Player Count and Their Average Overall Ratings")
nationality_stats = df.groupby('Nationality').agg(
    Player_Count=('ID', 'count'), 
    Average_Overall=('Overall', 'mean')
).reset_index()
top_nationalities = nationality_stats.sort_values(by='Player_Count', ascending=False).head(10)
fig_top_nationalities = px.bar(top_nationalities, 
              x='Nationality', 
              y='Average_Overall', 
              #title='Top 10 Nationalities by Player Count and Their Average Overall Ratings',
              labels={'Average_Overall': 'Average Overall Rating', 'Nationality': 'Nationality'},
              text='Player_Count', 
              color='Average_Overall',  
              color_continuous_scale='blugrn')  
fig_top_nationalities.update_layout(
    #title_x=0.5,
    margin={"r": 0, "t": 50, "l": 0, "b": 0}
)
st.plotly_chart(fig_top_nationalities, use_container_width=True)
st.markdown("### Top 5 Players by Value and Wage")
sorted_players = df.sort_values(by='Wage', ascending=False).head(5)
melted_df = pd.melt(sorted_players, id_vars='Name', value_vars='Wage', var_name='Category', value_name='Amount')
fig_top_players = px.bar(
    melted_df, 
    x='Amount', 
    y='Name', 
    labels={'Amount': 'Wage', 'Name': 'Players'},
    #title='Top 5 Players by Value and Wage'
)
fig_top_players.update_traces(marker_color='#5FBB9C')
fig_top_players.update_layout(
    #title_x=0.5,
    margin={"r": 0, "t": 50, "l": 0, "b": 0}
)
st.plotly_chart(fig_top_players, use_container_width=True)
st.markdown("### Number of FIFA Players by Country")
player_count = df.groupby('Nationality')['Name'].count().reset_index()
player_count.columns = ['Country', 'Player_Count']
fig_choropleth = px.choropleth(player_count, 
                                locations='Country', 
                                locationmode='country names', 
                                color='Player_Count',
                                hover_name='Country',
                                color_continuous_scale='blugrn',
                                #title='Number of FIFA Players by Country'
                                )
fig_choropleth.update_geos(showcoastlines=True, coastlinecolor='Black')
st.plotly_chart(fig_choropleth, use_container_width=True)
