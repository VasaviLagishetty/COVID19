#COVID19 DashBoard

#importing libraries
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests
from datetime import datetime

#Building Raw Dataframe

raw= requests.get("https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/Coronavirus_2019_nCoV_Cases/FeatureServer/1/query?where=1%3D1&outFields=*&outSR=4326&f=json")
raw_json = raw.json()
df = pd.DataFrame(raw_json["features"])

#Building Dataframe with use of raw Dataframe, all columns are mentioned

data_list = df["attributes"].tolist()
data = pd.DataFrame(data_list)
data = data.set_index("OBJECTID")
data = data.reset_index(drop = True)

#checking the NaN rows of Last_Update column
bool_series = pd.isnull(data['Last_Update']) 

#revoming rows of NaN Last_Updated Column
data = data[data['Last_Update'].notna()]
data["Province_State"].fillna(value="", inplace=True)

#Converting Last_Update Column to datetime type
data = data[data['Last_Update'].notna()]
data["Province_State"].fillna(value="", inplace=True)

#complete dataframe is build
print(data)

#Aggregating Values based on country region
df_total = data.groupby('Country_Region',as_index=False).agg({'Confirmed' : 'sum','Recovered' : 'sum','Deaths' : 'sum'}) 

#Total Confirmed, Recovered and Death Cases
total_confirmed = data['Confirmed'].sum()
total_recovered = data['Recovered'].sum()
total_deaths = data['Deaths'].sum()
print("Total confirmed cases till",data['Last_Update'][0],"are",total_confirmed)
print("Total recovered cases till",data['Last_Update'][0],"are",total_recovered)
print("Total death cases till",data['Last_Update'][0],"are",total_deaths)

#top10 countries of Confirmed, Death and Recovered Cases
df_top10 = df_total.nlargest(10, "Confirmed")
top10_countries_1 = df_top10["Country_Region"].tolist()
top10_confirmed = df_top10["Confirmed"].tolist()

df_top10 = df_total.nlargest(10, "Recovered")
top10_countries_2 = df_top10["Country_Region"].tolist()
top10_recovered = df_top10["Recovered"].tolist()

df_top10 = df_total.nlargest(10, "Deaths")
top10_countries_3 = df_top10["Country_Region"].tolist()
top10_deaths = df_top10["Deaths"].tolist()

#defining Subplot
fig = make_subplots(
    rows = 4, cols = 6,
    specs=[
            [{"type": "scattergeo", "rowspan": 4, "colspan": 3}, None, None, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"} ],
            [    None, None, None,               {"type": "bar", "colspan":3}, None, None],
            [    None, None, None,              {"type": "bar", "colspan":3}, None, None],
            [    None, None, None,               {"type": "bar", "colspan":3}, None, None],
          ]
)

#Hover Message
message = data["Country_Region"] + " " + data["Province_State"] + "<br>"
message += "Confirmed: " + data["Confirmed"].astype(str) + "<br>"
message += "Deaths: " + data["Deaths"].astype(str) + "<br>"
message += "Recovered: " + data["Recovered"].astype(str) + "<br>"
message += "Last updated: " + data["Last_Update"].astype(str)
data["text"] = message

#Scattergeo Graph
fig.add_trace(
    go.Scattergeo(
        locationmode = "country names",
        lon = data["Long_"],
        lat = data["Lat"],
        hovertext = data["text"],
        showlegend=False,
        marker = dict(
            size = 5,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = True,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(50, 50, 50)'
            ),
            cmin = 0,
            color = data['Confirmed'],
            cmax = data['Confirmed'].max(),
            colorbar_title="Confirmed Cases<br>Latest Update",  
            colorbar_x = -0.05
        )

    ),    
    row=1, col=1
)

fig.update_geos(
    projection_type="natural earth",
    landcolor="grey",
    oceancolor="LightBlue",
    showocean=True,
    lakecolor="LightBlue"
)

#Indicator Graphs
# Confirmed Cases
fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_confirmed,
        title="Confirmed Cases",
    ),
    row=1, col=4
)

# Recovered Cases
fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_recovered,
        title="Recovered Cases",
    ),
    row=1, col=5
)

# Death Cases
fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_deaths,
        title="Deaths Cases",
    ),
    row=1, col=6
)

#Bar Graphs
# Confirmed Cases
fig.add_trace(
    go.Bar(
        x=top10_countries_1,
        y=top10_confirmed, 
        name= "Confirmed Cases",
        marker=dict(color="Yellow"), 
        showlegend=True,
    ),
    row=2, col=4
)

# Recovered Cases
fig.add_trace(
    go.Bar(
        x=top10_countries_2,
        y=top10_recovered, 
        name= "Recovered Cases",
        marker=dict(color="Green"), 
        showlegend=True),
    row=3, col=4
)

# Death Cases
fig.add_trace(
    go.Bar(
        x=top10_countries_3,
        y=top10_deaths, 
        name= "Deaths Cases",
        marker=dict(color="crimson"), 
        showlegend=True),
    row=4, col=4
)

#Subplot Layout
fig.update_layout(
    template="plotly_dark",
    title = "Global COVID-19 Cases (Last Updated: " + str(data["Last_Update"][0]) + ")",
    showlegend=True,
    legend_orientation="h",
    legend=dict(x=0.65, y = -0.1),
    font=dict(family='Candara', size=12, color='#FFFFFF')
)

# Saving to a HTML file
fig.write_html('COVID19.html', auto_open=True)
