import streamlit as st
from streamlit_option_menu import option_menu
import streamlit as st
from streamlit_option_menu import option_menu
import Customer, Manager, home, creds 
import mysql.connector as ms
import random

# Initialize a single database connection and cursor
# Ensure buffered=True for the cursor, as it's beneficial for Streamlit apps
# where multiple execute calls might happen on the same cursor.
try:
    db_connection = ms.connect(
        host=creds.host, 
        user=creds.user, 
        password=creds.password, 
        database=creds.database
    )
    db_cursor = db_connection.cursor(buffered=True)
    # st.success("Database connected successfully!") # Optional: for debugging
except ms.Error as err:
    st.error(f"Error connecting to database: {err}")
    # Optionally, halt execution or disable DB-dependent parts of the app
    db_connection = None
    db_cursor = None

st.set_page_config(
    page_title="Crumbs",
    page_icon="🍪",   
)

# tidbits and niceday lists for random messages
tidbits=['Enjoy the best of baking with crumbs!','Every flavour has a story to tell!','Count the memories not the calories!','We bet you will keep coming back!','A wonderful gift for your loved ones!','Celebrate with crumbs!']
niceday=['Hope you have a good day :)','Stay hydrated :)','Just in case no one has told you already... you are amazing :)','Be a rainbow in someones storm :)','Perfection is accepting your imperfections :)']

def run_app():
    # Determine initial default_index for option_menu if needed, or set to 0 (Home)
    # The previous logic with buttons is removed for simplification, relying solely on option_menu
    default_page_index = 0 
            
    with st.sidebar:
        selected_app = option_menu(
            menu_title='User Navigation', # Changed title for clarity
            options=['Home','Customer','Manager'],
            icons=['house-fill','person-lines-fill','person-circle'],
            menu_icon='menu-button-wide', # Changed icon
            default_index=default_page_index,
            styles={
                "container": {"padding": "5px !important", "background-color":'#f0f2f6'}, # Light grey background
                "icon": {"color": "#007bff", "font-size": "23px"}, # Blue icons
                "nav-link": {
                    "color":"#333", # Darker text for readability
                    "font-size": "18px", 
                    "text-align": "left", 
                    "margin":"5px", 
                    "--hover-color": "#e9ecef" # Light hover color
                },
                "nav-link-selected": {"background-color": "#007bff", "color": "white"}, # Blue selected link
            }
        )
    
    if selected_app == "Home":
        home.app()

    elif selected_app == "Customer":
        if db_cursor and db_connection:
            yapping = random.choice(tidbits)
            st.info(yapping) # Using st.info for better visibility
            Customer.app(db_cursor, db_connection) # Pass cursor and connection
        else:
            st.error("Database connection is not available. Customer section cannot be loaded.")
            
    elif selected_app == "Manager":
        if db_cursor and db_connection:
            yapping = random.choice(niceday)
            st.info(yapping) # Using st.info for better visibility
            Manager.app(db_cursor, db_connection) # Pass cursor and connection
        else:
            st.error("Database connection is not available. Manager section cannot be loaded.")

if __name__ == '__main__':
    run_app()

# Proper closing of connection (though Streamlit's script execution model might make this tricky for long-lived apps)
# For typical Streamlit apps that rerun script on interaction, this explicit close might not always execute as expected.
# However, it's good practice if the app were to run continuously or if connection pooling isn't used.
# if db_connection and db_connection.is_connected():
#     db_cursor.close()
#     db_connection.close()
#     print("MySQL connection is closed") # For server logs, not Streamlit UI

