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
