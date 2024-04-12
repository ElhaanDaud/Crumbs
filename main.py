import streamlit as st
from streamlit_option_menu import option_menu
from Manager import app as Manager_app
from Customer import app as Customer_app
import mysql.connector as ms
import creds 
import pandas as pd
import random



m=ms.connect(host=creds.host, user=creds.user, password=creds.password, database=creds.database) 
mc=m.cursor()

st.set_page_config(
    page_title="Crumbs",
    page_icon="🍪"          
    )

class Crumbs:
    def __init__(self):
        self.app=[]

    def add_application(self,title,function):
        self.app.append({
            "title":title,
            "function" : function
        })

    def run(self):

        st.markdown("<h1 style='text-align: center; color: white;'>🍪 CRUMBS 🍪</h1>", unsafe_allow_html=True)
            
        
        st.text("""        
        ...................................▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄..................................    
        .                                  █▒▒░░░░░░░░░▒▒█                                 .
        .                                   █░░█░░░░░█░░█                                  .
        .                                ▄▄  █░░░▀█▀░░░█  ▄▄                               .
        .                               █░░█ ▀▄░░░░░░░▄▀ █░░█                              .
        .                               █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█                             .
        .                               █  ╦ ╦╔╗╦ ╔╗╔╗╔╦╗╔╗  █                             .
        .                               █  ║║║╠ ║ ║ ║║║║║╠   █                             .
        .                               █  ╚╩╝╚╝╚╝╚╝╚╝╩ ╩╚╝  █                             .
        ................................█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█..............................\n""")
        
        
        
        
        st.markdown("<h4 style='text-align: center; color: white;'>EXPERIENCE THE BEST OF BAKING WITH CRUMBS!! WE'LL BAKE YOUR DAY :)</h4>", unsafe_allow_html=True)
        
        

        st.text("Continue As:")

        col1, col2   = st.columns(2)

    # Add a button to the first column
        with col1:
            button1 = st.button("Manager")

    # Add a button to the second column
        with col2:
            button2 = st.button("Customer")
        
        i=0

        if button1:
            i=0
        
        elif button2:
            i=1
            
        with st.sidebar:
            app = option_menu(
                menu_title='User',
                options=['Manager','Customer'],
                icons=['house-fill','person-circle'],
                menu_icon='menu-app',  
                default_index=i,
                styles={"container":{
                        "padding":"10",
                        "background-colour":"grey"
                    },
                    "icon":{
                        "color":"white",
                        "font-size":"20px"
                        },
                    "nav-link":{
                        "color":"white",
                        "font-size":"20px",
                        "text-align":"left",
                        "--hover-color":"black"
                        },
                    "nav-link-selected":{
                        "background-color":"4a4a49",
                        },})
        

        if app == "Manager" or button1:
            Manager_app()
        if app == "Customer" or button2:
            Customer_app()

        


crumbs = Crumbs()

# Add applications to the Crumbs instance
crumbs.add_application("Manager", Manager_app)
crumbs.add_application("Customer", Customer_app)

# Run the Crumbs app
crumbs.run()
m.close()
    

