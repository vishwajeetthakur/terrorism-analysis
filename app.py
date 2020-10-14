# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 21:39:47 2020

@author: shaktimaan
CREATE CSV FILE FROM XLS FILE

"""
#to read file we used pandas


# World Chart UI with Tabs 

#importing the libraries

import pandas as pd  # used to read and operate on data easyly and flexibily like reading data from csv and to get particualrs cols as per requiremenet

import webbrowser  # used only to open the tab in the defualt brower u use used to host webiste

import dash # to create a ap and a dummy server to host the website---html file graph, 

import dash_html_components as html # as we design webpage we need html components which are available in it

from dash.dependencies import Input, State, Output  # we use it in call back to take inputs and give outputs based on it we can assume as java script as its a live actions and chnages on webpages 

import dash_core_components as dcc #plotting graph ... # to have advanced and easy to use components here graphs maps and dropdowns to be specifc

import plotly.graph_objects as go #plotly...plot over the graph.....bckend od dash..... # to generate figureres

import plotly.express as px #used to data elemtns   # to make the charts and graphs

from dash.exceptions import PreventUpdate #to prevent update # to prevent exceptions

#dash-->

# Global variables
app = dash.Dash() # 1st step to make an app in dash making object of the application as any here we made it app and we add all to app now!


def load_data(): # a function or method  to load data into df and to get some insigts of values
  dataset_name = "global_terror.csv" # the name of the file is stored in dataset_name

  #this line we use to hide some warnings which gives by pandas
  pd.options.mode.chained_assignment = None # as mentioned above
  
  global df      
  df = pd.read_csv(dataset_name)      # to read the data from csv and store in df
  
  global month_list
  month = {
         "January":1,
         "February": 2,
         "March": 3,
         "April":4,
         "May":5,
         "June":6,
         "July": 7,
         "August":8,
         "September":9,
         "October":10,
         "November":11,
         "December":12
         }                      # all the possible months are added manually 
  month_list= [{"label":key, "value":values} for key,values in month.items()]  # as we know to make a dropdown we need key (label to be specifc) and value 

  global date_list
  date_list = [x for x in range(1, 32)] # as maximum we have 31 days in any month so 1 to 31


  global region_list
  region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]  # all the regions from the dataser df col name region_txt 
  
    # unique to get all unique values
    #to list to convert into list
    #to dic to convert into dictionary
    #groupby to group the data in realtion with country and region 
    
    # try printing 1 and rest u will get to know 
  global country_list

  country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()  # all the country from the dataser df col name country_txt 

  #print(country_list)

  global state_list

  state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict() # all the state from the dataser df col name provstate 


  global city_list

  city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()  # all the city from the dataser df col name city 


  global attack_type_list
  attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()] # all the attack type from the dataser df col name attacktype1_txt 
  #print(attack_type_list)


  global year_list
  year_list = sorted ( df['iyear'].unique().tolist()  ) # similary for all years 

  global year_dict
  year_dict = {str(year): str(year) for year in year_list} # made into key value pair for dropdown

  
  #chart dropdown options
  global chart_dropdown_values                      # as we also have chart for chat key value pairs for dropdown
  chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                              
  chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()] # making them in format as required
  



def open_browser(): # a method or function to open the web browser
  # Open the default web browser
  webbrowser.open_new('http://127.0.0.1:8050/')


# Layout of your page
def create_app_ui(): # a method of function which makes the ui and all for the website
  # Create the UI of the Webpage here  
  main_layout = html.Div([         # if i have idea on html we use div and inside div we use multiple div and any other componetnts same idea here tooo
  html.H1('Terrorism Analysis with Insights', id='Main_title'),  # a simple h1 tag remember all the html functions starts with capital letter even dcc too like html.Br ot dcc.Dropdown
  dcc.Tabs(id="Tabs", value="Map",children=[                     # as per requirement we need tabs 
      dcc.Tab(label="Map tool" ,id="Map tool",value="Map", children=[   # so we made the main head tap with 2 children inside label will shwon in the output
          dcc.Tabs(id = "subtabs", value = "WorldMap",children = [    # child tabs called as subtabs
              dcc.Tab(label="World Map tool", id="World", value="WorldMap"),   # subtab 1
              dcc.Tab(label="India Map tool", id="India", value="IndiaMap")    # subtab 2
              ]),
                # all the below components are inside the main tab so all are avaiable in bot subtab 1 and 2

          dcc.Dropdown(                                     # a dropdown
              id='month',                                   # id indicated to specify it as in html 
                options=month_list,                         # what are the options rember that the format should be key value pair only check if ur confused by printing month_list or any
                placeholder='Select Month',                 #placeholder none selevcted then this message will be show inside dropdown check output for more clarity
                multi = True                                # as we want mutiple selection we made it true
                  ),                                        # close dropdown and done with 1 same for all below
          dcc.Dropdown(
                id='date', 
                placeholder='Select Day',
                multi = True
                  ),
          dcc.Dropdown(
                id='region-dropdown', 
                options=region_list,
                placeholder='Select Region',
                multi = True
                  ),
          dcc.Dropdown(
                id='country-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],          # as we know if we want data abt INDIA in it hyderabad first  south asia -> india -> Telanagan -> hyderabad 
                                                                    # so we need that path and we need filter when u sleect sound asia we should not see other countruies which are not related inside it for this we use filter
                                                                    # u will see them in call backs or now we gave all here so when region is not selected u will see in drop all which means all countries data can be slected 
                placeholder='Select Country',
                multi = True
                  ),
          dcc.Dropdown(
                id='state-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select State or Province',
                multi = True
                  ),
          dcc.Dropdown(
                id='city-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select City',
                multi = True
                  ),
          dcc.Dropdown(
                id='attacktype-dropdown', 
                options=attack_type_list,
                placeholder='Select Attack Type',
                multi = True
                  ),

          html.H5('Select the Year', id='year_title'),
          dcc.RangeSlider(                                   # for year we use range slider as we need max and min 
                    id='year-slider',                        # id to identify it and it should always be unique
                    min=min(year_list),                      # min from the data set or directly as we collected it from year_list
                    max=max(year_list),                      # max will the vise versa if u noticed in the output u will not see 1 year 1993 as its not having data its missing 
                    value=[min(year_list),max(year_list)],   # to store the data selected by the user in value 
                    marks=year_dict,                         
                    step=None
                      ),
          html.Br()
    ]),
      dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[ # same story as previously for tabs here for charts and we need 2 subtabs same stroy
          dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
              dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart", children = [          
                  html.Br(),  # br indicates line break @ 1 line gap but i noticed not working perfectly when tried 
                  dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"),  # a dropdown for the chart which we manually enteed above 
                  html.Br(),
                  html.Hr(),
                  dcc.Input(id="search", placeholder="Search Filter"), # a search for the search refer output for more idea 
                  html.Hr(),
                  html.Br()]),
              dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart", children = [html.Br(),
                  dcc.Dropdown(id="Chart_Dropdownn", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"), 
                  html.Br(),
                  html.Hr(),
                  dcc.Input(id="searchh", placeholder="Search Filter"),
                  html.Hr(),
                  html.Br()])
              ]),
         ])
     ]),
     # hope the above code is clear
  html.Div(id = "graph-object", children ="Graph will be shown here"), # as we do graphs and carts we made here from outputs we pass into this div and it will be the comment for all 4 subtabs as its completely outisde of all tabs
  ])
        
  return main_layout


# Callback of your page
@app.callback(dash.dependencies.Output('graph-object', 'children'),  # callback output is graph 
    [
    dash.dependencies.Input("Tabs", "value"),   # we gave ids and we use that ids to track the values in them which the user entered 
    dash.dependencies.Input('month', 'value'), # as above all inputs that user gave 
    dash.dependencies.Input('date', 'value'),
    dash.dependencies.Input('region-dropdown', 'value'),
    dash.dependencies.Input('country-dropdown', 'value'),
    dash.dependencies.Input('state-dropdown', 'value'),
    dash.dependencies.Input('city-dropdown', 'value'),
    dash.dependencies.Input('attacktype-dropdown', 'value'),
    dash.dependencies.Input('year-slider', 'value'), 
    
    dash.dependencies.Input("Chart_Dropdown", "value"), # check the names with above i mean ids and they should match else graph could be missing
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input("subtabs2", "value"),

    dash.dependencies.Input("Chart_Dropdownn", "value"),
    dash.dependencies.Input("searchh", "value"),
    dash.dependencies.Input("subtabs2", "value"),
    ]
    )

def update_app_ui(Tabs, month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,chart_dp_value, search,
                   subtabs2,Chart_Dropdownn_value,searchh,subtabs22):   # collect all the above values to a function and to return the final graph
    fig = None
     
    if Tabs == "Map":   # all the values of map are printer just for reference 
        print("Data Type of month value = " , str(type(month_value)))
        print("Data of month value = " , month_value)
        
        print("Data Type of Day value = " , str(type(date_value)))
        print("Data of Day value = " , date_value)
        
        print("Data Type of region value = " , str(type(region_value)))
        print("Data of region value = " , region_value)
        
        print("Data Type of country value = " , str(type(country_value)))
        print("Data of country value = " , country_value)
        
        print("Data Type of state value = " , str(type(state_value)))
        print("Data of state value = " , state_value)
        
        print("Data Type of city value = " , str(type(city_value)))
        print("Data of city value = " , city_value)
        
        print("Data Type of Attack value = " , str(type(attack_value)))
        print("Data of Attack value = " , attack_value)
        
        print("Data Type of year value = " , str(type(year_value)))
        print("Data of year value = " , year_value)

        # year_filter
        year_range = range(year_value[0], year_value[1]+1)  # as user given 2 year and we get the years assue 1999 to 2005 given
                                                            # range(x,y) gets all values b/n them x to y without including y 
                                                            # hence we increment range(x,y+1) so we get all b/n x to y 
                                                            # (1999,2000,2001,2002,2003,2004,2005)
        new_df = df[df["iyear"].isin(year_range)]           # filtering all data in that years 
        
        # month_filter
        if month_value==[] or month_value is None:          # if no month is slected just pass and ntg to do 
            pass
        else:                                               # else (means if selected)
            if date_value==[] or date_value is None:                    # check if date is not  slected now
                new_df = new_df[new_df["imonth"].isin(month_value)]     # here as date is not selected filter data only based on month
            else:                                                    # else (means if  selcted )
                new_df = new_df[new_df["imonth"].isin(month_value)         # both month and date filter only that data (use and operation (&))
                                & (new_df["iday"].isin(date_value))]
        # region, country, state, city filter             
        if region_value==[] or region_value is None:       # if month not selcted just pass
            pass
        else:                                              # else (means if month selected)
            if country_value==[] or country_value is None :     # and if country not selected go inside
                new_df = new_df[new_df["region_txt"].isin(region_value)]   # do filtering data based on the user region 
            else:                                                   # else(means country selected)
                if state_value == [] or state_value is None:                   # if state not selected  
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&    # # then do filtering based on region and country as state is not selected
                                    (new_df["country_txt"].isin(country_value))] 
                else:                           # else (means state selected )
                    if city_value == [] or city_value is None:              # if city not selected 
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&           # means  region country and state selcected hence do filtering based on them
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))]
                    else:                                                 # else (means city selected )
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&     # hence do filtering for all region country state and city 
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))&
                        (new_df["city"].isin(city_value))]
                         
        if attack_value == [] or attack_value is None:            # if attack value not selcted pass
            pass
        else:                                                     # else means its selected 
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)]        # hence filter based on it too now
        
        # N O T E: all the operations are done on new_df and stored in new_df and out original df is safe
        # hence in all the cases we use new_df to do graphs charts ot any



         # You should always set the figure for blank, since this callback 
         # is called once when it is drawing for first time        
        mapFigure = go.Figure()     # to craete data an empty figure and store in mapFigure
        if new_df.shape[0]:         # df.shape normally give no. of (rows,cols) as we use new_df.shape[0] we get no. rows ie. no of records after passing through all filters
            pass                    # if their is atlest 1 record pass 
        else:                       # else clean it to nothing
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]       # make all usual so we can redo according to requirement
            
        
        mapFigure = px.scatter_mapbox(new_df,   # plotting the graph
          lat="latitude",                         # lat and long to mark the point dataset col names should be given  same for bellow
          lon="longitude",
          color="attacktype1_txt",                  
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1                                    # zoom value can be 1 to 15 1 is min zoom @ zoom out
          )                       # everything is in mapFigure all data i mean
        mapFigure.update_layout(mapbox_style="open-street-map",                      # now update the graph which was empty previously
          autosize=True,                     # auto size to make the points in center @ ajust it 
          margin=dict(l=0, r=0, t=25, b=20), #  margins form all side @ l-left r-right t-top b-bottom
          )
          
        fig = mapFigure                      # finally store the mapFigure in fig 

    elif Tabs=="Chart":                          # now if we selected tab was chart
        fig = None                               # if their is any fig already make it None i.e making into empty or NULL 
        if subtabs2 == "WorldChart":              # if world chart selected 
            if chart_dp_value is not None:            # here chart_dp_value is selcted
                if search is not None:                # here search is that input search which we can enter is also entered
                    chart_df = df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")    # as none are insered collect the years data of that particualr colw hich we selcted and count them and store in count
                    chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case = False)]        # as selcted col is done now based on search print only reuired ones
                else:                                                                                         # this else means search not given
                    chart_df = df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")   # hence do only once for the dropdown
            else:                                                                                             # if dropdown also not selcted dont update any
                raise PreventUpdate
            chartFigure = px.area(chart_df, x= "iyear", y ="count", color = chart_dp_value)           # finally make a chart for year and count 
            fig = chartFigure                                                                         # store in fig
            #print(chart_df)
        elif subtabs22 == "IndiaChart":                                      # id india is selcted 

            # i think this logic is which i used even u can refer sirs code for more reference

            n_df=df[ [df['region_txt']=="South Asia"] and df['country_txt']=="India"] # fix refion and country and do same process

            if Chart_Dropdownn_value is not None:
                if searchh is not None: 
                    chart_df = n_df.groupby("iyear")[Chart_Dropdownn_value].value_counts().reset_index(name = "count")
                    chart_df  = chart_df[chart_df[Chart_Dropdownn_value].str.contains(searchh, case = False)]
                else:
                    chart_df = n_df.groupby("iyear")[Chart_Dropdownn_value].value_counts().reset_index(name="count")
            else:
                raise PreventUpdate
            chartFigure = px.area(chart_df, x= "iyear", y ="count", color = Chart_Dropdownn_value)
            fig = chartFigure

        else:
            return None
    return dcc.Graph(figure = fig)

# hence ur done with making fugure and the ui

@app.callback(                         # the dropdown when a month selected 
  Output("date", "options"),
  [Input("month", "value")])
def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]       # commonly pass all days 1 to 31 as its esay and best approactch 
    return option

@app.callback([Output("region-dropdown", "value"),
               Output("region-dropdown", "disabled"),
               Output("country-dropdown", "value"),
               Output("country-dropdown", "disabled")],             # desable means we fix that calue check output for more info in india map tool
              [Input("subtabs", "value")])                   # based on subtab value 
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":          # above are just flags to use if tab is world map do nothing just pass
        pass
    elif tab=="IndiaMap":          # if india is selcted only india hence region and country are fixed 
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c  # return all the parameters and disable them use , to separe reurns of multiple values 



@app.callback(
    Output('country-dropdown', 'options'),       # a small logic to filter the all the reuired regions countries
    [Input('region-dropdown', 'value')])
def set_country_options(region_value):
    option = []
    # Making the country Dropdown data
    if region_value is  None:                # if none is selcted pass
        raise PreventUpdate
    else:                                    # if selected we can use ant this approatch is better 
                                                # as anytime we need to add or remove a region hence everytime we do thsi
        for var in region_value:                 # do for each region selcted 
            if var in country_list.keys():        # check all and add them to options
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]      # make options into the same key value pair and return 

# same process for the bellow call backs too hope its clear


@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]
@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def set_city_options(state_value):
  # Making the city Dropdown data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]

# Flow of your Project
def main():  # finally the main  execusion starts here
  load_data()   # calling functions  (loading data)
  
  open_browser()  # open the browser 
   
  global app
  app.layout = create_app_ui()  # make app ui and pust into app layout
  app.title = "Terrorism Analysis with Insights"           # title of the website which u can see on tab check out put for more idea
  # go to https://www.favicon.cc/ and download the ico file and store in assets directory 
  app.run_server() # debug=True                 # to start the app to run

  print("This would be executed only after the script is closed")   # a message to prince once we stop the sever 
  #df = None
  app = None   # de allocating the spaces 



if __name__ == '__main__':
    main()




