import streamlit as st
from streamlit_option_menu import option_menu
import Customer, Manager, home, creds 
import mysql.connector as ms
import random



m=ms.connect(host=creds.host, user=creds.user, password=creds.password, database=creds.database) 
mc=m.cursor()

st.set_page_config(
    page_title="Crumbs",
    page_icon="🍪",   
    )

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        
        st.text("Continue As:")

        col1, col2   = st.columns([6,1])

    # Add a button to the second column
        with col1:
            button1 = st.button("Customer")

    # Add a button to the first column
        with col2:
            button2 = st.button("Manager")

        i=0

        if button1:
            i=1
            app="Customer"

        elif button2:
            i=2
            app = "Manager"
            
        with st.sidebar:
            app = option_menu(
                menu_title='User',
                options=['Home','Customer','Manager',],
                icons=['house-fill','person-lines-fill','person-circle'],
                menu_icon='menu-app',  
                default_index=i,
                styles={"container": {
                    "padding": "5!important",
                    "background-color":'black'
                    },
            "icon": {
                "color": "white", 
                "font-size": "23px"
                }, 
            "nav-link": {
                "color":"white",
                "font-size": "20px", 
                "text-align": "left", 
                "margin":"0px", 
                "--hover-color": "blue"},

            "nav-link-selected": {
                "background-color": "#02ab21"
                },})
        
        tidbits=['Enjoy the best of baking with crumbs!','Every flavour has a story to tell!','Count the memories not the calories!','We bet you will keep coming back!','A wonderful gift for your loved ones!','Celebrate with crumbs!']
        niceday=['Hope you have a good day :)','Stay hydrated :)','Just in case no one has told you already... you are amazing :)','Be a rainbow in someones storm :)','Perfection is accepting your imperfections :)']
        
        if app == "Home":
            i=0
            home.app()

        if app == "Customer":
            yapping=random.choice(tidbits)
            st.text(yapping)
            Customer.app()
            

        if app == "Manager":
            yapping=random.choice(niceday)
            st.text(yapping)
            Manager.app()

    run()


    

