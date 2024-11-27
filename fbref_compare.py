import streamlit as st
from fbref_functions import *

##############################
# page config
st.set_page_config(
    page_title="Player comparision tool", page_icon=":soccer:",layout="wide"
)
LOGO = "logo.png"
st.logo(
    LOGO,
    icon_image=LOGO,
    )
# sidebar
with st.sidebar:
    st.title(""":soccer: *Player comparision tool*""")
    st.caption("Compare player performance, expected, shooting, passing, defensive stats")
    
##############################
def main():    
    st.title("Player Comparision tool")
    player_season_compare()

if __name__ == "__main__":
    main()