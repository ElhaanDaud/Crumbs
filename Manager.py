import streamlit as st
import creds 
import mysql.connector as ms
import pandas as pd # Added for dataframe operations

# Database connection removed from here
# m = ms.connect(host=creds.host, user=creds.user, password=creds.password, database=creds.database) 
# mc = m.cursor(buffered=True) 

# Helper function to get table data, now accepts cursor
def get_table_data(mc_main, table_name): # Accept cursor
    try:
        mc_main.execute(f"SELECT * FROM {table_name};")
        data = mc_main.fetchall()
        columns = [i[0] for i in mc_main.description]
        return pd.DataFrame(data, columns=columns)
    except ms.Error as err:
        st.error(f"Error fetching data from {table_name}: {err}")
        return pd.DataFrame()

def app(db_cursor, db_connection): # Accept cursor and connection
    mc = db_cursor # Use the passed cursor
    m = db_connection # Use the passed connection

    st.title("Manager Dashboard")

    # Initialize session state for login
    if 'manager_logged_in' not in st.session_state:
        st.session_state['manager_logged_in'] = False
    if 'current_view' not in st.session_state:
        st.session_state['current_view'] = 'login' # Default view

    # Login Section
    if not st.session_state['manager_logged_in']:
        st.subheader("Manager Login")
        with st.form("login_form"):
            manager_id = st.text_input("Manager ID")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

            if login_button:
                try:
                    # Secure way to query: use placeholders
                    query = "SELECT * FROM admin WHERE id = %s AND password = %s"
                    mc.execute(query, (manager_id, password)) # Use passed mc
                    result = mc.fetchone() # Use fetchone as ID should be unique

                    if result:
                        st.session_state['manager_logged_in'] = True
                        st.session_state['manager_id'] = manager_id
                        st.session_state['current_view'] = 'main_menu' # Navigate to main menu
                        st.experimental_rerun() # Rerun to reflect login state
                    else:
                        st.error("Invalid Manager ID or Password.")
                except ms.Error as err:
                    st.error(f"Database error during login: {err}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
    
    # Main Application Area - Visible after login
    if st.session_state['manager_logged_in']:
        st.sidebar.success(f"Logged in as {st.session_state.get('manager_id', 'Manager')}")
        
        # Navigation
        menu_options = ["View Records", "Insert Records", "Update Records", "Delete Records", "Logout"]
        st.session_state.current_view = st.sidebar.radio("Navigation", menu_options, key="navigation_choice")

        if st.session_state.current_view == "Logout":
            st.session_state['manager_logged_in'] = False
            st.session_state['manager_id'] = None
            st.session_state['current_view'] = 'login' # Reset to login view
            st.experimental_rerun()
        
        st.header(st.session_state.current_view) # Display the current selected view as header

        if st.session_state.current_view == "View Records":
            st.subheader("View Table Records")
            # Tables allowed for viewing by manager
            viewable_tables = ['beverages', 'cakes', 'cookies', 'employee', 'menu', 'pastries', 'personal_details']
            
            selected_table_to_view = st.selectbox("Select a table to view:", options=viewable_tables, key="view_table_select")

            if selected_table_to_view:
                st.write(f"Displaying records for table: **{selected_table_to_view}**")
                df = get_table_data(mc, selected_table_to_view) # Pass cursor
                if not df.empty:
                    st.dataframe(df)
                else:
                    st.info(f"No data found in {selected_table_to_view} or table is empty.")

        elif st.session_state.current_view == "Insert Records":
            st.subheader("Insert New Record")
            insertable_tables = ['beverages', 'cakes', 'cookies', 'employee', 'menu', 'pastries', 'personal_details', 'admin']
            selected_table_to_insert = st.selectbox("Select a table to insert into:", options=insertable_tables, key="insert_table_select")

            if selected_table_to_insert:
                st.write(f"Inserting into: **{selected_table_to_insert}**")
                try:
                    mc.execute(f"DESCRIBE {selected_table_to_insert};") # Use passed mc
                    schema = mc.fetchall()
                    
                    with st.form(f"insert_form_{selected_table_to_insert}"):
                        new_record_data = {}
                        for col_name, col_type, _, _, _, _ in schema:
                            # Basic type handling for input fields
                            if "int" in col_type:
                                new_record_data[col_name] = st.number_input(f"{col_name} ({col_type})", step=1, value=0)
                            elif "float" in col_type or "double" in col_type or "decimal" in col_type:
                                new_record_data[col_name] = st.number_input(f"{col_name} ({col_type})", value=0.0)
                            elif "date" in col_type :
                                 new_record_data[col_name] = str(st.date_input(f"{col_name} ({col_type})"))
                            elif "time" in col_type or "datetime" in col_type or "timestamp" in col_type:
                                 new_record_data[col_name] = str(st.time_input(f"{col_name} ({col_type})"))
                            else: # Default to text input for varchar, text, etc.
                                new_record_data[col_name] = st.text_input(f"{col_name} ({col_type})")
                        
                        submit_insert = st.form_submit_button("Insert Record")

                        if submit_insert:
                            cols = ', '.join(new_record_data.keys())
                            placeholders = ', '.join(['%s'] * len(new_record_data))
                            sql = f"INSERT INTO {selected_table_to_insert} ({cols}) VALUES ({placeholders})"
                            
                            values = []
                            for col_name, _, _, _, _, _ in schema: # Iterate in schema order
                                value = new_record_data[col_name]
                                # Attempt to convert to int if original type was int and value is string from text_input
                                # This is a basic heuristic; more robust type checking might be needed
                                if "int" in schema[[s[0] for s in schema].index(col_name)][1] and isinstance(value, str):
                                    try:
                                        values.append(int(value))
                                    except ValueError:
                                        values.append(value) # Keep as string if conversion fails, DB might handle or error
                                else:
                                     values.append(value)
                            
                            try:
                                mc.execute(sql, tuple(values)) # Use passed mc
                                m.commit() # Use passed m for commit
                                st.success(f"Record inserted successfully into {selected_table_to_insert}!")
                            except ms.Error as err:
                                st.error(f"Database error on insert: {err}")
                            except Exception as e:
                                st.error(f"An unexpected error occurred during insert: {e}")
                except ms.Error as err:
                    st.error(f"Error fetching schema for {selected_table_to_insert}: {err}")

        elif st.session_state.current_view == "Update Records":
            st.subheader("Update Existing Record")
            updatable_tables = ['admin', 'beverages', 'cakes', 'cookies', 'employee', 'pastries', 'personal_details']
            selected_table_to_update = st.selectbox("Select a table to update:", options=updatable_tables, key="update_table_select")

            if selected_table_to_update:
                st.write(f"Updating records in: **{selected_table_to_update}**")
                df = get_table_data(mc, selected_table_to_update) # Pass cursor
                if not df.empty:
                    st.dataframe(df)
                else:
                    st.info(f"No data found in {selected_table_to_update} or table is empty.")
                    # Optionally, prevent update form if table is empty, though not strictly necessary
                
                try:
                    mc.execute(f"DESCRIBE {selected_table_to_update};") # Use passed mc
                    schema = mc.fetchall()
                    column_names = [col[0] for col in schema]
                    
                    with st.form(f"update_form_{selected_table_to_update}"):
                        record_id_to_update = st.text_input("Enter ID of the record to update:")
                        column_to_update = st.selectbox("Select column to update:", options=column_names, key="update_column_select")
                        new_value = st.text_input(f"Enter new value for {column_to_update}:")
                        
                        submit_update = st.form_submit_button("Update Record")

                        if submit_update:
                            if not record_id_to_update or not column_to_update:
                                st.warning("Please provide Record ID and select a column to update.")
                            else:
                                # Assuming 'ID' or 'id' is the primary key column name.
                                # This might need to be more robust if PK names vary wildly and aren't consistently 'ID' or 'id'.
                                # For most tables here, it's 'ID'. For 'admin', it's 'id'.
                                pk_column = 'id' if selected_table_to_update == 'admin' else 'ID'

                                sql = f"UPDATE {selected_table_to_update} SET {column_to_update} = %s WHERE {pk_column} = %s"
                                try:
                                    # Attempt to convert new_value to the correct type based on schema (simplified)
                                    target_col_type = ""
                                    for col_name, col_type, _, _, _, _ in schema:
                                        if col_name == column_to_update:
                                            target_col_type = col_type
                                            break
                                    
                                    actual_value = new_value
                                    if "int" in target_col_type:
                                        actual_value = int(new_value)
                                    elif "float" in target_col_type or "double" in target_col_type or "decimal" in target_col_type:
                                        actual_value = float(new_value)
                                    # Dates and times would need specific parsing from string if not using st.date/time_input
                                    
                                    mc.execute(sql, (actual_value, record_id_to_update)) # Use passed mc
                                    m.commit() # Use passed m for commit
                                    if mc.rowcount > 0:
                                        st.success(f"Record {record_id_to_update} in {selected_table_to_update} updated successfully!")
                                        # Refresh data view
                                        st.experimental_rerun()
                                    else:
                                        st.warning(f"No record found with ID {record_id_to_update} in {selected_table_to_update}, or value was the same.")
                                except ms.Error as err:
                                    st.error(f"Database error on update: {err}")
                                except ValueError:
                                    st.error(f"Invalid value format for column {column_to_update}. Expected type: {target_col_type}")
                                except Exception as e:
                                    st.error(f"An unexpected error occurred during update: {e}")
                except ms.Error as err:
                    st.error(f"Error fetching schema for {selected_table_to_update}: {err}")

        elif st.session_state.current_view == "Delete Records":
            st.subheader("Delete Record from Table")
            deletable_tables = ['beverages', 'cakes', 'cookies', 'employee', 'pastries', 'personal_details'] # Excludes admin, menu, c_details
            
            if 'record_to_delete_id' not in st.session_state:
                st.session_state.record_to_delete_id = None
            if 'table_to_delete_from' not in st.session_state:
                st.session_state.table_to_delete_from = None

            selected_table_to_delete = st.selectbox("Select a table to delete from:", options=deletable_tables, key="delete_table_select")

            if selected_table_to_delete:
                st.write(f"Deleting records from: **{selected_table_to_delete}**")
                df = get_table_data(mc, selected_table_to_delete) # Pass cursor
                if not df.empty:
                    st.dataframe(df)
                else:
                    st.info(f"No data found in {selected_table_to_delete} or table is empty.")
                
                if st.session_state.record_to_delete_id is None:
                    with st.form(f"delete_form_{selected_table_to_delete}"):
                        record_id_to_delete = st.text_input("Enter ID of the record to delete:")
                        submit_select_record_for_deletion = st.form_submit_button("Select Record for Deletion")

                        if submit_select_record_for_deletion:
                            if not record_id_to_delete:
                                st.warning("Please enter the ID of the record to delete.")
                            else:
                                st.session_state.record_to_delete_id = record_id_to_delete
                                st.session_state.table_to_delete_from = selected_table_to_delete
                                st.experimental_rerun() # Rerun to show confirmation
                
                if st.session_state.record_to_delete_id and st.session_state.table_to_delete_from == selected_table_to_delete:
                    st.warning(f"Are you sure you want to delete record with ID '{st.session_state.record_to_delete_id}' from table '{selected_table_to_delete}'?")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Confirm Deletion"):
                            try:
                                # Assuming 'ID' is the primary key for these tables.
                                pk_column = 'ID' 
                                sql = f"DELETE FROM {selected_table_to_delete} WHERE {pk_column} = %s"
                                mc.execute(sql, (st.session_state.record_to_delete_id,)) # Use passed mc
                                m.commit() # Use passed m for commit

                                if mc.rowcount > 0:
                                    st.success(f"Record '{st.session_state.record_to_delete_id}' deleted successfully from {selected_table_to_delete}!")
                                else:
                                    st.warning(f"No record found with ID '{st.session_state.record_to_delete_id}' in {selected_table_to_delete}.")
                                
                                # Reset state and rerun
                                st.session_state.record_to_delete_id = None
                                st.session_state.table_to_delete_from = None
                                st.experimental_rerun()
                            except ms.Error as err:
                                st.error(f"Database error on delete: {err}")
                                st.session_state.record_to_delete_id = None # Reset on error too
                                st.session_state.table_to_delete_from = None
                                st.experimental_rerun()
                            except Exception as e:
                                st.error(f"An unexpected error occurred during delete: {e}")
                                st.session_state.record_to_delete_id = None
                                st.session_state.table_to_delete_from = None
                                st.experimental_rerun()
                    with col2:
                        if st.button("Cancel"):
                            st.session_state.record_to_delete_id = None
                            st.session_state.table_to_delete_from = None
                            st.experimental_rerun()

    elif st.session_state.current_view != 'login': # If not logged in and not in login view, redirect to login
        st.session_state.current_view = 'login'
        st.experimental_rerun()

# Note: The printX functions (printemployee, printadmin etc.) from the original file 
# are not directly used here yet. They will be replaced or adapted for Streamlit display
# in the subsequent steps (e.g., inside View Records, or by using get_table_data).
# The functions like viewrecords, deleterecords, updaterecords, insertrecords from the original app()
# will be rebuilt using Streamlit components in their respective sections.