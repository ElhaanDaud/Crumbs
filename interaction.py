import mysql.connector as ms
m=ms.connect(host="localhost", user='root', password='&Bushra.S.583', database='Crumbs')
mc=m.cursor()
print("""
         ▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄
         █▒▒░░░░░░░░░▒▒█
          █░░█░░░░░█░░█
       ▄▄  █░░░▀█▀░░░█  ▄▄
      █░░█ ▀▄░░░░░░░▄▀ █░░█
      █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
      █  ╦ ╦╔╗╦ ╔╗╔╗╔╦╗╔╗  █
      █  ║║║╠ ║ ║ ║║║║║╠   █
      █  ╚╩╝╚╝╚╝╚╝╚╝╩ ╩╚╝  █
      █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
EXPERIENCE THE BEST OF BAKING WITH CRUMBS!!
WE'LL BAKE YOUR DAY :)\n""")
#----------------------------------------------------------------------------------------------------------------------------
def printcakes():
    print('_'*50)
    print("Here is the menu for cakes:")
    print('-'*50)
    print('ID \t','NAME \t\t\t','PRICE_1kg \t')
    mc.execute("select * from cakes;")
    cakes=mc.fetchall()
    for i in cakes:
        l=26-len(i[1])
        i1=i[1]+' '*l
        print (i[0],'\t',i1,i[2])
    print('_'*50)
    print('\n')
def printbeverages():
    print('_'*50)
    print("Here is the menu for beverages:")
    print('-'*50)
    print('ID \t','NAME \t\t\t','PRICE_MEDIUM \t')
    mc.execute("select * from beverages;")
    beverages=mc.fetchall()
    for i in beverages:
        l=29-len(i[1])
        i1=i[1]+' '*l
        print (i[0],'\t',i1,i[2])
    print('_'*50)
    print('\n')
def printcookies():
    print('_'*50)
    print("Here is the menu for cookies:")
    print('-'*50)
    print('ID \t','NAME \t\t\t','PRICE_500g \t')
    mc.execute("select * from cookies;")
    cookies=mc.fetchall()
    for i in cookies:
        l=26-len(i[1])
        i1=i[1]+' '*l
        print (i[0],'\t',i1,i[2])
    print('_'*50)
    print('\n')
