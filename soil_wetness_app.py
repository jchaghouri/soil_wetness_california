#Import Python Libraries
import pandas as pd
import folium 
import geopandas as gpd
from folium.features import GeoJsonPopup, GeoJsonTooltip
import streamlit as st
from streamlit_folium import folium_static
import sqlite3
import time
import matplotlib.pyplot as plt
import statsmodels
import branca
 

#lines 17-32 are connecting to the SQL data base and extracting data    

conn = sqlite3.connect('soil_database') #Connect to SQL database
c = conn.cursor()
#This query is selecting all of the columns from the soil wetness table from the database and putting them into a data frame

c.execute('''  
select *
from counties c
inner join soil_wetness s on c.countyfp = s.CountyFP
''')


wetness = pd.DataFrame(c.fetchall(),columns=['county_fips_id','Name','YEAR','January','February', 'March', 'April','May','June','July','August','September','October','November','December','Annual Average','CountyFP'])

finaldf = wetness


#lines 35-110 prepare and clean the data for time series analysis

wetness['YEAR'] = wetness['YEAR'].astype('str')


wetness['Month'] = '1'
wetness['Day'] = '1'
wetness['Date'] = pd.to_datetime(wetness[['YEAR','Month','Day']], format = '%Y-%m')
Jandf = wetness[["January",'Date','Name']]
Jandf = Jandf.rename(columns={'January':'Value'})

wetness['Month'] = '2'
wetness['Day'] = '1'
wetness['Date'] = pd.to_datetime(wetness[['YEAR','Month','Day']], format = '%Y-%m')
Febdf = wetness[["February",'Date','Name']]
Febdf = Febdf.rename(columns={'February':'Value'})

wetness['Month'] = '3'
wetness['Day'] = '1'
wetness['Date'] = pd.to_datetime(wetness[['YEAR','Month','Day']], format = '%Y-%m')
Mardf = wetness[["March",'Date','Name']]
Mardf = Mardf.rename(columns={'March':'Value'})

wetness['Month'] = '4'
wetness['Day'] = '1'
wetness['Date'] = pd.to_datetime(wetness[['YEAR','Month','Day']], format = '%Y-%m')
Aprdf = wetness[["April",'Date','Name']]
Aprdf = Aprdf.rename(columns={'April':'Value'})

wetness['Month'] = '5'
wetness['Day'] = '1'
wetness['Date'] = pd.to_datetime(wetness[['YEAR','Month','Day']], format = '%Y-%m')
Maydf = wetness[["May",'Date','Name']]
Maydf = Maydf.rename(columns={'May':'Value'})

wetness['Month'] = '6'
wetness['Day'] = '1'
wetness['Date'] = pd.to_datetime(wetness[['YEAR','Month','Day']], format = '%Y-%m')
Jundf = wetness[["June",'Date','Name']]
Jundf = Jundf.rename(columns={'June':'Value'})

wetness['Month'] = '7'
wetness['Day'] = '1'
wetness['Date'] = pd.to_datetime(wetness[['YEAR','Month','Day']], format = '%Y-%m')
Juldf = wetness[["July",'Date','Name']]
Juldf = Juldf.rename(columns={'July':'Value'})

wetness['Month'] = '8'
wetness['Day'] = '1'
wetness['Date'] = pd.to_datetime(wetness[['YEAR','Month','Day']], format = '%Y-%m')
Augdf = wetness[["August",'Date','Name']]
Augdf = Augdf.rename(columns={'August':'Value'})

wetness['Month'] = '9'
wetness['Day'] = '1'
wetness['Date'] = pd.to_datetime(wetness[['YEAR','Month','Day']], format = '%Y-%m')
Sepdf = wetness[["September",'Date','Name']]
Sepdf = Sepdf.rename(columns={'September':'Value'})

wetness['Month'] = '10'
wetness['Day'] = '1'
wetness['Date'] = pd.to_datetime(wetness[['YEAR','Month', 'Day']],format = '%Y-%m')
Octdf = wetness[["October",'Date','Name']]
Octdf = Octdf.rename(columns={'October':'Value'})

