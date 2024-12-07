# Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit
## Introduction
  This web app allows users to dynamically filter bus routes, prices, and timings using Redbus data scraped through Selenium.
  Users can filter routes based on their preferred state, bus type and fare range, providing a user-friendly experience for planning bus journeys with ease.
## Approach
  ### 1.Route extraction
    Using selenium the bus routes of various state buses(both govt and private) are extracted from the redbus website and 
    coverted into dataframes then stored as a csv file. A minimum of 10 such states' routes have been extracted. 
    The code used for route extraction can be referred from the file "routeextract.ipynb"
  ### 2.Extraction of Bus details
    Using selenium and the route details extracted previously, the details of buses servicing through the 
    specific routes are extracted. The extracted data includes 
      1.bus name, 
      2.bus type, 
      3.price, 
      4.ratings, 
      5.start time, 
      6.end time,
      7.Total duration etc..
    The extracted detais are converted into dataframes and stored as csv files. The code used for extraction of bus details
    can be referred from the file "bus_extract"
  ### 3.Creating Database
    Before Creating the database all the data from csv files of "extraction of bus details" have been merged together as 
    single data frame for data pre-processing. After cleaning and pre-processing the data frame is converted as csv file.
    Using my sql connector a new database is created and the data from the newly created csv file have been entered into it.
    The code for the process can be referred from the file "database.ipynb"
  ### 4.Creating Web App
    Finally, with the help of streamlit an interactive user-friendly interface that allows user to search the extracted details have been
    created. The app sorts the results based on various states, routes, type of the bus and fare range.
## Results
  **Home page**
  ![Screenshot (17)](https://github.com/user-attachments/assets/d8006adf-bdf9-43d1-9f13-c72057f7b3b3)

  **Search Page**
  
  ![Screenshot (18)](https://github.com/user-attachments/assets/dd0194cb-47b0-4c8e-9159-6abc8cc20e46)

  **Results for bus servicing for selected route**
  
  ![Screenshot (19)](https://github.com/user-attachments/assets/8a0ebd47-f7b9-4a97-bb34-50ac9fc9a894)

  **Filtered result based on bus type**
  
  ![Screenshot (20)](https://github.com/user-attachments/assets/26d5bc90-6f88-47b5-943a-7c0bfc12e1ec)
