#!/usr/bin/env python
import wx
import os
import zlib

import lxml.etree as ET
import requests
from io import BytesIO
from requests.auth import HTTPBasicAuth
from datetime import date

#class DownloadButton(wx.Button):
#
#    def __init__(self, *args, **kw):
#        super(DownloadButton, self).__init__(*args, **kw)
#
#        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
#
#    def OnButtonClicked(self, e):

class MainWindow(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw)

##########################################################################################
# Split window code
        self.main_window = wx.SplitterWindow(parent=self, name="Main Window Splitter")

        self.left_panel = wx.Panel(self.main_window, name="Left Panel")
        #self.right_panel = wx.Panel(self.main_window, name="Right Panel")
        self.right_panel = wx.ScrolledWindow(self.main_window, name="Right Panell")
        #self.right_panel = wx.VScrolledWindow(self.main_window, name="Right Panell")
        #self.right_panel.SetScrollbars(0, 16, 50, style=wx.VSCROLL)
        self.right_panel.SetScrollbars(0, 20, 50, 50)

        self.left_vbox = wx.BoxSizer(wx.VERTICAL)
        self.right_vbox = wx.BoxSizer(wx.VERTICAL)

        self.username_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.username_label = wx.StaticText(self.left_panel, label="Username: ")
        self.username_hbox.Add(self.username_label)
        self.username_input_text = wx.TextCtrl(self.left_panel)
        self.username_hbox.Add(self.username_input_text)

        self.password_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.password_label = wx.StaticText(self.left_panel, label="Password: ")
        self.password_hbox.Add(self.password_label)
        self.password_input_text = wx.TextCtrl(self.left_panel, style=wx.TE_PASSWORD)
        self.password_hbox.Add(self.password_input_text)

        #self.coordinates_shape_hbox = wx.BoxSizer(wx.HORIZONTAL)
        #self.coordinates_shape_label = wx.StaticText(self.left_panel, label="Coordinates shape: ")
        #self.coordinates_shape_hbox.Add(self.coordinates_shape_label)
        #self.coordinates_shape_choice = wx.Choice(
        #        self.left_panel,
        #        choices=["Choose shape",
        #                 "Point",
        #                 "Triangle",
        #                 "Quadrilateral"
        #                 ]
        #        )
        #self.coordinates_shape_hbox.Add(self.coordinates_shape_choice)

        #self.Bind(wx.EVT_CHOICE, self.CoordinateSelection, id=self.coordinates_shape_choice.GetId())

        self.from_date_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.from_date_label = wx.StaticText(self.left_panel, label="From date (YYYY-MM-DD): ")
        self.from_date_hbox.Add(self.from_date_label)
        self.from_date_input_text = wx.TextCtrl(self.left_panel)
        self.from_date_hbox.Add(self.from_date_input_text)

        self.to_date_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.to_date_label = wx.StaticText(self.left_panel, label="To date (YYYY-MM-DD): ")
        self.to_date_hbox.Add(self.to_date_label)
        self.to_date_input_text = wx.TextCtrl(self.left_panel)
        self.to_date_hbox.Add(self.to_date_input_text)

        self.coordinates_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.coordinates_label = wx.StaticText(self.left_panel, label="Coordinate pair(s) (Longitude, Latitude): ")
        self.coordinates_hbox.Add(self.coordinates_label)
        self.coordinates_input_text = wx.TextCtrl(self.left_panel, style=wx.TE_MULTILINE)
        self.coordinates_hbox.Add(self.coordinates_input_text)

        self.search_submit = wx.Button(self.left_panel, label="Search", name="Search Button")

        self.Bind(wx.EVT_BUTTON, self.SearchButtonClick, id=self.search_submit.GetId())

        #self.download_directory_hbox = wx.BoxSizer(wx.HORIZONTAL)
        #self.download_directory_label = wx.StaticText(self.left_panel, label="Download directory: ")
        #self.download_directory_hbox.Add(self.download_directory_label)
        #self.download_directory_input_text = wx.TextCtrl(self.left_panel, value=os.getcwd())
        #self.download_directory_hbox.Add(self.download_directory_input_text)
        
        self.left_vbox.Add(self.username_hbox)
        self.left_vbox.Add(self.password_hbox)
        self.left_vbox.Add(self.from_date_hbox)
        self.left_vbox.Add(self.to_date_hbox)
        self.left_vbox.Add(self.coordinates_hbox)
        self.left_vbox.Add(self.search_submit)
        #self.left_vbox.Add(self.download_directory_hbox)

        #self.right_vbox.Add(wx.StaticText(self.right_panel, label="RIGHT"))

        self.left_panel.SetSizer(self.left_vbox)
        self.right_panel.SetSizer(self.right_vbox)

        self.main_window.SplitVertically(self.left_panel, self.right_panel, sashPosition=300)
