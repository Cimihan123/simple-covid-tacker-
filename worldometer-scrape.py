from requests_html import HTMLSession
import requests
import pandas as pd
import numpy as np



def covidTrack(url):
    r_html = HTMLSession()
    response =  r_html.get(url)
    #cases
    counts = response.html.find(".content-inner")
    container = counts[0].text
    cases = response.html.find('#maincounter-wrap')
    title = ([(x.text).replace('\n',' ') for x in cases])
    #headers
    table = (response.html.find(".table"))[0]
    table_row = table.find('tr') #table rows
    rows = table_row[0]
    table_head = rows.find('th') #table headers
    table_heads = [ (i.text).replace('\n',' ') for i in table_head[1:] ]

    table1 = response.html.find('#main_table_countries_today')[0]
    t_body =  table1.find('tr')[9:224]
    table_data = []
    for t in t_body:
        col = t.find('td')
        datas =[]


        for i  in col[1:]:
             datas.append(i.text)
        table_data.append(datas)

    df = pd.DataFrame(table_data,columns=table_heads,index=np.arange(215))
    df.to_csv('sau.csv',index=False)

url = "https://www.worldometers.info/coronavirus/"
covidTrack(url)


file = pd.read_csv('sau.csv')
county_name = input('what is your country name ?')
locate =  file.loc[file['Country, Other']== county_name]
print(locate)





