import streamlit as st
import mysql.connector as ms
import creds 

m=ms.connect(host=creds.host, user=creds.user, password=creds.password, database=creds.database) 
mc=m.cursor()


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

    
def app():
    st.title("Customer")
    sure='NO'
    while sure in ('NO','N'):
        st.write('\n')
        st.write("Enter your personal details")
        name=(st.text_input("Name").lower().strip())
        phone_no=st.text_input("Phone number")
        int(phone_no)
        option='?'
        while option not in ('YES','NO','Y','N'):
            option=(st.text_input("Do you want the order you place to be home delivered (Yes/No)").strip().upper())
        if option in ('YES','Y'):
            address=st.text_input("Address_")
        else:
            address= '-'
        st.write('_'*50)
        st.write ('\nYour personal details are:')
        st.write('Name-',name,'\nAddress-',address,'\nPhone Number-',phone_no,)
        st.write('_'*50)
        sure='?'
        while sure not in ('YES','NO','Y','N'):
            sure=(st.text_input("\nConfirm the personal details? (Yes/No)_").strip().upper())
    st.write("Your information has been stored\n")
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
            st.writemenu()
            category='?'
            while category not in ('C00','B00','K00','P00'):
                category=(st.text_input("Enter the id of the category whose menu you would like to view_").upper().strip())

            if category=='C00':
                st.writecakes()
                mc.execute("select * from cakes;")
                cakes=mc.fetchall()
                while ID not in ('C01','C02','C03','C04','C05','C06','C07','C08','C09','C10'):
                    ID=(st.text_input("Enter the id of the cake you wish to order_").strip().upper())
                for i in cakes:
                    if i[0]==ID:
                        price=i[2]
                        s=i[1]
                while weight not in (0.25,0.5,1.0,2.0,1,2):
                    weight=float(st.text_input("Enter the weight of cake to be ordered (0.25/0.5/1.0/2.0)_"))
                s+=' cake '+str(weight)+' kg'
                order[s]=weight/0.5*price
                
            elif category=='B00':
                st.writebeverages()
                mc.execute("select * from beverages;")
                beverages=mc.fetchall()
                while ID not in ('B01','B02','B03','B04','B05','B06','B07','B08','B09','B10'):
                    ID=(st.text_input("Enter the id of the beverage you wish to order_").strip().upper())
                for i in beverages:
                    if i[0]==ID:
                        price=i[2]
                        s=i[1]
                while size not in ('SMALL','MEDIUM','LARGE'):
                    size=(st.text_input("Enter the size of beverage to be ordered (Small/Medium/Large)_").strip().upper())
                    if size=='SMALL':
                        l=0.75
                    elif size=='MEDIUM':
                        l=1
                    elif size=='LARGE':
                        l=1.5
                quantity=int(st.text_input("Enter no of drinks you want to order_"))
                l=l*quantity
                s+=' '+ size.lower()+ ' (X'+str(quantity)+')'
                order[s]=price*l
                
            elif category=='K00':
                st.writecookies()
                mc.execute("select * from cookies;")
                cookies=mc.fetchall()
                while ID not in ('K01','K02','K03','K04','K05','K06','K07','K08','K09','K10'):
                    ID=(st.text_input("Enter the id of the cookies you wish to order_").strip().upper())
                for i in cookies:
                    if i[0]==ID:
                        price=i[2]
                        s=i[1]

                while weight not in (150,250,500):
                    weight=int(st.text_input("Enter the weight of cookies to be ordered (150/250/500)_"))
                quantity=int(st.text_input("Number of boxes you want to order_"))
                l=weight*quantity
                s+=' cookies '+str(weight)+' g'+' (X'+str(quantity)+')'
                order[s]=price/500*l
                
            elif category=='P00':
                st.writepastries()
                mc.execute("select * from pastries;")
                pastries=mc.fetchall()
                while ID not in ('P01','P02','P03','P04','P05','P06','P07','P08','P09','P10'):
                    ID=(st.text_input("Enter the id of the pastries you wish to order_").strip().upper())
                for i in pastries:
                    if i[0]==ID:
                        price=i[2]
                        s=i[1]
                quantity=int(st.text_input("Number of pieces you want to order_"))
                s+=' pastry '+'(X'+str(quantity)+')'
                order[s]=price*quantity
                
            choice=(st.text_input("\nDo you want to add on to your order?(Yes/No)_").strip().upper())

        for i in order:
            amount+=order[i]
        taxes=amount*18/100
        order['GST']=taxes
        amount+=taxes
        if amount>500 and address!='-':
            delivery='?'
            while delivery not in ('YES','NO','Y','N'):
                delivery=(st.text_input("Do you want the order to be home delivered? (Yes/No)_").strip().upper())
            if delivery in ('YES','Y'):
                order['Delivery']=50
        elif amount<500 and address!='-':
            st.write('Delivery not available for orders below 500')
        st.write('_'*50)
        st.write("Here is your bill:")
        import datetime
        d=str(datetime.datetime.now())
        date=str(d[:-7])
        st.write(name,' '*20,date)
        st.write('_'*50)
        st.write('NAME',' '*36, 'PRICE')
        for i in order:
            l=42-len(i)
            i1=i+' '*l
            st.write (i1 , float(order[i]))
        st.write('-'*50)
        st.write('Total amount',' '*29,amount)
        st.write(' '*40,'=',round(amount))
        st.write('_'*50)
        
        confirm='?'
        while confirm not in ('YES','NO','EXIT','Y','N'):
            confirm=(st.text_input("\nPlace order? (Yes/No/Exit)_").strip().upper())
            
    if confirm in ('YES','Y'):
        st.write("Your order has been placed!\n\n")

        st.write("""
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
        st.write('You have successfully logged out')