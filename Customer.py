import streamlit as st
import mysql.connector as ms
import creds 
import pandas as pd

m=ms.connect(host=creds.host, user=creds.user, password=creds.password, database=creds.database) 
mc=m.cursor()

tidbits=['Enjoy the best of baking with crumbs!','Every flavour has a story to tell!','Count the memories not the calories!','We bet you will keep coming back!','A wonderful gift for your loved ones!','Celebrate with crumbs!']
niceday=['Hope you have a good day :)','Stay hydrated :)','Just in case no one has told you already... you are amazing :)','Be a rainbow in someones storm :)','Perfection is accepting your imperfections :)']
#----------------------------------------------------------------------------------------------------------------------------
def printcakes():
    st.write('_'*50)
    st.write("Here is the menu for cakes:")
    st.write('-'*50)
    st.write('ID \t','NAME \t\t\t','PRICE_1kg \t')
    mc.execute("select * from cakes;")
    cakes=mc.fetchall()
    for i in cakes:
        l=26-len(i[1])
        i1=i[1]+' '*l
        st.write (i[0],'\t',i1,i[2])
    st.write('_'*50)
    st.write('\n')
def printbeverages():
    st.write('_'*50)
    st.write("Here is the menu for beverages:")
    st.write('-'*50)
    st.write('ID \t','NAME \t\t\t','PRICE_MEDIUM \t')
    mc.execute("select * from beverages;")
    beverages=mc.fetchall()
    for i in beverages:
        l=29-len(i[1])
        i1=i[1]+' '*l
        st.write (i[0],'\t',i1,i[2])
    st.write('_'*50)
    st.write('\n')
def printcookies():
    st.write('_'*50)
    st.write("Here is the menu for cookies:")
    st.write('-'*50)
    st.write('ID \t','NAME \t\t\t','PRICE_500g \t')
    mc.execute("select * from cookies;")
    cookies=mc.fetchall()
    for i in cookies:
        l=26-len(i[1])
        i1=i[1]+' '*l
        st.write (i[0],'\t',i1,i[2])
    st.write('_'*50)
    st.write('\n')
def printpastries():
    st.write('_'*50)
    st.write("Here is the menu for pastries:")
    st.write('-'*50)
    st.write('ID \t','NAME \t\t\t','PRICE_PERPIECE\t')
    mc.execute("select * from pastries;")
    pastries=mc.fetchall()
    for i in pastries:
        l=29-len(i[1])
        i1=i[1]+' '*l
        st.write (i[0],'\t',i1,i[2])
    st.write('_'*50)
    st.write('\n')
def printmenu():
    mc = ms.cursor()
    sql_query = "SELECT * FROM menu;"
    mc.execute(sql_query)
    data = mc.fetchall()

    # Display the list of categories using DataFrame
    st.write("Here is the list of categories:")
    for row in data:
        st.write(row)


def app():
    
    with st.form("personal_details_form"):
        st.write("Enter your personal details")
        
        name = st.text_input("Name", key="name_input").lower().strip()
        phone_no = st.text_input("Phone number", key="phone_input")

        option_key = "delivery_option" + str(hash("Do you want the order you place to be home delivered (Yes/No)"))
        option = st.radio("Do you want the order you place to be home delivered", ('Yes', 'No'), key=option_key)

        if option == 'Yes':
            address = st.text_input("Address", key="address_input")
        else:
            address= '-'
            

        submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write('\nYour personal details are:')
        st.write('Name:', name)
        st.write('Address:', address)
        st.write('Phone Number:', phone_no)
        st.write("Your information has been stored\n")
        

    if submitted:
        next_button = st.button("Next")
        if next_button:
            printmenu()

    
