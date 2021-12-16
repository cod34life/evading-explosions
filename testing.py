"""
Name: Xiaofan Gao
CS230: Section 06
Data: volcanoes.csv
URL: Link to your web application online
Description:
This website showcases a variety of information about volcanoes in several visual mediums. They are as follows:
a map displaying every volcano's exact latitude and longitude, a bar chart with the average heights of
some of the most popular volcano types, and two pie charts showing the proportion of volcanoes with each
unique tectonic setting and rock composition. Since most of the volcanoes in the dataset have had eruption
activity, these visuals can help geologists determine the location and profiles of volcanic activity and
predict future eruptions. This site is heavily user-interactive. Examples include navigating to a specific
section, changing the color of the bar chart, and deciding which pie chart(s) to view.
"""

#all imports
import csv
import folium
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


#all global variables
color_selected = "#d07e59"
option = ''

#all functions

#adds space between site elements
def add_space():
    st.markdown('#')

def sidebar_space():
    st.sidebar.markdown('#')

#totals values in a list
def sum_list(l):
    sum = 0
    for i in l:
        sum+=i
    return sum

#allows user to add info
def contribute():
    contribution = st.sidebar.text_input("Tell us what you know about volcanoes, and we'll add it to the site!")
    submit = st.sidebar.button("SUBMIT")



#creates dataframe for volcanoes file --> most important part of project
df_volcanoes = pd.read_csv(r"C:\Users\ga1_xiao\pythonProject2\Final Project\volcanoes.csv", encoding="latin-1")

#starts building site
st.title("Evading Eruptions with Hard Data")
#Streamlit image - https://docs.streamlit.io/library/api-reference/media/st.image
volcano = Image.open(r"C:\Users\ga1_xiao\pythonProject2\Final Project\eruption.jpg")
st.image(volcano)
#sidebar for site settings
st.sidebar.title("Settings")

add_space()

#explains dataframe usage
st.write("By using a compilation of volcano data, we can predict and, thus, avoid future eruptions "
         "by analyzing the location and geographical composition of many volcanoes that have shown evidence "
         "of erupting before. The complete dataset contains over 1000 records on volcanoes. "
         "Feel free to scroll through the sample set for more info.")

#dataframe must be cleaned up before it's displayed
#drops volcano number column (will confuse site visitors, since there's already indexes)
df_display = df_volcanoes.drop(["Volcano Number"], axis=1)
#alphabetized by volcano name
df_display= df_display.sort_values(by=["Volcano Name"], ascending=[True])
#displays however many records user wants (stops at 100 because it's a sample)
#inspiration - https://medium.com/swlh/a-beginners-guide-to-streamlit-5e0a4e711968
num_records = st.sidebar.slider("Records Displayed:",1,100)
st.write(df_display.iloc[1:num_records+1])

add_space()

#asks user what visual they want to see first
visuals = st.sidebar.selectbox("Go to Section", ('Where in the World', 'Heightened Risk', 'Destruction Deconstructed'))
#linking to specific part of page - https://discuss.streamlit.io/t/how-to-navigate-to-a-certain-segment-based-on-user-input/1815/5
#COOL because this functions like one of those actual informational sites (also took me a while to implement correctly)
#map part
if 'Where in the World' in visuals:
    st.sidebar.markdown(f"<a href='#linkto_{1}'>Travel time!</a>", unsafe_allow_html=True)
#bar graph part
if 'Heightened Risk' in visuals:
    st.sidebar.markdown(f"<a href='#linkto_{2}'>Look up!</a>", unsafe_allow_html=True)
    #let user choose bar chart color (default is light brown like the outside of a volcano)
    #Streamlit color picker - https://docs.streamlit.io/library/api-reference/widgets/st.color_picker
    #COOL because I just love it when you can customize things by color
    color_selected = st.sidebar.color_picker('Bar color:', '#d07e59')
