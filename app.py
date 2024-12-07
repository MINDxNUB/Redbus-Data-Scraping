import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import pymysql
from datetime import time



# Load the routes data for different states from CSV files
def load_routes(filename):
    df = pd.read_csv(filename)
    return df["Route"].tolist()

lists_ker = load_routes("D:/CSV files redbus/kerala.csv")
lists_westb = load_routes("D:/CSV files redbus/westbengal.csv")
lists_tel = load_routes("D:/CSV files redbus/telengana.csv")
lists_goa = load_routes("D:/CSV files redbus/goa.csv")
lists_raj = load_routes("D:/CSV files redbus/rajasthan.csv")
lists_southb = load_routes("D:/CSV files redbus/southbengal.csv")
lists_hima = load_routes("D:/CSV files redbus/himachal.csv")
lists_ass = load_routes("D:/CSV files redbus/assam.csv")
lists_punj = load_routes("D:/CSV files redbus/punjab.csv")
lists_biha = load_routes("D:/CSV files redbus/bihar.csv")

# Display available routes for selected state
state_route_map = {
    "Kerala": lists_ker,
    "West Bengal": lists_westb,
    "Telangana": lists_tel,
    "Goa": lists_goa,
    "Rajasthan": lists_raj,
    "South Bengal": lists_southb,
    "Himachal Pradesh": lists_hima,
    "Assam": lists_ass,
    "Punjab": lists_punj,
    "Bihar": lists_biha,
}


#streamlit page config
st.set_page_config(layout="wide")


# Sidebar navigation menu
web = option_menu(menu_title="🚌 Redbus Filtering App",
                 options=["Home", "Find Routes"],
                 icons=["house", "map"],
                 orientation="horizontal",
                 styles={"container": {"width": "100%"},
                         "icon": {"font-size": "20px", "color": "#000"}})

# Home page content
if web == "Home":
    st.image("t1.jpg", width=200)
    st.title("Redbus Data Scraping and Filtering Application")
    st.subheader("Overview")
    st.markdown("This web app allows users to dynamically filter bus routes, prices, and timings using Redbus data scraped through Selenium. "
                "Users can filter routes based on their preferred state, bus type, fare range, and start time, providing a user-friendly experience "
                "for planning bus journeys with ease.")
# States and Routes page content
if web == "Find Routes":
    # Create a two-column layout for state selection and bus options
    col1, col2 = st.columns(2)
    
    with col1:
        state = st.selectbox("Select a State", 
                             ["Kerala", "West Bengal", "Telangana", "Goa", "Rajasthan", 
                              "South Bengal", "Himachal", "Assam", "Punjab", "Bihar"])

    with col2:
        bus_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
        fare_range = st.radio("Select Fare Range", ("50-999", "1000-1999", "2000 and above"))
    
    #getting list of routes to select based on the state
    routes = state_route_map.get(state, [])
    selected_route = st.selectbox(f"Select a Route in {state}", routes)

     # Function to fetch filtered bus data from the MySQL database
    def fetch_data(route, bus_type, fare_range):
        connection = pymysql.connect(host="localhost", user="root", password="5678", database="redbus", autocommit=True)
        cursor = connection.cursor()
        #cursor.execute("USE REDBUS")

        # Determine fare range
        if fare_range == "50-999":
            fare_min, fare_max = 50, 999
        elif fare_range == "1001-1999":
            fare_min, fare_max = 1000, 1999
        else:
            fare_min, fare_max = 2000, 10000  # for "2000 and above"

        # Set bus type condition
        if bus_type == "Sleeper":
            bus_type_condition = "Bustype LIKE '%Sleeper%'"
        elif bus_type == "Semi-Sleeper":
            bus_type_condition = "Bustype LIKE '%Semi-Sleeper%'"
        else:
            bus_type_condition = "Bustype NOT LIKE '%Sleeper%' AND Bustype NOT LIKE '%Semi-Sleeper%'"

        # Construct SQL query
        query = f'''
        SELECT 
            id, Route_name, Route_link, Busname, Bustype, 
            DATE_FORMAT(Start_time, '%H:%i:%s') AS Start_time, 
            Total_duration, 
            DATE_FORMAT(End_time, '%H:%i:%s') AS End_time, 
            Ratings, Price, Seats_Available
        FROM bus_routes 
        WHERE Price BETWEEN {fare_min} AND {fare_max}
        AND Route_name = "{route}"
        AND {bus_type_condition}
        ORDER BY Price DESC, Start_time ASC
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        #connection.close()
        # Convert results into a DataFrame
        df = pd.DataFrame(result, columns=[
            "id", "Route_name", "Route_link", "Busname", "Bustype", "Start_time", "Total_duration", "End_time", 
             "Ratings", "Price", "Seats_Available" 
        ])
        df['Start_time'] = pd.to_datetime(df['Start_time'], format='%H:%M:%S').dt.strftime('%H:%M:%S')
        df['End_time'] = pd.to_datetime(df['End_time'], format='%H:%M:%S').dt.strftime('%H:%M:%S')
        return df


    # If a route is selected, fetch and display filtered data
    if selected_route:
        st.subheader(f"Filtered Bus Data for {selected_route}")
        filtered_data = fetch_data(selected_route, bus_type, fare_range)
        
        # Show filtered data in a table
        if filtered_data.empty:
            st.write("No buses found for the selected criteria.")
        else:
            st.dataframe(filtered_data)