wetness['Month'] = '11'
wetness['Day'] = '1'
wetness['Date'] = pd.to_datetime(wetness[['YEAR','Month','Day']], format = '%Y-%m')
Novdf = wetness[["November",'Date','Name']]
Novdf = Novdf.rename(columns={'November':'Value'})

wetness['Month'] = '12'
wetness['Day'] = '1'
wetness['Date'] = pd.to_datetime(wetness[['YEAR','Month','Day']], format = '%Y-%m')
Decdf = wetness[["December",'Date','Name']]
Decdf = Decdf.rename(columns={'December':'Value'})

timesdf = pd.concat([Jandf,Febdf,Mardf,Aprdf,Maydf,Jundf,Juldf,Augdf,Sepdf,Octdf,Novdf,Decdf])

wetness['Year'] = pd.DatetimeIndex(wetness['Date']).year


#lines 35-51 create the header and sidebar for the streamlit app
st.header("Surface Soil Wetness in California by County")
with st.sidebar:
    
    st.markdown("**GitHub**")
    st.write('Check out the code at our Github page [here](https://github.com/jchaghouri/soil_wetness_california)')
    
    st.markdown("**Data:**")
    
    st.write("***Surface Soil Wetness***")
    st.write("The data we collected for analysis was the Monthy & Annual Surface Soil Wetness from the NASA POWER data set. The soil wetness value represents the percent of soil moisture. A value of 0 indicates a completey water-free soil and a value of 1 indicated a completely saturated soil; where surface is the layer from the surface 0cm to 5cm below grade.")
    
    st.write("***Time Data***")
    st.write("The data we collected is from 2011 to 2021. This is in monthly values as well as annual values that represent the average soil wetness percent between all of the months in that year.")
             
    st.write("***Location Data***")
    st.write("Data was collected for every county in California using the POWER Data Access Viewer")
                
    st.markdown("**References**")
    st.write("The data was obtained from the National Aeronautics and Space Administration (NASA) Langley Research Center (LaRC) Prediction of Worldwide Energy Resource (POWER) Project funded through the NASA Earth Science/Applied Science Program.")
    st.write("The data was obtained from the POWER Project's Monthly and Annually 2.3.12 version on 2022/09/20.")
   
    
#lines 54-56 combine the county, soilwetness, and geodata into one merged data frame, that includes all wetness values, all geometry data, and all county names with ID numbers

geodata = gpd.read_file('county_ca.geojson')
combineddf = geodata.merge(finaldf,left_on ='NAME', right_on = 'Name', how ='outer')

#This line creates two tabs in the streamlit app to split our analysis between map and time series 
tab1, tab2 = st.tabs(["Map Visualization", "Time Series Analysis"])

