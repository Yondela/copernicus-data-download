#!/usr/bin/env python3

import lxml.etree as ET
import requests
from io import BytesIO
from requests.auth import HTTPBasicAuth

import getpass

API_URL = "https://scihub.copernicus.eu/dhus/"

API_DATA_URL = API_URL + "odata/v1/"
API_SEARCH_URL = API_URL + "search?q="

def main_loop():
    
    # Main command
    command = ""

    # Date
    from_date = ""
    to_date = ""
    
    # Defined area
    area_shape = ""
    area_coordinates = list()

    # User information
    username = ""
    password = ""
    
    # Search
    search_result = ""
    
    while command != "quit":
    
        command = input("Please enter command. Either 'quit', 'area', 'date', or 'search':\n")
    
        if command == "search" and (area_shape == "" or len(area_coordinates)) == 0:
            print("Please specify the area you would like to search your current area value is empty.")
    
        elif command == "search" and (from_date == "" or to_date == ""):
            print("Please specify the date you would like to search your current date value is empty.")

        elif command == "date":
            #from_date, to_date = date()
            #from_date = input("From date(DD/MM/CCYY):\n")
            #to_date = input("To date(DD/MM/CCYY):\n")
            from_date = "2021-09-09"
            to_date = "2021-10-12"

        elif command == "area":
            #area_shape, area_coordinates = area()
            #area_shape = input("Enter the shape of the area. (E.g., point, triangle, or rectangle):\n")
            #area_coordinates = input("Please enter the coordinates. (E.g., Lat,Long):\n")
            area_shape = "point"
            area_coordinates = ["-30.725229, 25.084173"]

        elif command == "user":
            username = input("Enter your user name:\n")
            try:
                password = getpass.getpass()
            except Exception as error:
                print('ERROR', error)

        elif command == "search":

            search_query = '(platformname:Sentinel-1 OR platformname:Sentinel-2)' + ' AND footprint:"Intersects(' + area_coordinates[0] + ')" AND beginposition:[' + from_date + 'T00:00:00.000Z TO ' + to_date + 'T23:59:59:999Z]'

            search_result_response = requests.get(API_SEARCH_URL+search_query,
                                                  auth = HTTPBasicAuth(username, password),
                                                  allow_redirects=True)
            
            print(search_result_response)
            print(search_result_response.content)
            search_result = search_result_response.content
            search_result_root = ET.XML(search_result)
            ET.indent(search_result_root)

            search_title = search_result_root.find("{*}title")
            search_subtitle = search_result_root.find("{*}subtitle")
            search_items_per_page = search_result_root.find("{*}itemsPerPage")
            print(search_title.text)
            print(search_subtitle.text)
            print("Items per page: {}".format(search_items_per_page.text))

            print()

            for entry in search_result_root.iter("{*}entry"):
                entry_id = entry.find("{*}id")
                entry_title = entry.find("{*}title")
                entry_summary = entry.find("{*}summary")
                print("ID: {}".format(entry_id.text))
                print("Title: {}".format(entry_title.text))
                print("Summary: {}".format(entry_summary.text))

                print("----------------------------------")

#def date():
#    from_date_internal = input("From date(DD/MM/CCYY):\n")
#    to_date_internal = input("To date(DD/MM/CCYY):\n")
#
#    from_date_list = from_date_internal.split("/")
#    from_date_day = int(from_date_list[0])
#    from_date_month = int(from_date_list[1])
#    from_date_year = int(from_date_list[2])
#
#    if not (1 <= from_date_day <= 31):
#        raise ValueError("The day value is either less than 1 or more than 31.")
#    if not (1 <= from_date_month <= 12):
#        raise ValueError("The month value is either less than 1 or more than 12.")
#
#    if not (1 <= from_date_year <= 31):
#        raise ValueError("The year value is either less than 1 or more than")
#        
#
#    return from_date_internal, to_date_internal
#
#def area():
#    area_shape = input("Enter the shape of the area. (E.g., point, triangle, or rectangle)")
#    area_coordinates = input("Please enter the coordinates. (E.g., Lat,Long)")
#
#    return area_shape, area_coordinates
#
#def search():
#    pass

if __name__ == "__main__":
    main_loop()