##########################################################################################

        ## Setting up the panels
        #main_panel = wx.Panel(self, name="Main Panel")
        #search_parameters_panel = wx.Panel(main_panel, name="Search Parameters Panel")
        #search_results_panel = wx.Panel(main_panel, name="Search Results Panel")

        ## Setting up the BoxSizers
        #main_hbox = wx.BoxSizer(wx.HORIZONTAL)
        #search_parameters_vbox = wx.BoxSizer(wx.VERTICAL)
        #search_results_vbox = wx.BoxSizer(wx.VERTICAL)

        ## Search results BoxSizer sections
        #username_hbox = wx.BoxSizer(wx.HORIZONTAL)
        #username_label = wx.StaticText(search_parameters_panel, label="Username: ")
        #username_hbox.Add(username_label)
        #username_input_text = wx.TextCtrl(search_parameters_panel)
        #username_hbox.Add(username_input_text)

        #search_parameters_vbox.Add(username_hbox)
        #search_results_vbox.Add(wx.StaticText(main_panel, label="Search Results Text"))

        ##search_parameters_panel.SetSizer(search_parameters_vbox)
        ##search_results_panel.SetSizer(search_results_vbox)

        #main_hbox.Add(search_parameters_vbox)
        #main_hbox.Add(search_results_vbox)

        #main_panel.SetSizer(main_hbox)

        ##self.SetSizer(main_hbox)

        self.CreateStatusBar()

        self.Show(True)

    
    #def CoordinateSelection(self, event):

        #self.left_vbox.Add(wx.StaticText(self.left_panel, label="What is happening!"))

    def SearchButtonClick(self, event):

        self.right_vbox.Clear(True)

        #from_date = "2021-09-09"
        #to_date = "2022-09-10"
        #area_coordinates = "-30.725229, 25.084173"
        self.username = self.username_input_text.GetLineText(0)
        self.password = self.password_input_text.GetLineText(0)
        self.from_date = self.from_date_input_text.GetLineText(0)
        self.to_date = self.to_date_input_text.GetLineText(0)
        self.coordinates = list()
        self.area_coordinates = ""

        #area_coordinates = self.coordinates_input_text.GetLineText(0)
        for i in range(0,self.coordinates_input_text.GetNumberOfLines()):
            if self.coordinates_input_text.GetLineText(i) != "":
                self.coordinates.append(self.coordinates_input_text.GetLineText(i))
            #self.left_vbox.Add(wx.StaticText(self.left_panel, label=self.coordinates_input_text.GetLineText(i)))
        #print(area_coordinates)

        if self.username == "":
            # Please enter the username
            self.right_vbox.Add(wx.StaticText(self.right_panel, label="Please enter username."))

        elif self.password == "":
            # Please enter the password
            self.right_vbox.Add(wx.StaticText(self.right_panel, label="Please enter password."))

        elif self.from_date == "":
            # Please enter the from_date
            self.right_vbox.Add(wx.StaticText(self.right_panel, label="Please enter from date."))

        elif self.to_date == "":
            # Please enter the to_date
            self.right_vbox.Add(wx.StaticText(self.right_panel, label="Please enter to date."))

        elif len(self.coordinates) == 0:
            # Please enter the coordinates
            self.right_vbox.Add(wx.StaticText(self.right_panel, label="Please enter at least 1 coordinate pair."))

        elif self.username != "" and self.password != "" and self.FromAndToDateCheck(self.from_date, self.to_date) and self.CoordinatesCheck(self.coordinates):
            print("Every parameter has a value. It doesn't mean it's the correct value though.")

            #print(self.coordinates_input_text.GetNumberOfLines())
            #print(self.coordinates_input_text.GetLineText(0))
            #print(len(self.coordinates_input_text.GetLineText(0)))

            if len(self.coordinates) == 1:
                self.area_coordinates = self.coordinates[0]
                search_query = '(footprint:"Intersects(' + self.area_coordinates + ')" AND (platformname:Sentinel-1 OR platformname:Sentinel-2) AND beginposition:[' + self.from_date + 'T00:00:00.000Z TO ' + self.to_date + 'T23:59:59.999Z])'
                #search_query = "*"
            elif len(self.coordinates) > 2:
                for area_coordinate_pair in self.coordinates:
                    self.area_coordinates = self.area_coordinates + area_coordinate_pair.replace(',', ' ') + ','
                self.area_coordinates = self.area_coordinates + self.coordinates[0].replace(',', ' ')
                print(self.area_coordinates)
                print(self.coordinates)
                search_query = '(footprint:"Intersects(POLYGON((' + self.area_coordinates + ')))" AND (platformname:Sentinel-1 OR platformname:Sentinel-2) AND beginposition:[' + self.from_date + 'T00:00:00.000Z TO ' + self.to_date + 'T23:59:59.999Z])'

            api_url_search = "https://scihub.copernicus.eu/dhus/search?q="
            search_result_response = requests.get(api_url_search+search_query,
                                                  auth = HTTPBasicAuth(self.username, self.password),
                                                  allow_redirects=True)

            if search_result_response.status_code == 401:

                self.right_vbox.Add(wx.StaticText(self.right_panel, label="There has been an error with the username and password. Please enter the correct username and password"))

            elif search_result_response.status_code == 200:
                #print(search_result_response.content)
                #self.right_vbox.Add(wx.StaticText(self.right_panel, label=search_result_response.content.decode()))

                search_result_root = ET.XML(search_result_response.content)
                ET.indent(search_result_root)

                search_title = search_result_root.find("{*}title")
                search_subtitle = search_result_root.find("{*}subtitle")
                search_items_per_page = search_result_root.find("{*}itemsPerPage")
                
                self.right_vbox.Add(wx.StaticText(self.right_panel, label=search_title.text))
                self.right_vbox.Add(wx.StaticText(self.right_panel, label=search_subtitle.text))
                self.right_vbox.Add(wx.StaticText(self.right_panel, label=search_items_per_page.text))
                self.right_vbox.Add(wx.StaticText(self.right_panel, label=""))
                #print(search_title.text)
                #print(search_subtitle.text)
                #print("Items per page: {}".format(search_items_per_page.text))

                #print()
                self.entries_dict = dict()

                for entry in search_result_root.iter("{*}entry"):
                    # entry_elements = entry.iter("{*}id", "{*}title", "{*}summary")
                    entry_id = entry.find("{*}id")
                    entry_title = entry.find("{*}title")
                    entry_summary = entry.find("{*}summary")
                    #self.right_vbox.Add(wx.StaticText(self.right_panel, label="ID: {}\nTitle: {}\nSummary: {}".format(entry_id.text, entry_title.text, entry_summary.text)), proportion=1, flag=wx.ALL, border=5)
                    self.right_vbox.Add(wx.StaticText(self.right_panel, label="ID: {}\nTitle: {}\nSummary: {}".format(entry_id.text, entry_title.text, entry_summary.text), style=wx.ALIGN_LEFT))

                    download_button = wx.Button(self.right_panel, label="Download")
                    self.Bind(wx.EVT_BUTTON, self.DownloadData, id=download_button.GetId())
                    self.right_vbox.Add(download_button)

                    self.entries_dict[download_button.GetId()] = [entry_id.text, entry_title]
                    #print("ID: {}".format(entry_id.text))
                    #print("Title: {}".format(entry_title.text))
                    #print("Summary: {}".format(entry_summary.text))
                    #print("Thumbnail")
                    #for link in entry.findall("{*}link[@rel]"):
                    #    if link.attrib['rel'] == 'icon':
                    #        response = requests.get(link.attrib['href'],
                    #                                auth = HTTPBasicAuth(self.username, self.password),
                    #                                allow_redirects = True
                    #                                )
                    #        #display(Image(response.content))
                    #        print(response.text)
                    #        #self.right_vbox.Add(wx.Image(response.content))
                    #        #image = wx.Image(size=(100, 100), data=response.content)
                    #        image = wx.Image(response.text, type=wx.BITMAP_TYPE_PNG)
                    #        #image = wx.Image(size=(200, 200), data=response.text)
                    #        self.right_vbox.Add(image)

                    self.right_vbox.Add(wx.StaticText(self.right_panel, label="---------------------------------------------------------------"))
            #event.Skip()
            self.right_panel.Layout()
            #self.right_panel.Fit()
            #self.right_vbox.Layout()
            #self.right_panel.Update()
            #self.right_panel.Show()
            #print("---------------------------------------------------------------")

        else:
            # Note: This else for now will hold the other possible scenarios that didn't occur however later you
            # will have to remove it since the errors will be handled by the functions.
            
            print("This ERROR has not been caught.")


    def FromAndToDateCheck(self, from_date, to_date):
        try:
            from_date_data = date.fromisoformat(from_date)
        except ValueError:
            print("The from_date has the incorrect format.")
            return False

        try:
            to_date_data = date.fromisoformat(to_date)
        except ValueError:
            print("The to_date has the incorrect format.")
            return False

        if from_date_data > to_date_data:
            print("From date is greater than To date. From date has to be less or equal to To date.")
            return False

        if to_date_data > date.today():
        # You need to take care of ensuring that the to_date is lower than the date today.
            print("To date is greater than current date.")
            return False

        return from_date_data <= to_date_data

    def CoordinatesCheck(self, coordinates):

        for coordinate_pair in coordinates:

            if len(coordinate_pair) < 3 or not ("," in coordinate_pair) or (coordinate_pair.find(",") == len(coordinate_pair) - 1):
                print("There is an issue with the coordinate pair(s)")
                return False

            coordinate_pair_split = coordinate_pair.split(',')
            try:
                coordinate_pair_longitude = float(coordinate_pair_split[0])

            except ValueError:
                print("The longitude value should be a number")
                return False

            try:
                coordinate_pair_latitude = float(coordinate_pair_split[1])

            except ValueError:
                print("The latitude value should be a number")
                return False

            if not (-180.0 <= coordinate_pair_longitude <= 180):
                print("The longitude value should be between -180.0 and 180.0")
                return False
            elif not (-85.05 <= coordinate_pair_latitude <= 85.05):
                print("The latitude value should be between -85.05 and 85.05")
                return False

        return True

    def DownloadData(self, event):

        #print("{}".format(event.GetId()))
        #print("{}".format(self.entries_dict[event.GetId()]))
        dir_dialog = wx.DirDialog(self.right_panel, message="Download data")
        if dir_dialog.ShowModal() == wx.ID_OK:
            data_request = requests.get('https://scihub.copernicus.eu/dhus/odata/v1/' + "Products('" + self.entries_dict[event.GetId()][0] + "')/$value",
                                        auth = HTTPBasicAuth(self.username, self.password),
                                        allow_redirects=True)

            #decompressed_data = zlib.decompress(data_request.content, wbits=zlib.MAX_WBITS|32)
            #decompressed_data = zlib.decompress(data_request)

            #print(dir_dialog.GetPath())
            open(dir_dialog.GetPath() + "/" + self.entries_dict[event.GetId()][0] + ".zip", "wb").write(data_request.content)
            #print(data_request)
            #print(self.entries_dict[event.GetId()][0])
            #with open(dir_dialog.GetPath() + "/test.zip", "wb") as f:
            #    print(data_request.content)
            #    f.write(data_request.content)
            #open(dir_dialog.GetPath() + "/test.zip", "wb").write(data_request.content)