#lines 
with tab1:
    #lines 64-66 creates a select box for the user to choose a year and month for the map visualization 
    time = st.slider('Choose a year:', 2011,2021,2011)
    st.write('The year is ', time)
   # time = str(time)
    month = st.select_slider('Choose a month or the annual average:', options= ['Annual Average','January','February', 'March', 'April','May','June','July','August','September','October','November','December'])
    #this if statement creates a plot on the map is the user chooses to see the annual average soil wetness rather than monthly values
    if (month == 'Annual Average'):
        df =combineddf[['county_fips_id', 'Name','Year','Annual Average','geometry' ]]
       
        df = df[df['Year']==time]
        st.write('You chose Annual Average')
        
        st.write('Hover your cursor over the county you want to see the Surface Soil Wetness value for.')
        
        st.write('The data you chose to view is the Annual Average Surface Soil Wetness for', time)

        #lines 80-81 set the map starting location and creates the tiles
        m = folium.Map(location=[37, -120], zoom_start=5.5,tiles=None)
        folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m)
       




        #Plot Choropleth map using folium
        choropleth1 = folium.Choropleth(
            geo_data='county_ca.geojson',     #This is the geojson file for the counties in California 
            name='Choropleth Map of Central Valley Soil Wetness',
            data=df,                                  #This is the dataframe we created in the data preparation step
            columns=['county_fips_id', month],                #'county_fips_id' and 'month' are the two columns in the dataframe that we use to grab the data for each county and plot it in the choropleth map
            key_on='feature.properties.COUNTYFP',     #This is the key in the geojson file that we use to grab the geometries for each county in order to add the geographical boundary layers to the map
            fill_color = 'YlGn',
            nan_fill_color="grey",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Surface Soil Wetness',
            highlight=True,
            line_color='black').geojson.add_to(m)
        geojson1 = folium.features.GeoJson(
                       data=df,
                       name='Surface Soil Wetness Values',
                       smooth_factor=2,
                       style_function=lambda x: {'color':'black','fillColor':'green','weight':0.5},
                       tooltip=folium.features.GeoJsonTooltip(
                           fields=['Name',
                                   'Annual Average',
                                   'Year'],
                           aliases=["Name:",
                                    'Annual Average:',
                                    'Year:'], 
                           localize=False,
                           sticky=False,
                           labels=True,
                           style="""
                               background-color: #F0EFEF;
                               border: 2px solid black;
                               border-radius: 3px;
                               box-shadow: 3px;
                           """,
                           max_width=800,),
                            highlight_function=lambda x: {'weight':3,'fillColor':'blue'},
                           ).add_to(m) 
        colormap = branca.colormap.linear.YlGn_09.scale(0, 1)
        colormap = colormap.to_step(index=[0., .1,.2,.3,.4,.5,.6, 0.7 ,0.8 ,0.9 ,1.])
        colormap.caption = 'Surface Soil Wetness'
        colormap.add_to(m)

        folium_static(m)


    #this else statement creates a plot on the map if the user chooses to see the values of a specific month
    else:
        
        
        df = combineddf[['COUNTYFP','Year','January','February', 'March', 'April','May','June','July','August','September','October','November','December','Name','geometry']]
        df =df[df['Year']==time]
        df =df.loc[:,('COUNTYFP','Year',month,"Name",'geometry')]

        st.write('You chose', month)
        
        st.write('Hover your cursor over the county you want to see the Surface Soil Wetness value for.')
        
        
        st.write('The data you chose to view is the Surface Soil Wetness for ', month, time)





        #Initiate a folium map
        m = folium.Map(location=[37, -120], zoom_start=5.5,tiles=None)
        folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m)
     




        #Plot Choropleth map using folium
        choropleth1 = folium.Choropleth(
            geo_data='county_ca.geojson',     #This is the geojson file for the counties in California
            name='Choropleth Map of Central Valley Soil Wetness',
            data=df,                                  #This is the dataframe we created in the data preparation step
            columns=['COUNTYFP', month],                #'COUNTYFP' and 'month' are the two columns in the dataframe that we use to grab the data for each county and plot it in the choropleth map
            key_on='feature.properties.COUNTYFP',             #This is the key in the geojson file that we use to grab the geometries for each county in order to add the geographical boundary layers to the map
            fill_color = 'YlGn',
            nan_fill_color="grey",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Surface Soil Wetness',
            highlight=True,
            line_color='black').geojson.add_to(m)
        geojson1 = folium.features.GeoJson(
                       data=df,
                       name='Soil Wetness Values',
                       smooth_factor=2,
                       style_function=lambda x: {'color':'black','fillColor':'green','weight':0.5},
                       tooltip=folium.features.GeoJsonTooltip(
                           fields=['Name',
                                   month,
                                   'Year'],
                           aliases=["Name:",
                                    'Soil Wetness Value:',
                                    'Year:'], 
                           localize=True,
                           sticky=False,
                           labels=True,
                           style="""
                               background-color: #F0EFEF;
                               border: 2px solid black;
                               border-radius: 3px;
                               box-shadow: 3px;
                           """,
                           max_width=800,),
                            highlight_function=lambda x: {'weight':3,'fillColor':'blue'},
                           ).add_to(m) 
        colormap = branca.colormap.linear.YlGn_09.scale(0, 1)
        colormap = colormap.to_step(index=[0., .1,.2,.3,.4,.5,.6, 0.7 ,0.8 ,0.9 ,1.])
        colormap.caption = 'Surface Soil Wetness'
        colormap.add_to(m)
        
        folium_static(m)

