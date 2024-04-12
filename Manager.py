import streamlit as st
import creds 
import mysql.connector as ms
m=ms.connect(host=creds.host, user=creds.user, password=creds.password, database=creds.database) 
mc=m.cursor()


def printemployee():
    print('_'*50)
    print("Here is the employee table:")
    print('-'*50)
    print('ID \t','NAME \t\t','SALARY \t', 'DEPARTMENT')
    mc.execute("select * from employee;")
    employee=mc.fetchall()
    for i in employee:
        l=15-len(i[1])
        i1=i[1]+' '*l
        i2=str(i[2])+' '*8
        print (i[0],'\t',i1,i2,'\t',i[3])
    print('_'*50)
    print('\n')
def printadmin():
    print('_'*50)
    print("Here is the admin table:")
    print('-'*50)
    print('ID \t','PASSWORD')
    mc.execute("select * from admin;")
    admin=mc.fetchall()
    for i in admin:
        print(i[0],'\t',i[1])
    print('_'*50)
    print('\n')
def printmenu():
    print('_'*50)
    print("Here is the list of categories:")
    mc.execute("select * from menu;")
    menu=mc.fetchall()
    print('-'*50)
    print ('ID \t', 'NAME \t')
    for i in menu:
        print (i[0],'\t', i[1] )
        print('_'*50)
        print('\n')
def printpersonal():
    print('_'*55)
    print("Here are the personal details:")
    mc.execute("select * from personal_details;")
    p=mc.fetchall()
    print('-'*55)
    print ('ID \t', 'NAME \t\t', 'PHONE_NO \t', 'EMAIL_ID')
    for i in p:
        l=7-len(i[1])
        i1=i[1]+' '*l
        i2=str(i[2])+' '*8
        print (i[0],'\t', i1,'\t', i[2],'\t', i[3] )
    print('_'*55)
    print('\n')
#----------------------------------------------------------------------------------------------------------------------------

    

