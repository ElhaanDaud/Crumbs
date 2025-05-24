import streamlit as st
import mysql.connector as ms
import creds 
import pandas as pd
import datetime # Added for timestamping orders

# Remove local database connection
# m=ms.connect(host=creds.host, user=creds.user, password=creds.password, database=creds.database) 
# mc=m.cursor()

# tidbits and niceday lists can be kept if used exclusively by Customer.py, or moved to main.py if shared
tidbits=['Enjoy the best of baking with crumbs!','Every flavour has a story to tell!','Count the memories not the calories!','We bet you will keep coming back!','A wonderful gift for your loved ones!','Celebrate with crumbs!']
niceday=['Hope you have a good day :)','Stay hydrated :)','Just in case no one has told you already... you are amazing :)','Be a rainbow in someones storm :)','Perfection is accepting your imperfections :)']
#----------------------------------------------------------------------------------------------------------------------------
def printcakes(mc_main): # Accept cursor
    st.write("Here is the menu for cakes:")
    mc_main.execute("select * from cakes;")
    cakes=mc_main.fetchall()
    df = pd.DataFrame(cakes, columns=['ID', 'Name', 'Price'])
    st.dataframe(df)
    
def printbeverages(mc_main): # Accept cursor
    st.write("Here is the menu for beverages:")
    mc_main.execute("select * from beverages;")
    beverages=mc_main.fetchall()
    df = pd.DataFrame(beverages, columns=['ID', 'Name', 'Price'])
    st.dataframe(df)
    
def printcookies(mc_main): # Accept cursor
    st.write("Here is the menu for cookies:")
    mc_main.execute("select * from cookies;")
    cookies=mc_main.fetchall()
    df = pd.DataFrame(cookies, columns=['ID', 'Name', 'Price'])
    st.dataframe(df)
    
    
def printpastries(mc_main): # Accept cursor
    st.write("Here is the menu for pastries:")
    mc_main.execute("SELECT * FROM pastries;")
    pastries = mc_main.fetchall()
    df = pd.DataFrame(pastries, columns=['ID', 'Name', 'Price'])
    st.dataframe(df)
    
  
def printmenu(mc_main): # Accept cursor
    sql_query = "SELECT * FROM menu;"
    mc_main.execute(sql_query)
    data = mc_main.fetchall()
    st.write("Here is the list of categories:")
    df = pd.DataFrame(data, columns=['ID', 'Category Name'])
    st.dataframe(df)
    return data # Return categories for selection