#everything below is for tab 2: time series analysis
with tab2:
    #lines 208-212 describe all the parts of the times series analysis using sesonal decompose 
    st.write("Displayed below is four different plots,Observed, Trend, Seasonal, and Residual. This time series analysis was done using ***seasonal_decompose*** in the *StatModel* package in Python. The model used for these plots is multiplicative.")
    st.write("***Observed***: This plot displays the Surface Soil Wetness for your chosen county with years on the x-axis and wetness value on the y-axis.")
    st.write("***Trend***: Shows a pattern in data that shows the movement of a series to relatively higher or lower values over a long period of time. In other words, a trend is observed when there is an increasing or decreasing slope in the time series. This is the integral of the ***Observed*** plot, so this shows the yearly wetness and whether it is going down or up from the previous year.")
    st.write("***Seasonal***: This is the pattern of our data, in this case the seasonality plot for each county looks like a sine wave. This is because the rain season happens every November-February so the seasonal pattern is sinusoidal.")
    st.write("***Residual***: The residual is what is left. There are patterns that do not fit in the trend and they are put here in the remainder.")
    #creates a selection box for the user to select a county
    countyname =  st.selectbox('Choose a county:', ('Alameda',
     'Alpine',
     'Humboldt',
     'Lake',
     'Los Angeles',
     'Nevada',
     'San Mateo',
     'Santa Clara',
     'Yuba',
     'Mendocino',
     'Mono',
     'Riverside',
     'San Benito',
     'San Luis Obispo',
     'Santa Barbara',
     'Sutter',
     'Tulare',
     'Butte',
     'Solano',
     'Calaveras',
     'Colusa',
     'Monterey',
     'Stanislaus',
     'San Bernardino',
     'Del Norte',
     'Plumas',
     'Shasta',
     'Siskiyou',
     'Marin',
     'San Joaquin',
     'Contra Costa',
     'Glenn',
     'Imperial',
     'Placer',
     'Kings',
     'Lassen',
     'Tuolumne',
     'San Francisco',
     'Fresno',
     'Modoc',
     'Santa Cruz',
     'Tehama',
     'Ventura',
     'San Diego',
     'Kern',
     'El Dorado',
     'Sierra',
     'Orange',
     'Yolo',
     'Trinity',
     'Madera',
     'Inyo',
     'Amador',
     'Sacramento',
     'Napa',
     'Sonoma',
     'Mariposa',
     'Merced'))
    
    
    #lines 351-361 create a time series analysis using sesonal decompose and a multiplicative model
    from statsmodels.tsa.seasonal import seasonal_decompose

    tsdf = timesdf.loc[timesdf['Name']== countyname]
    tsdf = tsdf.sort_values(by=['Date'])

    tsdf.set_index('Date', inplace=True)

    analysis = tsdf[['Value']].copy()


    decompose_result_mult = seasonal_decompose(analysis, model="multiplicative")

    observed = decompose_result_mult.observed
    trend = decompose_result_mult.trend
    seasonal = decompose_result_mult.seasonal
    residual = decompose_result_mult.resid
    #plot the four outputs of the sesonal decompose analysis
    fig,ax = plt.subplots(4)
    fig.suptitle('Seasonal Decomposed Time Series Analysis')
    ax[0].plot(observed)
    ax[0].set_title('Observed')

    ax[1].plot(trend)
    ax[1].set_title("Trend")

    ax[2].plot(seasonal)
    ax[2].set_title("Seasonal")

    ax[3].plot(residual)
    ax[3].set_title("Residual")
    fig.set_size_inches((10,10))
    fig.tight_layout()
    st.pyplot(fig)
    
    
    
    
    