#pie charts part
if 'Destruction Deconstructed' in visuals:
    st.sidebar.markdown(f"<a href='#linkto_{3}'>Break off!</a>", unsafe_allow_html=True)
    #asks user which one they'd like to view
    option = st.sidebar.multiselect(
    "Select a volcanic feature",
    ['Plates', 'Rocks'])

    sidebar_space()





#all visuals

#Query 1: 2D map of all volcanoes
#link to this section of page
st.markdown(f"<div id='linkto_{1}'></div>", unsafe_allow_html=True)
#section title
#html header - https://discuss.streamlit.io/t/how-do-i-align-st-title/1668/4'
st.markdown("<h3 style='text-align: center; color: #EE2D29;'>Where in the World</h3>", unsafe_allow_html=True)
#paragraph of info
st.write("Since volcanoes can't move, below is an always up-to-date map displaying each volcano's location"
         "in latitude and longitude. Notice how a portion of volcanoes are in oceans; these are called submarine"
         "volcanoes, and they are merely underwater vents that periodically produce magma. The real threats are "
         "the highly-clustered volcanoes in areas with a high population, like the Ring of Fire around Japan." )

#Folium map tutorial - https://towardsdatascience.com/creating-a-simple-map-with-folium-and-python-4c083abfff94

#dataframe with only the latitude and longitude for volcanoes
df_locations = df_volcanoes[["Latitude", "Longitude", "Volcano Name"]]

#creates Folium map (starting point is Bentley University)
map = folium.Map(location=[42.389, -71.2206], zoom_start=4, control_scale=True)

#iterates through dataframe of coordinates
for i, location in df_locations.iterrows():
    #places custom marker at every group of coordinates
    folium.CircleMarker([location["Latitude"], location["Longitude"]],
                        radius=2,
                        color = 'red',
                        popup = location["Volcano Name"]).add_to(map)
#Streamlit folium - https://discuss.streamlit.io/t/ann-streamlit-folium-a-component-for-rendering-folium-maps/4367
folium_static(map)

add_space()



#Query 2: bar graph showing average height of volcano types
#link to this section of page
st.markdown(f"<div id='linkto_{2}'></div>", unsafe_allow_html=True)
#section title
st.markdown("<h3 style='text-align: center; color: #FA7445;'>Heightened Risk</h3>", unsafe_allow_html=True)
#paragraph of info
st.write("In general, the taller something is, the more of a risk it can be. During earthquakes, "
         "people have to watch out for the collapse of taller buildings and structures. Likewise, "
         "when a tall volcano erupts, pyroclastic tidbits like rocks and volcanic ash will"
         "fly further, and volcanic gases like carbon and sulfur dioxide have a wider spread. "
         "Below is a bar chart with several popular volcano structures and their heights on average.")


#x-axis is volcano types (hardcoded because they're not consecutive rows in dataframe)
x_types = ["Caldera","Lava dome","Pyroclastic cone","Shield","Stratovolcano"]

#y-axis is average height of volcanoes by type
#formula for calculating average elevation for a SPECIFIC group - https://stackoverflow.com/questions/53287976/getting-the-average-value-for-each-group-of-a-pandas-dataframe
avgheights = df_volcanoes.groupby('Primary Volcano Type')['Elevation (m)'].agg(np.mean)
#get average height for each volcano type in the list above
y_heights = []
for i in x_types:
    y_heights.append(avgheights[i])


#builds and formats bar graph
fig,ax = plt.subplots()
fig.set_size_inches(10,7)
#updates color with user selection
ax.bar(x_types,y_heights, color = color_selected)
#chart labels are bold for better visibility
ax.set_title("Average Height of Volcanoes by Type", fontsize = 15, fontweight ="bold")
ax.set_xlabel("Volcano Types",fontweight ="bold")
ax.set_ylabel("Average Height (in meters)", fontweight ='bold')
#plots figure in Streamlit
st.pyplot(fig)

add_space()