#"""
#Hello World, but with more meat.
#"""
#
#import wx
#
#class HelloFrame(wx.Frame):
#    """
#    A Frame that says Hello World
#    """
#
#    def __init__(self, *args, **kw):
#        # ensure the parent's __init__ is called
#        super(HelloFrame, self).__init__(*args, **kw)
#
#        # create a panel in the frame
#        pnl = wx.Panel(self)
#
#        # put some text with a larger bold font on it
#        st = wx.StaticText(pnl, label="Hello World!")
#        font = st.GetFont()
#        font.PointSize += 10
#        font = font.Bold()
#        st.SetFont(font)
#
#        # and create a sizer to manage the layout of child widgets
#        sizer = wx.BoxSizer(wx.VERTICAL)
#        sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
#        pnl.SetSizer(sizer)
#
#        # create a menu bar
#        self.makeMenuBar()
#
#        # and a status bar
#        self.CreateStatusBar()
#        self.SetStatusText("Welcome to wxPython!")
#
#
#    def makeMenuBar(self):
#        """
#        A menu bar is composed of menus, which are composed of menu items. This method builds a set of menus and binds handlers to be called when the menu item is selected.
#        """
#
#        # Make a file menu with Hello and Exit items
#        fileMenu = wx.Menu()
#        # The "\t..." syntax defines an accelerator key that also triggers
#        # the same event
#        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
#        "Help string shown in status bar for this menu item")
#        fileMenu.AppendSeparator()
#        # When using a stock ID we don't need to specify the menu item's
#        # label
#        exitItem = fileMenu.Append(wx.ID_EXIT)
#
#        # Now a help menu for the about item
#        helpMenu = wx.Menu()
#        aboutItem = helpMenu.Append(wx.ID_ABOUT)
#
#        # Make the menu bar and add the two menus to it. The '&' defines
#        # that the next letter is the "mnemonic" for the menu item. On the
#        # platforms that support it those letters are underlined and can be
#        # triggered from the keyboard.
#        menuBar = wx.MenuBar()
#        menuBar.Append(fileMenu, "&File")
#        menuBar.Append(helpMenu, "&Help")
#
#        # Give the menu bar to the frame
#        self.SetMenuBar(menuBar)
#
#        # Finally, associate a handler function with the EVT_MENU event for
#        # each of the menu items. That means that when that menu item is
#        # activated then the associated handler function will be called.
#        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
#        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
#        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
#
#
#    def OnExit(self, event):
#        """Close the frame, terminating the application."""
#        self.Close(True)
#
#
#    def OnHello(self, event):
#        """Say hello to the user."""
#        wx.MessageBox("Hello again from wxPython")
#
#
#    def OnAbout(self, event):
#        """Display an About Dialog"""
#        wx.MessageBox("This is a wxPython Hello World sample",
#                      "About Hello World 2",
#                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    #app = wx.App()
    #frm = HelloFrame(None, title='Hello World 2')
    #frm.Show()
    #app.MainLoop()
    app = wx.App()
    frame = MainWindow(parent=None, title="SAR and MSI Downloader")
    app.MainLoop()
