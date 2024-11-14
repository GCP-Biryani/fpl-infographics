import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from bs4 import BeautifulSoup
from tabulate import tabulate
pd.options.mode.chained_assignment = None

#
PLAYERS_DF = pd.read_csv("players_data.csv")
#
# page config
st.set_page_config(
    page_title="Latest price changes • FPL Infographics", page_icon=":soccer:",layout="wide"
)
LOGO = "logo.png"
st.logo(
    LOGO,
    icon_image=LOGO,
    )

# sidebar
with st.sidebar:
    st.markdown(""":soccer: :green[FPL] *Infographics*""")
    st.caption(
        """[GCP Biryani](https://github.com/GCP-Biryani)"""
    )

############
st.markdown(
    "##### :money_mouth_face: Price changes & price predictions"
)
tab1, tab2, tab3 = st.tabs(["Today price changes","Price change predictions","Injury News"])
with tab2:
    url = 'https://www.livefpl.net/prices'          # Price Changes
    header = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, 'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))[0]
    headers = []
    rows = []
    for i, row in enumerate(table.find_all('tr')):
        if i == 0:
            headers = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    table = tabulate(
        rows, 
        headers=["State", "Predicted Rises", "Predicted Falls"], 
        tablefmt="rounded_grid"
    )
    # st.dataframe(df,hide_index=True,width=1400)
    st.table(df)
with tab1:
    url = 'https://www.livefpl.net/price_changes'          # Price Changes
    header = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, 'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))[0]

    headers = []
    rows = []
    for i, row in enumerate(table.find_all('tr')):
        if i == 0:
            headers = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    table1 = tabulate(
        rows, 
        headers=["Player", "Team", "Old price", "New Price"], 
        tablefmt="rounded_grid"
    )
    st.dataframe(df,hide_index=True,width=1400)
with tab3:
    D_DF = pd.read_csv("players_raw.csv")
    DOUBT_DF = D_DF[D_DF['status'] == 'd']
    DOUBT_DF['news_added'] = DOUBT_DF['news_added'].apply(lambda x: x.split('T')[0])
    DOUBT_DF = DOUBT_DF[['web_name','news','news_added']].sort_values('news_added',ascending=False)
    DOUBT_DF.rename(columns={'web_name': 'Name','news_added':'Updated'}, inplace=True)

    st.dataframe(data=DOUBT_DF,hide_index=True,use_container_width=False,width=800, height=1500)