#Query 3: 2 pie charts that display on user selection
#link to this section of page
st.markdown(f"<div id='linkto_{3}'></div>", unsafe_allow_html=True)
#section title
st.markdown("<h3 style='text-align: center; color: #FCB930;'>Destruction Deconstructed</h3>", unsafe_allow_html=True)
#paragraph of info
st.write("Like humans, volcanoes have many features. These include the type of tectonic plate they reside on, along"
         " with the kind of rock they're mostly made up of. Which kinds of plates or rocks "
         "cause the most eruptions? If you're wondering, select one or both to see the answer! ")

#easier to clean data (because some column values need to go)
df_volcanoes.columns = [column.replace(' ', '_') for column in df_volcanoes.columns]

#tectonic settings pie chart
#clean up tectonic data
df_tectondata = df_volcanoes[df_volcanoes.Tectonic_Setting!= "Unknown"]

#get number of volcanoes for each tectonic setting
df_tectonum = df_tectondata.groupby("Tectonic_Setting").count()
#store numbers into a list
tectonum_list = df_tectonum.loc[:,"Volcano_Number"].tolist()

#this is equal to 100% of the pie
print(sum_list(tectonum_list))
#get rid of slices smaller than 2%
bottom_3p = 42.21
tectonum_slices = []
for i in tectonum_list:
    if i>bottom_3p:
        tectonum_slices.append(i)


#tectonic pie slice labels (hardcoded because difficult to edit with dataframe properties)
tectonnames = [
'Intraplate/Continental crust(>25)',
'Rift zone/Continental crust (>25)',
'Rift zone/Oceanic crust (<15)',
'Subduction zone/Continental crust (>25)',
'Subduction zone/Crustal thickness unknown',
'Subduction zone/Intermediate crust (15-25)',
'Subduction zone/Oceanic crust (< 15)'
]
tectonnames = list(tectonnames)

#formats and decorates tectonic pie chart
fig2, ax2 = plt.subplots()
fig2.set_size_inches(8, 10)
ax2.pie(tectonum_slices, labels = tectonnames, autopct ='% 1.2f %%',startangle = 180)
ax2.axis('equal')
ax2.set_title('Plate Tectonics (Measurements in Meters)', fontsize=20, fontweight ="bold")



#dominant rock type pie chart
#clean up rock data
df_rockdata = df_volcanoes[df_volcanoes.Dominant_Rock_Type!="No Data (checked)"]

#get number of volcanoes made up of each rock type
df_rocknum = df_rockdata.groupby("Dominant_Rock_Type").count()
#store numbers into list
rocknum_list = df_rocknum.loc[:,"Volcano_Number"].tolist()


#this is equal to 100% of the pie
print(sum_list((rocknum_list)))
#get rid of slices smaller than 3% of pie
bottom_2p = 26.92
rocknum_slices = []
for i in rocknum_list:
    if i>bottom_2p:
        rocknum_slices.append(i)

#rock pie slice labels (hardcoded because difficult to edit with dataframe properties)
rocknames = [
    'Andesite/Basaltic Andesite',
    'Basalt/Picro-Basalt',
    'Dacite',
    'Rhyolite',
    'Trachyandesite/Basaltic Trachyandesite',
    'Trachybasalt/Tephrite Basanite',
    'Trachyte/Trachydacite']
rocknames = list(rocknames)

#formats and decorates rock type pie chart
fig3, ax3 = plt.subplots()
fig3.set_size_inches(6, 7)
ax3.pie(rocknum_slices, labels = rocknames, autopct ='% 1.2f %%',startangle = 180)
ax3.axis('equal')
ax3.set_title('Volcanic Rock', fontsize=15, fontweight ="bold")

if 'Plates' in option:
    #displays tectonic pie chart
    st.pyplot(fig2)
if 'Rocks' in option:
    #displays rock pie chart
     st.pyplot(fig3)

#allows user to add info to site
sidebar_space()
sidebar_space()
sidebar_space()
add_info = st.sidebar.button("Want to add to the site?")
if add_info:
    contribute()

#site theme - https://www.schemecolor.com/volcano-color-palette.php
#COOL - in general, I really liked my incorporation of HTML thanks to Streamlit's markdown feature



