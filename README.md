# Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit
## Introduction
  This web app allows users to dynamically filter bus routes, prices, and timings using Redbus data scraped through Selenium.
  Users can filter routes based on their preferred state, bus type and fare range, providing a user-friendly experience for planning bus journeys with ease.
## Approach
  ### 1.Route extraction
    Using selenium the bus routes of various state buses(both govt and private) are extracted from the redbus website and 
    coverted into dataframes then stored as a csv file. A minimum of 10 such states' routes have been extracted. 
    The code used for route extraction can be referred from the file **routeextract.ipynb**