def app(db_cursor, db_connection): # Accept cursor and connection (for commit)
    mc = db_cursor # Use the passed cursor
    m = db_connection # Use the passed connection

    if 'order' not in st.session_state:
        st.session_state.order = []
    if 'customer_details' not in st.session_state:
        st.session_state.customer_details = {}
    if 'view' not in st.session_state:
        st.session_state.view = 'personal_details'

    if st.session_state.view == 'personal_details':
        with st.form("personal_details_form", clear_on_submit=False): # Keep data for later
            st.write("Enter your personal details")
            
            name = st.text_input("Name", key="name_input").lower().strip()
            phone_no = st.text_input("Phone number", key="phone_input")
            delivery_option_key = "delivery_option" + str(hash("Do you want the order you place to be home delivered (Yes/No)"))
            option = st.radio("Do you want the order you place to be home delivered", ('Yes', 'No'), key=delivery_option_key)

            if option == 'Yes':
                address = st.text_input("Address", key="address_input")
            else:
                address = '-'
            
            submitted_personal_details = st.form_submit_button("Submit Details")
        
        if submitted_personal_details:
            if not name or not phone_no:
                st.error("Name and Phone number are required.")
            else:
                st.session_state.customer_details = {
                    'name': name,
                    'phone_no': phone_no,
                    'option': option,
                    'address': address
                }
                st.session_state.view = 'category_selection'
                st.experimental_rerun() # Rerun to update view

    if st.session_state.view == 'category_selection':
        st.write('\nYour personal details are:')
        st.write('Name:', st.session_state.customer_details.get('name'))
        st.write('Address:', st.session_state.customer_details.get('address'))
        st.write('Phone Number:', st.session_state.customer_details.get('phone_no'))
        st.write("Your information has been stored\n")
        
        st.header("Select a Category to Order From")
        categories = printmenu(mc) # Pass cursor
        
        category_options = {cat[1]: cat[0] for cat in categories} # Name: ID
        selected_category_name = st.selectbox("Choose a category:", options=list(category_options.keys()))

        if selected_category_name:
            st.session_state.selected_category_id = category_options[selected_category_name]
            st.session_state.selected_category_name = selected_category_name
            st.session_state.view = 'item_selection'
            st.experimental_rerun()

    elif st.session_state.view == 'item_selection':
        st.header(f"Menu for {st.session_state.selected_category_name}")
        category_id = st.session_state.selected_category_id
        
        items_df = pd.DataFrame()
        if category_id == 'C00': # Cakes
            printcakes(mc) # Pass cursor
            mc.execute("SELECT * FROM cakes;")
            items = mc.fetchall()
            items_df = pd.DataFrame(items, columns=['ID', 'Name', 'Price_1kg'])
        elif category_id == 'B00': # Beverages
            printbeverages(mc) # Pass cursor
            mc.execute("SELECT * FROM beverages;")
            items = mc.fetchall()
            items_df = pd.DataFrame(items, columns=['ID', 'Name', 'Price_Medium'])
        elif category_id == 'K00': # Cookies
            printcookies(mc) # Pass cursor
            mc.execute("SELECT * FROM cookies;")
            items = mc.fetchall()
            items_df = pd.DataFrame(items, columns=['ID', 'Name', 'Price_500g'])
        elif category_id == 'P00': # Pastries
            printpastries(mc) # Pass cursor
            mc.execute("SELECT * FROM pastries;")
            items = mc.fetchall()
            items_df = pd.DataFrame(items, columns=['ID', 'Name', 'Price_Piece'])
        
        if not items_df.empty:
            item_names = items_df['Name'].tolist()
            selected_item_name = st.selectbox("Select an item:", item_names)
            
            if selected_item_name:
                selected_item_details = items_df[items_df['Name'] == selected_item_name].iloc[0]
                item_id = selected_item_details['ID']
                price = selected_item_details.iloc[2] # Price is the 3rd column

                quantity = 1
                weight = 0.5 # default for cakes/cookies
                size = 'Medium' # default for beverages

                if category_id == 'C00': # Cakes
                    weight = st.radio("Select weight (kg):", (0.25, 0.5, 1.0, 2.0), index=1)
                    # Price is per kg, adjust
                    calculated_price = (weight / 1.0) * price 
                elif category_id == 'K00': # Cookies
                    weight = st.radio("Select weight (g):", (150, 250, 500), index=2)
                    # Price is per 500g, adjust
                    calculated_price = (weight / 500.0) * price 
                elif category_id == 'B00': # Beverages
                    size_options = {'Small': 0.75, 'Medium': 1.0, 'Large': 1.5}
                    size = st.radio("Select size:", list(size_options.keys()), index=1)
                    quantity = st.number_input("Quantity:", min_value=1, value=1)
                    calculated_price = size_options[size] * price * quantity
                elif category_id == 'P00': # Pastries
                    quantity = st.number_input("Quantity (pieces):", min_value=1, value=1)
                    calculated_price = price * quantity
                else:
                    calculated_price = price # Should not happen

                st.write(f"Price for {selected_item_name}: {calculated_price:.2f}")

                if st.button("Add to Order"):
                    order_item = {
                        "id": item_id,
                        "name": selected_item_name,
                        "category": st.session_state.selected_category_name,
                        "quantity": quantity,
                        "weight": weight if category_id in ['C00', 'K00'] else None,
                        "size": size if category_id == 'B00' else None,
                        "price": calculated_price
                    }
                    st.session_state.order.append(order_item)
                    st.success(f"{selected_item_name} added to your order!")
        
        if st.button("View Another Category"):
            st.session_state.view = 'category_selection'
            st.experimental_rerun()
        
        if st.button("View Cart & Proceed to Checkout"):
            st.session_state.view = 'cart_view'
            st.experimental_rerun()

    elif st.session_state.view == 'cart_view':
        st.header("Your Current Order")
        if not st.session_state.order:
            st.write("Your cart is empty.")
            if st.button("Add Items"):
                st.session_state.view = 'category_selection'
                st.experimental_rerun()
            return

        cart_df = pd.DataFrame(st.session_state.order)
        # Ensure all relevant columns are present, fillna for display if necessary
        display_cols = ['name', 'price']
        if 'quantity' in cart_df.columns: display_cols.insert(1, 'quantity')
        if 'weight' in cart_df.columns: display_cols.insert(2, 'weight')
        if 'size' in cart_df.columns: display_cols.insert(3, 'size')
        
        # Filter out columns that might be all None for cleaner display
        cart_df_display = cart_df[display_cols].copy()
        for col in ['quantity', 'weight', 'size']:
            if col in cart_df_display.columns and cart_df_display[col].isnull().all():
                cart_df_display.drop(columns=[col], inplace=True)
        
        st.dataframe(cart_df_display)
            
        subtotal = sum(item['price'] for item in st.session_state.order)
        st.write(f"**Subtotal: {subtotal:.2f}**")

        taxes = subtotal * 0.18  # GST 18%
        st.write(f"**GST (18%): {taxes:.2f}**")
        
        total_before_delivery = subtotal + taxes
        delivery_charge = 0
        customer_details = st.session_state.customer_details
        if customer_details.get('option') == 'Yes': # Home delivery
            if total_before_delivery > 500:
                delivery_charge = 50
                st.write(f"**Delivery Charge: {delivery_charge:.2f}**")
            else:
                st.info("Home delivery is available for orders above Rs. 500 (after tax). Your current total is not eligible.")
        
        grand_total = total_before_delivery + delivery_charge
        st.session_state.grand_total = grand_total # Store for confirmation page
        st.write(f"**Grand Total: {grand_total:.2f}**")

        if st.button("Add More Items"):
            st.session_state.view = 'category_selection'
            st.experimental_rerun()
            
        if st.button("Place Order"):
            st.session_state.view = 'order_confirmation'
            st.experimental_rerun()

    elif st.session_state.view == 'order_confirmation':
        st.header("Confirm Your Order")
        
        customer_details = st.session_state.customer_details
        st.write("### Review Your Details:")
        st.write(f"Name: {customer_details.get('name')}")
        st.write(f"Phone: {customer_details.get('phone_no')}")
        if customer_details.get('option') == 'Yes':
            st.write(f"Address: {customer_details.get('address')}")
        st.write("---")
        
        st.write("### Order Summary:")
        if not st.session_state.order: # Should not happen if navigated correctly
            st.write("Your cart is empty.")
            if st.button("Go Back to Menu"):
                st.session_state.view = 'category_selection'
                st.experimental_rerun()
            return

        cart_df = pd.DataFrame(st.session_state.order)
        # Ensure all relevant columns are present, fillna for display if necessary
        display_cols = ['name', 'price']
        if 'quantity' in cart_df.columns: display_cols.insert(1, 'quantity')
        if 'weight' in cart_df.columns: display_cols.insert(2, 'weight')
        if 'size' in cart_df.columns: display_cols.insert(3, 'size')
        
        cart_df_display = cart_df[display_cols].copy()
        for col in ['quantity', 'weight', 'size']:
            if col in cart_df_display.columns and cart_df_display[col].isnull().all():
                cart_df_display.drop(columns=[col], inplace=True)
        st.dataframe(cart_df_display)
        
        subtotal = sum(item['price'] for item in st.session_state.order)
        taxes = subtotal * 0.18
        total_before_delivery = subtotal + taxes
        delivery_charge = 0
        if customer_details.get('option') == 'Yes' and total_before_delivery > 500:
            delivery_charge = 50
        
        grand_total = st.session_state.grand_total # Fetched from previous calculation
        
        st.write(f"**Subtotal: {subtotal:.2f}**")
        st.write(f"**GST (18%): {taxes:.2f}**")
        if delivery_charge > 0:
            st.write(f"**Delivery Charge: {delivery_charge:.2f}**")
        st.write(f"**Grand Total: {grand_total:.2f}**")
        st.write("---")

        if st.button("Confirm & Pay (Simulated)"):
            try:
                order_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Ensure address is present if delivery option was yes, else '-'
                address_to_save = customer_details.get('address', '-')
                if customer_details.get('option') == 'No':
                    address_to_save = '-'

                val = (customer_details.get('name'), 
                       address_to_save, 
                       customer_details.get('phone_no'), 
                       float(grand_total), # Ensure it's float
                       order_date)
                sql = """INSERT INTO c_details (name, address, phone_no, amount, date_time)
                         VALUES (%s, %s, %s, %s, %s)"""
                mc.execute(sql, val) # Use the passed cursor
                m.commit() # Use the passed connection for commit
                
                st.success("Your order has been placed successfully!")
                st.balloons()
                
                # Clear order and reset view
                st.session_state.order = []
                st.session_state.view = 'personal_details' # Or a thank you page
                # Clear customer details as well if starting fresh
                # st.session_state.customer_details = {} 
                if st.button("Place Another Order"):
                    st.experimental_rerun()

            except ms.Error as err:
                st.error(f"Database error: {err}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

        if st.button("Go Back to Cart"):
            st.session_state.view = 'cart_view'
            st.experimental_rerun()