def app():
    st.title("Manager")
    def login():
        c=0
        while c==0:
            a=input("Enter the ID_")
            b=input("Enter the Password_")
            mc.execute("select * from admin where id ='"+a+"' and password = '"+b+"'");
            L = mc.fetchall()
            if len(L) == 0:
                print("No user record found, Please try again")
            else:
                c=1

    def viewrecords():
        print('_'*50)
        print("The tables that we have are:")
        print('-'*50)
        mc.execute("show tables")
        l1 = mc.fetchall()
        count = 0
        print ('ID \t TABLE NAME')
        for i in l1:
            if i[0] not in ('admin','c_details'):
                count+=1
                print(count ,'\t',i[0].capitalize())
        print('_'*50)
        print ("\n")
        table='?'
        while table not in ('beverages','cakes','cookies','employee','menu','pastries','personal_details'):
            table=(input("Enter the name of table you want to be displayed_").lower().strip())
        print("\n")
        if table == 'beverages':
            printbeverages()
        elif table == 'cakes' :
            printcakes()
        elif table == 'cookies':
            printcookies()
        elif table == 'employee':
            printemployee()
        elif table == 'menu':
            printmenu()
        elif table == 'pastries':
            printpastries()
        elif table == 'personal_details':
            printpersonal()

    def deleterecords():
        print('_'*50)
        print("The tables that we have are:")
        print('-'*50)
        mc.execute("show tables")
        l1 = mc.fetchall()
        count = 0
        print ('ID \t TABLE NAME')

        for i in l1:
            if i[0] not in ('admin','c_details','menu'):
                count+=1
                print(count ,'\t',i[0].capitalize())
        print('_'*50)
        print ("\n")
        table=' '
        while table not in ('beverages','cakes','cookies','pastries','employee','personal_details'):
            table=(input("Enter the table name whose record you want to delete_").lower().strip())
        if table=='beverages':
            printbeverages()
        if table=='cakes':
            printcakes()
        if table=='cookies':
            printcookies()
        if table=='pastries':
            printpastries()
        if table=='employee':
            printemployee()
        if table=='personal_details':
            printpersonal()
        n=(input("Enter the ID of the record you want to delete_").upper().strip())
        mc.execute("delete from "+table+" where ID='"+n+"'")
        m.commit()
        print("Record deleted")
        
    def updaterecords():
        print('_'*50)
        print("The tables that we have are:")
        print('-'*50)
        mc.execute("show tables")
        l1 = mc.fetchall()
        count = 0
        print ('ID \t TABLE NAME')
        for i in l1:
            if i[0] not in ('c_details','menu'):
                count+=1
                print(count ,'\t',i[0].capitalize())
        print('_'*50)
        print ("\n")
        table=' '
        while table not in ('admin','beverages','cakes','cookies','employee','pastries','personal_details'):
            table=(input("Enter the table name whose data you want to update_").strip().lower())
        if table=='beverages':
            printbeverages()
        if table=='cakes':
            printcakes()
        if table=='cookies':
            printcookies()
        if table=='pastries':
            printpastries()
        if table=='employee':
            printemployee()
        if table=='admin':
            printadmin()
        if table=='personal_details':
            printpersonal()
        n=(input("ID of the record you want to edit_").upper().strip())
        field=(input("Field to be updated_").lower().strip())
        entry=input("New entry_")
        mc.execute("Update "+table+" set "+field+" = '"+entry+"' where id ='"+n+"'")
        m.commit()
        print("The field has been updated")
        
    def insertrecords():
        print('_'*50)
        print("The tables that we have are:")
        print('-'*50)
        mc.execute("show tables")
        l1 = mc.fetchall()
        count = 0
        print ('ID \t TABLE NAME')
        for i in l1:
            if i[0] not in ('c_details'):
                count+=1
                print(count ,'\t',i[0].capitalize())
        print('_'*50)
        print ("\n")
        table=' '
        while table not in ('beverages','cakes','cookies','pastries','employee','personal_details','admin','menu'):
            table=(input("Enter the table name into which you want to enter new record_").strip().lower())
        if table=='beverages':
            printbeverages()
        elif table=='cakes':
            printcakes()
        elif table=='cookies':
            printcookies()
        elif table=='pastries':
            printpastries()
        elif table=='employee':
            printemployee()
        elif table=='admin':
            printadmin()
        elif table=='personal_details':
            printpersonal()
        elif table=='menu':
            printmenu()
        mc.execute("desc "+table+" ")
        desc=mc.fetchall()
        field=[]
        value=()
        s=[]
        for i in desc:
            field.append(i[0])
        for i in desc:
            print("Column",i[0])
            v=input("Enter value_")
            if v.isnumeric():
                v=int(v)
            else:
                v=v.capitalize().strip()
            value+=(v,)
            s.append('%s')
        fields='('+','.join(field)+')'
        s2='('+','.join(s)+')'
        sql= "INSERT INTO "+table+" "+fields+" values "+s2+" "
        mc.execute(sql,value)
        m.commit()
        print("Your record has been added")
    login()
    cont='yes'
    while cont.lower() in ('yes','y'):
        print("""\nYou can choose from the below operation which you want to execute:
1 View Records
2 Delete Records
3 Update Records
4 Insert Records
5 Exit""")
        
        choice=9
        while choice not in (1,2,3,4,5):
            choice = int(input("Enter your choice number_"))
        if choice == 1:
            viewrecords()
        elif choice == 2:
            deleterecords()
        elif choice == 3:
            updaterecords()
        elif choice == 4:
            insertrecords()
        elif choice == 5:
            cont='no'
        if choice!=5:
            c=' '
            while c not in ('yes','y','no','n') :
                c=(input("Do you want to continue? (yes/no)_").strip().lower())
                cont=c
    print('''
                | ✿✿✿══✿✿══✿✿══✿✿✿  |
                | ═══════════(\/)══════════ |
                | ══════════(◕.◕)══════════ |
                | ══════════() ()══════════ |
                |  / \ / \ / \ / \ / \ / \  |
                | ( L | O | G | G | E | D | |
                |  \_/ \_/ \_/ \_/ \_/ \_/  |
                |         _   _   _         |
                |        / \ / \ / \        |
                |       ( O | U | T |       |
                |        \_/ \_/ \_/        |''')
#----------------------------------------------------------------------------------------------------------------------------