def printpastries():
    print('_'*50)
    print("Here is the menu for pastries:")
    print('-'*50)
    print('ID \t','NAME \t\t\t','PRICE_PERPIECE\t')
    mc.execute("select * from pastries;")
    pastries=mc.fetchall()
    for i in pastries:
        l=29-len(i[1])
        i1=i[1]+' '*l
        print (i[0],'\t',i1,i[2])
    print('_'*50)
    print('\n')
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
def customer():
    sure='NO'
    while sure in ('NO','N'):
        print('\n')
        print("Enter your personal details")
        name=(input("Name_").lower().strip())
        phone_no=int(input("Phone number_"))
        option='?'
        while option not in ('YES','NO','Y','N'):
            option=(input("Do you want the order you place to be home delivered (Yes/No)").strip().upper())
        if option in ('YES','Y'):
            address=input("Address_")
        else:
            address= '-'
        print('_'*50)
        print ('\nYour personal details are:')
        print('Name-',name,'\nAddress-',address,'\nPhone Number-',phone_no,)
        print('_'*50)
        sure='?'
        while sure not in ('YES','NO','Y','N'):
            sure=(input("\nConfirm the personal details? (Yes/No)_").strip().upper())
    print("Your information has been stored\n")
    confirm='NO'
    while confirm in ('NO','N'):
        choice='YES'
        order={}
        amount=0
        while choice in ('YES','Y'):
            ID='?'
            weight=0
            size='?'
            s=' '
            price=0
            printmenu()
            category='?'
            while category not in ('C00','B00','K00','P00'):
                category=(input("Enter the id of the category whose menu you would like to view_").upper().strip())

            if category=='C00':
                printcakes()
                mc.execute("select * from cakes;")
                cakes=mc.fetchall()
                while ID not in ('C01','C02','C03','C04','C05','C06','C07','C08','C09','C10'):
                    ID=(input("Enter the id of the cake you wish to order_").strip().upper())
                for i in cakes:
                    if i[0]==ID:
                        price=i[2]
                        s=i[1]
                while weight not in (0.25,0.5,1.0,2.0,1,2):
                    weight=float(input("Enter the weight of cake to be ordered (0.25/0.5/1.0/2.0)_"))
                s+=' cake '+str(weight)+' kg'
                order[s]=weight/0.5*price
                
            elif category=='B00':
                printbeverages()
                mc.execute("select * from beverages;")
                beverages=mc.fetchall()
                while ID not in ('B01','B02','B03','B04','B05','B06','B07','B08','B09','B10'):
                    ID=(input("Enter the id of the beverage you wish to order_").strip().upper())
                for i in beverages:
                    if i[0]==ID:
                        price=i[2]
                        s=i[1]
                while size not in ('SMALL','MEDIUM','LARGE'):
                    size=(input("Enter the size of beverage to be ordered (Small/Medium/Large)_").strip().upper())
                    if size=='SMALL':
                        l=0.75
                    elif size=='MEDIUM':
                        l=1
                    elif size=='LARGE':
                        l=1.5
                quantity=int(input("Enter no of drinks you want to order_"))
                l=l*quantity
                s+=' '+ size.lower()+ ' (X'+str(quantity)+')'
                order[s]=price*l
                
            elif category=='K00':
                printcookies()
                mc.execute("select * from cookies;")
                cookies=mc.fetchall()
                while ID not in ('K01','K02','K03','K04','K05','K06','K07','K08','K09','K10'):
                    ID=(input("Enter the id of the cookies you wish to order_").strip().upper())
                for i in cookies:
                    if i[0]==ID:
                        price=i[2]
                        s=i[1]

                while weight not in (150,250,500):
                    weight=int(input("Enter the weight of cookies to be ordered (150/250/500)_"))
                quantity=int(input("Number of boxes you want to order_"))
                l=weight*quantity
                s+=' cookies '+str(weight)+' g'+' (X'+str(quantity)+')'
                order[s]=price/500*l
                
            elif category=='P00':
                printpastries()
                mc.execute("select * from pastries;")
                pastries=mc.fetchall()
                while ID not in ('P01','P02','P03','P04','P05','P06','P07','P08','P09','P10'):
                    ID=(input("Enter the id of the pastries you wish to order_").strip().upper())
                for i in pastries:
                    if i[0]==ID:
                        price=i[2]
                        s=i[1]
                quantity=int(input("Number of pieces you want to order_"))
                s+=' pastry '+'(X'+str(quantity)+')'
                order[s]=price*quantity
                
            choice=(input("\nDo you want to add on to your order?(Yes/No)_").strip().upper())

        for i in order:
            amount+=order[i]
        taxes=amount*18/100
        order['GST']=taxes
        amount+=taxes
        if amount>500 and address!='-':
            delivery='?'
            while delivery not in ('YES','NO','Y','N'):
                delivery=(input("Do you want the order to be home delivered? (Yes/No)_").strip().upper())
            if delivery in ('YES','Y'):
                order['Delivery']=50
        elif amount<500 and address!='-':
            print('Delivery not available for orders below 500')
        print('_'*50)
        print("Here is your bill:")
        import datetime
        d=str(datetime.datetime.now())
        date=str(d[:-7])
        print(name,' '*20,date)
        print('_'*50)
        print('NAME',' '*36, 'PRICE')
        for i in order:
            l=42-len(i)
            i1=i+' '*l
            print (i1 , float(order[i]))
        print('-'*50)
        print('Total amount',' '*29,amount)
        print(' '*40,'=',round(amount))
        print('_'*50)
        
        confirm='?'
        while confirm not in ('YES','NO','EXIT','Y','N'):
            confirm=(input("\nPlace order? (Yes/No/Exit)_").strip().upper())
            
    if confirm in ('YES','Y'):
        print("Your order has been placed!\n\n")

        print("""
                                 )
                                ( )
                                 |
                                TTT
                                | |
                            _.--| |--._
                          .-'; ;`-'* ; ` *.
                         [ *  ;  *  ;  ;   ]
                         [_    ;   *    * _]
                          |'''---...---'''|
                          | | | | | | | | |
                          | | | | | | | | |
                           `---.|.|.|.---'
                    ✿✿✿════✿✿═════✿✿════✿✿✿
                    ════════════(\/)══════════════
                    ════════════(◕.◕)═════════════
                    ════════════() ()═════════════
                   / \ / \ / \ / \ / \   / \ / \ / \
                  ( T | H | A | N | K ) ( Y | O | U )
                   \_/ \_/ \_/ \_/ \_/   \_/ \_/ \_/
            _   _   _   _     _     _   _   _   _     _   _   _
           / \ / \ / \ / \   / \   / \ / \ / \ / \   / \ / \ / \
          ( H | A | V | E ) ( A ) ( N | I | C | E ) ( D | A | Y )
           \_/ \_/ \_/ \_/   \_/   \_/ \_/ \_/ \_/   \_/ \_/ \_/
           """)

        val=(name,address,phone_no,amount,date)
        sql= """INSERT INTO c_details (name,address,phone_no,amount,date_time)
                values(%s,%s,%s,%s,%s)"""
        mc.execute(sql,val)
        m.commit()
    else:
        print('You have successfully logged out')
#----------------------------------------------------------------------------------------------------------------------------
def manager():
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
tidbits=['Enjoy the best of baking with crumbs!','Every flavour has a story to tell!','Count the memories not the calories!','We bet you will keep coming back!','A wonderful gift for your loved ones!','Celebrate with crumbs!']
niceday=['Hope you have a good day :)','Stay hydrated :)','Just in case no one has told you already... you are amazing :)','Be a rainbow in someones storm :)','Perfection is accepting your imperfections :)']
import random
whichone=' '
while whichone not in ("customer","manager"):
    whichone=(input("Continue as a customer or the manager?_").strip().lower())
if whichone=='customer':
    print('\n')
    print(random.choice(tidbits))
    customer()
else:
    print('\n')
    print(random.choice(niceday))
    manager()
m.close()
