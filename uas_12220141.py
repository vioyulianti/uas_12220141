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
from PIL import Image

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
for i in list(file_csv["kode_negara"]) :
    if i not in list(file_json["alpha-3"]) :
        list_remove_data.append(i)

for i in list_remove_data:
    file_csv = file_csv[file_csv.kode_negara != i]

# Chart -> Total Production
st.subheader("Total Crude Oil Production")

list_countries = []
for i in range(len(file_csv)) :
    for j in range(len(file_json)) :
        if list(file_csv["kode_negara"])[i] == list(file_json["alpha-3"])[j]:
            list_countries.append(list(file_json["name"])[j])

country = st.selectbox("List of Countries", list_countries)



x = file_csv[file_csv["tahun"]]
y = file_csv[file_csv["produksi"]]
graph_1 = file_csv.loc[file_csv["kode_negara"] == list_countries]
graph_1 = figure(title = 'Crude Oil Production Data of', x_axis_label = x, y_axis_label = y)
graph_1.line(x, y, legend_label = 'Trend', line_width = 4)

st.bokeh_chart(graph_1, use_container_width = True)

# Lower Left Columns
t = input()
b = input()

graph_2 = file_csv.loc[file_csv["tahun"] == t]
graph_2 = graph_2.sort_values(by = ["produksi"], ascending = False)
graph_3 = graph_2[:b]

graph_3.plot.bar(x = "negara",  y= "produksi")

# Lower Right Columns
B = input()
list_2 = []
for i in list(file_csv["kode_negara"]) :
    if i not in list_2 :
        list_2.append(i)

jk = []
for i in list_2 :
    a = file_csv.loc[file_csv["kode_negara"] == i, "produksi"].sum()
    jk.append(a)


dfk = pd.DataFrame(list(zip(list_2, jk)), columns = ["kode_negara", "jk"])
dfk = dfk.sort_values(by = ["jk"], ascending = False)

dfk1 = dfk[:B]

#plot

# Upper Left Right
jumlahproduksi = graph_2[:1].iloc[0]["produksi"]
kodenegara = graph_2[:1].iloc[0]["kode_negara"]
nama = ""
region = ""
subregion = ""

for i in range(len(file_json)) :
    if list(file_json["alpha-3"])[i] == kodenegara :
        nama = list(file_json["name"])[i]
        region = list(file_json["region"])[i]
        subregion = list(file_json["sub-region"])[i]

print(jumlahproduksi)
print(kodenegara)
print(nama)
print(region)
print(subregion)

jumlahproduksi = graph_2[:1].iloc[0]["jk"]
kodenegara = graph_2[:1].iloc[0]["kode_negara"]
nama = ""
region = ""
subregion = ""

for i in range(len(file_json)) :
    if list(file_json["alpha-3"])[i] == kodenegara :
        nama = list(file_json["name"])[i]
        region = list(file_json["region"])[i]
        subregion = list(file_json["sub-region"])[i]

print(jumlahproduksi)
print(kodenegara)
print(nama)
print(region)
print(subregion)



dft = graph_2[graph_2.produksi != 0]
dft = dft.sort_values(by = ["produksi"], ascending = True)

jumlahproduksi = dft[:1].iloc[0]["produksi"]
kodenegara = dft[:1].iloc[0]["kode_negara"]
nama = ""
region = ""
subregion = ""

for i in range(len(file_json)) :
    if list(file_json["alpha-3"])[i] == kodenegara :
        nama = list(file_json["name"])[i]
        region = list(file_json["region"])[i]
        subregion = list(file_json["sub-region"])[i]

print(jumlahproduksi)
print(kodenegara)
print(nama)
print(region)
print(subregion)

dfkt = dfk[dfk.jk != 0]
dfkt = dfkt.sort_values(by = ["jk"], ascending = True)

jumlahproduksi = dfkt[:1].iloc[0]["jk"]
kodenegara = dfkt[:1].iloc[0]["kode_negara"]
nama = ""
region = ""
subregion = ""

for i in range(len(file_json)) :
    if list(file_json["alpha-3"])[i] == kodenegara :
        nama = list(file_json["name"])[i]
        region = list(file_json["region"])[i]
        subregion = list(file_json["sub-region"])[i]

print(jumlahproduksi)
print(kodenegara)
print(nama)
print(region)
print(subregion)

dfprodukisnol = graph_2[graph_2.produksi == 0]
listnegaranol = []
listregionnol = []
listsubregionnol = []

for i in range(len(dfprodukisnol)) :
    for j in range (len(file_json)) :
        if list(dfprodukisnol["kode_negara"])[i] == list(file_json["alpha-3"])[j] :
            listnegaranol.append(list(file_json["name"])[j])
            listregionnol.append(list(file_json["region"])[j])
            listsubregionnol.append(list(file_json["sub-region"])[j])

dfprodukisnol["negara"] = listnegaranol
dfprodukisnol["region"] = listregionnol
dfprodukisnol["sub-region"] = listsubregionnol

dfknol = dfk[dfk.produksi == 0]
listnegarakumulatifnol = []
listregionkumulatifnol = []
listsubregionkumulatifnol = []

for i in range(len(dfknol)) :
    for j in range (len(file_json)) :
        if list(dfknol["kode_negara"])[i] == list(file_json["alpha-3"])[j] :
            listnegarakumulatifnol.append(list(file_json["name"])[j])
            listregionkumulatifnol.append(list(file_json["region"])[j])
            listsubregionkumulatifnol.append(list(file_json["sub-region"])[j])

dfknol["negara"] = listnegarakumulatifnol
dfknol["region"] = listregionkumulatifnol
dfknol["sub-region"] = listsubregionkumulatifnol
