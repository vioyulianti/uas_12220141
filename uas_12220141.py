# NAMA  : VIO YULIANTI
# NIM   : 12220141
# UAS PEMOGRAMAN KOMPUTASI

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import string as str
import streamlit as st
from bokeh.plotting import figure
from bokeh.core.property.dataspec import value

# Title
st.set_page_config(layout = "wide")
st.title("World Crude Oil Production 1971 - 2015")

# Opening JSON and CSV File
## JSON File
fhand1 = open("kode_negara_lengkap.json")
file_json = json.load(fhand1)
file_json = pd.DataFrame.from_dict(file_json, orient = "columns")
## CSV File
fhand2 = open("produksi_minyak_mentah.csv")
file_csv = pd.read_csv(fhand2)

# Removing Data
list_remove_data = []
list_country_codes = []
country_codes = list(file_csv["kode_negara"])
alpha_3 = list(file_json["alpha-3"])

for i in country_codes :
    if i not in list_country_codes :
        list_country_codes.append(i)
for i in list_country_codes:
    if i not in alpha_3 :
        list_remove_data.append(i)
for i in list_remove_data :
    file_csv = file_csv[file_csv.kode_negara != i]
    if i in list_country_codes :
        list_country_codes.remove(i)

# Data
list_countries = []
for i in range(len(list_country_codes)) :
    for j in range(len(alpha_3)) :
        if list_country_codes[i] == alpha_3[j] :
            list_countries.append(list(file_json["name"])[j])

# Chart 1 -> Total Production
st.subheader("Total Crude Oil Production")
country = st.selectbox("List of Countries", list_countries)

x_axis = []
y_axis = []

code = file_json[file_json["name"] == country]["alpha-3"].tolist()[0]

for i in range(len(list_countries)) :
    if country == list_countries[i] :
        country_codes = list_country_codes[i]

x_axis = file_csv[file_csv["kode_negara"] == country_codes]["tahun"].tolist()
y_axis = file_csv[file_csv["kode_negara"] == country_codes]["produksi"].tolist()

graph1 = figure(title = 'Crude Oil Production Data of {}'.format(country), x_axis_label = "Years", 
                y_axis_label = "Oil Production")
graph1.width = 900
graph1.height = 600
graph1.line(x_axis, y_axis, legend_label = 'Oil Production of {}'.format(country), 
            line_width = 3, line_color = "#092B6B")

st.bokeh_chart(graph1, use_container_width = True)

# Chart 2 -> Top Countries by Production in T Year
st.subheader ("Countries with The Largest Number of Production in The Selected Year")

input1, input2 = st.columns(2)
input3, input4 = st.columns(2)
chart3, chart4= st.columns(2)

info = input1.info("The Graph Below Presents The Total Amount of Crude Oil Production")
year = input2.slider("Select Year", min_value = 1971, max_value = 2015, step = 1)
num = input3.number_input("Number of Countries", min_value = 1, max_value = None)
numbers = input4.number_input("Write The Number of Countries", min_value = 1, max_value = None)

# Data
list_countries_code = []
list_region = []
list_subregion = []

for i in range(len(list_country_codes)) :
    for j in range(len(alpha_3)) :
        if list_country_codes[i] == alpha_3[j] :
            list_countries_code.append(list(file_json["country-code"])[j])
            list_region.append(list(file_json["region"])[j])
            list_subregion.append(list(file_json["sub-region"])[j])

df = pd.DataFrame(list(zip(list_countries, list_country_codes, list_countries_code, list_region, list_subregion)), 
                            columns=['Country', 'alpha-3', 'Country Code', 'Region', 'Sub-Region'])

df1 = file_csv.loc[file_csv["tahun"] == year]
df1 = df1.sort_values(by = ["produksi"], ascending = False)

countries_inyear = []

for i in range(len(list(df1["kode_negara"]))) :
    for j in range(len(list(df["alpha-3"]))) :
        if list(df["alpha-3"])[j] == list(df1["kode_negara"])[i] :
            countries_inyear.append(list(df["Country"])[j])
    
df1["Country"] = countries_inyear

plt.title('{B} Countries with The Largest Crude Oil Production in {T}'.format(B = numbers,T = year))
plt.bar(df1['Country'][:numbers], df1['produksi'][:numbers], width = 0.8, bottom = None,
            color = "#092B6B", data = None)
plt.xticks(rotation = 90)
plt.xlabel('Country')
plt.ylabel('Maximum Production')

chart4.pyplot(plt)

# Chart 3 -> Cumulative Oil Production
cumulative = []
country2 = []

for i in list_country_codes :
    sum_production = file_csv.loc[file_csv["kode_negara"] == i, "produksi"].sum()
    cumulative.append(sum_production)

df2 = pd.DataFrame(list(zip(list_countries, list_country_codes, cumulative)), columns = 
                            ["Country", "Country Code", "Cumulative Production"]).sort_values(by = 
                            ["Cumulative Production"], ascending = False)

countries_incumulative = []

for i in range(len(list(df2["Country Code"]))) :
    for j in range(len(list(df["alpha-3"]))) :
        if list(df["alpha-3"])[j] == list(df2["Country Code"])[i] :
            countries_incumulative.append(list(df["Country"])[j])
    
df2["Country"] = countries_incumulative

