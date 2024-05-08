import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from folium.plugins import MarkerCluster 
from folium.plugins import HeatMap
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
from streamlit_folium import folium_static

col1, col2, col3 = st.columns(3)

df=pd.read_csv("D:/airbnb/airbnbdf.csv")
def get_hostdf():
    hostdata=df[['name', 'description', 'host_id', 'host_name',"accommodates",
             "review_scores",'host_location','host_is_superhost',
              'host_response_rate', 'host_neighbourhood', 'host_response_time',
              'host_listings_count','host_total_listings_count','host_verifications',
              'street', 'market','is_location_exact', 'country',"availability_365"]]
    d=hostdata["host_id"].value_counts().reset_index()
    d.columns=['host_id','host_counts']
    lf=pd.merge(df,d,on='host_id',how='left')
    return lf
def que1():
    lf=get_hostdf()
    l= lf.loc[lf['price'].idxmax()]
    
    name=l["name"]
    price=l["price"]
    host=l["host_name"]
    id=l["host_id"]
    country=l["country"]
    desc=l["description"]
    prop=l["property_type"]
    fac=l["amenities"]
    st.write(f":green[name of the residences:] {name}")      
    st.write(f':green[description of the residence]{desc}')
    st.write(f':green[host details name] {host}')
    st.write(f':green[host id]{id}')
    st.write(f':green[property type of the residence] : {prop}  ')
    st.write(f':green[facilities provided] {fac}')
    st.write(f":green[country name] {country}")
    st.write(f':green[price] {price}')
             

def que2():
    cnt=df["country"].value_counts().reset_index()
    row=cnt.loc[cnt['count'].idxmax()]
    nat=row['country']
    count=row["count"]
    st.write(f'country {nat}  has most residences with a total of {count}')
    
def que3():
    avg=df["price"].mean()
    st.write(f'average price of residences{avg}')

def que4():
    df=get_hostdf()
    row=df.loc[df['host_counts'].idxmax()]
    nam=row['host_name']
    id=row["host_id"]
    count1=row["host_counts"]
    st.write(f'host name : {nam}  host id: {id} number of hostings {count1}' )

def que5():
    fiv=df
    fiv=fiv.loc[fiv["number_of_reviews"].idxmax()]
    name=fiv["name"]
    pty=fiv["property_type"]
    id=fiv["host_id"]
    hnm=fiv["host_name"]
    j=fiv["number_of_reviews"]
    rating=df["review_scores"]
    st.write(f":purple[residence name :] {name}")
    st.write(f":purple[property type :] {pty}")
    st.write(f":purple[host id :] {id}")
    st.write(f":purple[host name :] {hnm}")
    st.write(f":purple[total number of reviews :] {j}")
    st.write(f":purple[rating :] {rating}")
    
    
    
def que6():
    cnt=df
    row=cnt.loc[cnt['price'].idxmin()]
    pr=row["price"]
    nam=row['name']
    pty=row["property_type"]
    hnm=row["host_name"]
    hid=row["host_id"]
    st.write(f':green[name of residence:] {nam}')
    st.write(f':green[host name:] {hnm}')
    st.write(f':green[price of hotel:] {pr}')
    st.write(f':green[host id:] {hid}')
    st.write(f':green[property details:] {pty}')
    
   
def getcountryplot(selcon):
    
    df["latitude"].dropna()
    df["latitude"].dropna()

    df1=df[["_id","name","description",
    "host_id","host_name","host_neighbourhood",
    "street","market",'longitude','country',"property_type",
    'latitude',"price",'availability_30',
    'availability_60', 'availability_90',
    'availability_365', 'amenities',"review_scores",
    "number_of_reviews"]]
    
    if selcon is not None:
        df1=df1[df1["country"]==selcon]
        df1["latitude"]=df1["latitude"].dropna()
        df1["longitude"]=df1["longitude"].dropna()


    # Calculate the mean latitude and longitude for centering the map
    center_lat = df1['latitude'].mean()
    center_lon = df1['longitude'].mean()

    # Create a Folium map centered at the mean coordinates
    my_map = folium.Map(location=[center_lat, center_lon], zoom_start=10)
    marker_cluster = MarkerCluster().add_to(my_map)

        # Add markers for each location
    for _, row in df1.iterrows():
        popup_content = f"{row['name']} - availability in year: {row['availability_365']} property type-{row["property_type"]} {row['review_scores']}"
        folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup_content,
        icon=folium.Icon(icon='cloud')).add_to(marker_cluster)
    st_folium(my_map,height=800, width=1400)
    
def tophotels(selcon):
    df["latitude"].dropna()

    df2=df[["_id","name","description",
    "host_id","host_name","host_neighbourhood",
    "street","market",'longitude','country',"property_type",
    'latitude',"price",'availability_30',
    'availability_60', 'availability_90',
    'availability_365', 'amenities',"review_scores",
    "number_of_reviews"]]
    
    nf=df2[df2["country"]==selcon]
    nf=nf.sort_values(by='review_scores',ascending=False)
    nf1=nf.head(50)
    center_latp = nf1['latitude'].mean()
    center_lonp = nf1['longitude'].mean()
    my_map2 = folium.Map(location=[center_latp, center_lonp], zoom_start=25)
    marker_cluster1 = MarkerCluster().add_to(my_map2)
    for _, row in nf1.iterrows():
            popup_content = f"{row['name']} {row['price']} property type-{row['property_type']} {row['review_scores']}"
            folium.Marker(
                location=[row['latitude'],row['longitude']],
                popup=popup_content,
                icon=folium.Icon(icon='flag')
            ).add_to(marker_cluster1)
    #display streamlit folium
    
    st_folium(my_map2,height=800, width=1400)
            
