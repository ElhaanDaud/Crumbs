import streamlit as st
from streamlit_option_menu import option_menu
from Manager import app as Manager_app
from Customer import app as Customer_app
import mysql.connector as ms
import creds 
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

        elif button2:
            i=2
        
        
            
        with st.sidebar:
            app = option_menu(
                menu_title='User',
                options=['Home','Customer','Manager',],
                icons=['house-fill','person-lines-fill','person-circle'],
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
        
        tidbits=['Enjoy the best of baking with crumbs!','Every flavour has a story to tell!','Count the memories not the calories!','We bet you will keep coming back!','A wonderful gift for your loved ones!','Celebrate with crumbs!']
        niceday=['Hope you have a good day :)','Stay hydrated :)','Just in case no one has told you already... you are amazing :)','Be a rainbow in someones storm :)','Perfection is accepting your imperfections :)']
        
        if app == "Home ":
            i=0

        if app == "Customer" or button1:
            st.write(random.choice(tidbits))
            Customer_app()
            

        if app == "Manager" or button2:
            st.write(random.choice(niceday))
            Manager_app()
            
        

        


crumbs = Crumbs()

# Add applications to the Crumbs instance
crumbs.add_application("Manager", Manager_app)
crumbs.add_application("Customer", Customer_app)

# Run the Crumbs app
crumbs.run()
m.close()
    