plt.title('{B} Countries with The Largest Crude Oil Cumulative Production'.format(B = num))
plt.bar(df2['Country'][:num], df2['Cumulative Production'][:num], width = 0.8, bottom = None,
            color = "#092B6B", data = None)
plt.xticks(rotation = 90)
plt.xlabel('Country')
plt.ylabel('Cumulative Production')

chart3.pyplot(plt)

# Information 
##1
st.subheader("Crude Oil Production Data")

left, right = st.columns([2,2])
left1, right1 = st.columns([2,2])
left2, right2 = st.columns(2)
left3, right3 = st.columns(2)

country_code = []
name_country = []
region = []
subregion = []

year_info = left.slider("Choose Year", min_value = 1971, max_value = 2015, step = 1)
caption = right.info("Below is The Overall Crude Oil Production Data")

info = file_csv.loc[file_csv["tahun"] == year_info].drop(["tahun"], axis = 1)
info = info.rename(columns = {'produksi': 'Production in {}'.format(year_info)})

list_country_code = list(info["kode_negara"])
for i in range(len(list_country_code)):
    for j in range(len(df["alpha-3"])) :
        if list(df["alpha-3"])[j] == list_country_code[i] :
            country_code.append(list(df["Country Code"])[j])
            name_country.append(list(df["Country"])[j])
            region.append(list(df["Region"])[j])
            subregion.append(list(df["Sub-Region"])[j])

info["Name"] = name_country
info["Country Code"] = country_code
info["Region"] = region
info["Sub-Region"] = subregion

info = info[["Name", "Country Code", "Region", "Sub-Region", "Production in {}".format(year_info)]].sort_values(by = 
            "Production in {}".format(year_info), ascending = False)

production = info.iloc[0]["Production in {}".format(year_info)]
Name = info.iloc[0]["Name"]
codes = info.iloc[0]["Country Code"]
Region = info.iloc[0]["Region"]
SubRegion = info.iloc[0]["Sub-Region"]

for i in range(len(file_json)) :
    if list(file_json["alpha-3"])[i] == codes :
        Name = list(file_json["name"])[i]
        Region = list(file_json["region"])[i]
        SubRegion = list(file_json["sub-region"])[i]

with left1 :
    st.metric("Largest Amount of Crude Oil Production in {}".format(year_info), production)
    st.caption("Country : {}".format(Name))
    st.caption("Region : {}".format(Region))
    st.caption("Sub Region : {}".format(SubRegion))
    st.caption("Country Code : {}".format(codes))

## 2
info2 = pd.DataFrame(list(zip(list_country_codes, cumulative)), columns = ["Country Code", "Cumulative Production"])

info2["Name"] = df["Country"].tolist()
info2["Country Code"] = df["Country Code"].tolist()
info2["Region"] = df["Region"].tolist()
info2["Sub-Region"] = df["Sub-Region"].tolist()

info2 = info2[["Name", "Country Code", "Region", "Sub-Region", "Cumulative Production"]].sort_values(by = 
            "Cumulative Production", ascending = False)

Production2 = info2.iloc[0]["Cumulative Production"]
Name2 = info2.iloc[0]["Name"]
Codes2 = info2.iloc[0]["Country Code"]
Region2 = info2.iloc[0]["Region"]
SubRegion2 = info2.iloc[0]["Sub-Region"]

with left2 :
    st.metric("Largest Amount of Crude Oil Cumulative Production", Production2)
    st.caption("Country : {}".format(Name2))
    st.caption("Region : {}".format(Region2))
    st.caption("Sub Region : {}".format(SubRegion2))
    st.caption("Country Code : {}".format(Codes2))

## 3
Production4 = "Production in {}".format(year_info)

info3 = info[info[Production4]!= 0].sort_values(by = [Production4], ascending = True)

production3 = info3.iloc[0]["Production in {}".format(year_info)]
Name3 = info3.iloc[0]["Name"]
codes3 = info3.iloc[0]["Country Code"]
Region3 = info3.iloc[0]["Region"]
SubRegion3 = info3.iloc[0]["Sub-Region"]

with right1 :
    st.metric("Smallest Amount of Crude Oil Production in {}".format(year_info), production3)
    st.caption("Country : {}".format(Name3))
    st.caption("Region : {}".format(Region3))
    st.caption("Sub Region : {}".format(SubRegion3))
    st.caption("Country Code : {}".format(codes3))

## 4
Production5 = "Cumulative Production"
info4 = info2[info2[Production5]!= 0].sort_values(by = ["Cumulative Production"], ascending = True)

production4 = info4.iloc[0][Production5]
Name4 = info4.iloc[0]["Name"]
codes4 = info4.iloc[0]["Country Code"]
Region4 = info4.iloc[0]["Region"]
SubRegion4 = info4.iloc[0]["Sub-Region"]

with right2 :
    st.metric("Smallest Amount of Crude Oil Cumulative Production", production4)
    st.caption("Country : {}".format(Name4))
    st.caption("Region : {}".format(Region4))
    st.caption("Sub Region : {}".format(SubRegion4))
    st.caption("Country Code : {}".format(codes4))

## 5
info5 = info[info["Production in {}".format(year_info)] == 0]

production_5 = info5.iloc[0]["Production in {}".format(year_info)]
Name5 = info5.iloc[0]["Name"]
codes5 = info5.iloc[0]["Country Code"]
Region5 = info5.iloc[0]["Region"]
SubRegion5 = info5.iloc[0]["Sub-Region"]