with st.sidebar:
    
    selected = option_menu("Main Menu", ["Home", "explore areas","analysis",'facts',"learning outcomes"], icons=['house','book', 'pen', 'check mark button', 'school'], menu_icon="cast", default_index=1)
logo_url = "D:/airbnb/airbnblogo.png"
st.image(logo_url, width=170)

if selected=="Home":
        st.title(":rainbow[Welcome to Airbnb booking analysis ]")
        st.write("This is an comprehensive data representation model of airbnb")
        st.write(":orange[In this application you can explore the bookings data conviniently ]")
        st.write(":violet[with the help of dynamic maps ]")
        st.write(":orange[understanding the data can be done easily with statistical representation]")
        st.write(":violet[analysation can be done with charts and graphs ]")
        st.write(":grey[and much more]")
        st.write(":grey[switch to desired tabs now]")
        st.markdown("")
        st.image("D:/airbnb/abnblogo1.jpg",width=480)

if selected=='explore areas':
    countries=df["country"].unique()
    selcon=st.selectbox(" select country",countries)
    getcountryplot(selcon)
    st.write("explore bookings data with interactive maps of the given countries")
    if st.button("explore top 50 rated bookings"):
        map=tophotels(selcon)
        st_folium(map,width=720) 
    
        
    if st.button("explore the densed areas of hotels with heat map"):
        df=df[df["country"]==selcon]

        latp = df['latitude'].mean()
        lonp = df['longitude'].mean()
        hm = folium.Map(location=[latp,lonp], zoom_start=25)
        hmap=df[['latitude','longitude']].values.tolist()
        HeatMap(hmap).add_to(hm)
        folium_static(hm)
        st.write("This is the heatmap of most bookings")
        st.markdown("")
        
        
if selected=='analysis':
    st.subheader(":raibow[Analysis of the Booking data]")
    st.write(":purple[welcome to the page of airbnb booking analysis]")
    st.write("explore the airbnb data charts ")
    st.write("analyse the data in various format given below")
    
    countries=df["country"].unique()
    selcon1=st.selectbox(" select country",countries)
    df=df[df["country"]==selcon1]
    df["property_type"].value_counts()
    value_counts_df = df["property_type"].value_counts().reset_index()
    fig,ax=plt.subplots()
    ax.bar(value_counts_df['property_type'],value_counts_df["count"],color="purple")
    ax.set_xlabel('property_type')
    ax.set_ylabel('count')
    ax.set_title('chart of various property types',color="red")
    ax.tick_params(axis="x",rotation=90)
    st.pyplot(fig)


    prdf=df[df["country"]==selcon1]
    d=prdf["room_type"].value_counts().reset_index()
    if st.button("Check various properties statistics"):
        fig1,ax=plt.subplots(figsize=(9,12))
        ax.pie(d["count"],labels=d["room_type"],shadow=True,autopct='%1.3f%%',startangle=90)
        ax.legend(title="room types",labels=d['room_type'],loc="best")
        
        ax.set_aspect('equal')
        st.pyplot(fig1)
    
    if st.button("average price of property"):
            avdf=df[df["country"]==selcon1]
            result = avdf.groupby('property_type')['price'].mean()
            resultdf= pd.DataFrame(result).reset_index()
            fig3,ax=plt.subplots()
            ax.bar(x=resultdf['property_type'], height=resultdf['price'],color="violet")
            ax.set_xlabel('property_type')
            ax.set_ylabel('count')
            ax.set_title('average price of various property types',color="red")
            ax.tick_params(axis="x",rotation=90)
            st.pyplot(fig3)
        
    
    st.markdown("")

if selected=='facts':
    st.header(":rainbow[explore the facts related the airbnb bookings]")
    st.markdown("")
    st.write("there are multiple facts of host related data of their performance and statistics")
    hdf=get_hostdf()
    opted=st.selectbox("select facts mentioned",("1.residence with highest price",
                       "2.country with most residences",
                       "3.average price of residences",
                       "4.maximum number of  hostings",
                       "5.maximum number of ratings",
                       "6.minimum price of bookings"))
    if opted=="1.residence with highest price":
        que1()
    if opted=="2.country with most residences":
        que2()
    if opted=="3.average price of residences":
        que3()
    if opted=="4.maximum number of  hostings":
        que4()
    if opted=="5.maximum number of ratings":
        que5()
    if opted=="6.minimum price of bookings":
        que6()
    
        
        

    
if selected=='learning outcomes':
        st.subheader(":rainbow[airbnb analysis learning outcomes 🧑‍🎓]")
        st.write("with the help of airbnb capstone i came to learn and uplift some of the vital skills 📚")
        st.write("--powerbi")
        st.write("--python🐍")
        st.write("--EXPLORATORY DATA ANALYSYS🔍")
        st.write("--DATA VISUALISATION WITH THE HELP OF FOLIUM MAPS🗺️")
        st.write("--MONGODB DATA EXTRACTION")
        st.write("--STREAMLIT")
    
