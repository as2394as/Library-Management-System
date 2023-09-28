'''
This file has all the code
to checkout/reserve a book
'''
import database as d
import numpy as np
import pandas as pd
from datetime import date


class BookCheckout():
    '''
    this class has all the functions related to book checkout functionality
    '''

    def __init__(self):
        self.db = d.DbAccess()

    def checkout(self,books,member_id):
        '''
        takes books and member_id
        and returns the string for 
        successful or failed checkout operation
        '''
        failedMsg,successfulMsg = self.checkout_check(books,member_id)
        return failedMsg,successfulMsg
        
    def reserveBook(self,books,member_id): 
        '''
        takes books and member_id
        and returns the string for 
        successful or failed reservation operation
        '''
        failedMsg,successfulMsg = self.reserve_check(books,member_id)
        return failedMsg,successfulMsg
    
    def reserve_check(self,books,member_id):
        '''
        takes in books and member id
        and performs insert and updates in db
        for reserve opreration
        '''
        success_result = ""
        fail_result = ""
        today="'"+date.today().strftime("%d/%m/%Y")+"'"
        for row in books:
            if(row[4]=='Checked Out'):
                result = self.check(row,member_id)
                if result=="":
                    insert1=[row[0],member_id,"'reserved'",today]
                    history = "insert into loan_reservation_history(book_id,member_id,reason,date_time) values ("+",".join(insert1)+");"
                    cursor = self.db.run_sql(history)
                    history_id=cursor.lastrowid
                    
                    update = "update status set reservation_date = "+today+",reserved_id="+member_id+" where history_id = "+row[6]+" and book_id= "+row[0]+";"
                    
                    cursor = self.db.run_sql(update)
                    success_result = success_result+"--------SUCCESS--------\n"+"The book with id:"+row[0]+"\nis successfully reserved\n----------------------------\n"
                else:
                    fail_result=fail_result+"--------FAILED--------\n"+result.format(row[4])
            else:
                fail_result = fail_result+"--------FAILED--------\n"+"The book with id:"+row[0]+"\ncould not be reserved as it is "+row[4]+"\n----------------------------\n"
        return fail_result,success_result
    
    def check(self,row,member_id):
        '''
        takes row of the selected books table and member_id
        and returns the string based on if the book in the
        row is assigned to the member
        '''
        fail_result = ""
        query = "select * from status where book_id="+row[0]+";"
        cursor = self.db.run_sql(query)
        item = list(cursor.fetchall())
        if(len(item)>0):
            item=item[0]
            if(item[2]==int(member_id)):
                fail_result = fail_result+"The book with id: "+str(item[1])+"\nis already {0} with member: "+member_id+"\n"
        return fail_result
        
    def check_r(self,row,member_id):
        '''
        takes row of the selected books table and member_id
        and returns the string based on if the book in the
        row is assigned to the member
        '''
        fail_result = ""
        query = "select * from status where book_id="+row[0]+";"
        cursor = self.db.run_sql(query)
        item = list(cursor.fetchall())
        if(len(item)>0):
            item=item[0]
            print("############",item[2])
            if(item[3]!=int(member_id)):
                fail_result = fail_result+"The book with id: "+str(item[1])+"\nis already {0} with member: "+str(item[3])+"\n"
            elif(item[2]!=None):
                fail_result = fail_result+"The book with id: "+str(item[1])+"\nis not returned yet"
        return fail_result
            
    def checkout_check(self,books,member_id):
        '''
        takes in books and member id
        and performs insert and updates in db
        for checkout opreration
        '''
        success_result = ""
        fail_result = ""
        today="'"+date.today().strftime("%d/%m/%Y")+"'"
        for row in books:
            if(row[4]=='Available' or row[4]=='Reserved'):
                
                if(row[4]=='Reserved'):
                    result = self.check_r(row,member_id)
                    if(result == ""):
                        insert1=[row[0],member_id,"'checkout'",today]
                        history = "insert into loan_reservation_history(book_id,member_id,reason,date_time) values ("+",".join(insert1)+");"
                        cursor = self.db.run_sql(history)
                        history_id=cursor.lastrowid
                        
                        if(row[6]!='nan'):
                            update = "update status set checkout_date = "+today+",member_id="+member_id+",reserved_id=null,return_date=null,reservation_date=null where history_id = "+row[6]+" and book_id= "+row[0]+";"
                            
                            cursor = self.db.run_sql(update)
                        else:
                            insert2=[str(history_id),row[0],member_id,"null",today,"null"]
                            insert = "insert into status(history_id,book_id,member_id,reservation_date,checkout_date,return_date) values("+",".join(insert2)+");"
                            cursor = self.db.run_sql(insert)
                        success_result = success_result+"--------SUCCESS--------\n"+"The book with id:"+row[0]+"\nis successfully checked out\n----------------------------\n"
                    else:
                        fail_result=fail_result+"--------FAILED--------\n"+result.format(row[4])
                elif(row[4]=='Available'):
                    insert1=[row[0],member_id,"'checkout'",today]
                    history = "insert into loan_reservation_history(book_id,member_id,reason,date_time) values ("+",".join(insert1)+");"
                    cursor = self.db.run_sql(history)
                    history_id=cursor.lastrowid
                    
                    if(row[6]!='nan'):
                        update = "update status set checkout_date = "+today+",member_id="+member_id+",return_date=null,reservation_date=null where history_id = "+row[6]+" and book_id= "+row[0]+";"
                        
                        cursor = self.db.run_sql(update)
                    else:
                        insert2=[str(history_id),row[0],member_id,"null",today,"null"]
                        insert = "insert into status(history_id,book_id,member_id,reservation_date,checkout_date,return_date) values("+",".join(insert2)+");"
                        cursor = self.db.run_sql(insert)
                    success_result = success_result+"--------SUCCESS--------\n"+"The book with id:"+row[0]+"\nis successfully checked out\n----------------------------\n"
            else:
                fail_result = fail_result+"--------FAILED--------\n"+"The book with id:"+row[0]+"\ncould not be booked as it is "+row[4]+"\n----------------------------\n"
        return fail_result,success_result


def main(): 
    BC = BookCheckout()

    test_cases1 = '''############################
######## TEST CASE 1 #######
############################'''

    #checkout_check()
    #checkout()
    print(test_cases1)
    print("checkout_check(books=[['9999','','','','Checked Out','','null']],1234)")
    print("checkout(books=[['9999','','','','Checked Out','','null']],1234)")
    print()
    books=[["9999",'','','','Checked Out','','null']]
    member_id = str(1234)
    print(BC.checkout(books,member_id))
    print("TEST CASE 1 PASSED")
    print()
    print()
    
    
    test_cases2 = '''############################
######## TEST CASE 2 #######
############################'''

    #reserve_check()
    #reserveBook()
    print(test_cases2)
    print("reserve_check(books=[['9999','','','','Checked Out','','null']],1234)")
    print("reserveBook(books=[['9999','','','','Checked Out','','null']],1234)")
    print()
    books=[["9999",'','','','Reserved','','null']]
    member_id = str(1234)
    print(BC.reserveBook(books,member_id))
    print("TEST CASE 2 PASSED")
    print()
    print()
    
    
    


if __name__=='__main__':
	main()
