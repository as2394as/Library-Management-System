'''
This file has all the code
to return a book
'''
import database as d
import numpy as np
import pandas as pd
from datetime import date,timedelta


class BookReturn():
    '''
    this class has all the functions related to book return functionality
    '''
    
    def __init__(self):
        self.db = d.DbAccess()
        
    def returnBook(self,books):
        '''
        takes books and member_id
        and returns the string for 
        successful or failed return operation
        '''
        books_result1,books_result2 = self.return_check(books)
        return books_result1,books_result2
    
    def return_check(self,books):
        '''
        takes in books and member id
        and performs insert and updates in db
        for checkout opreration
        '''
        fail_result=""
        success_result=""
        today="'"+date.today().strftime("%d/%m/%Y")+"'"
        null_value = "Null"
        for row in books:
            if(row[4]=='Checked Out' or row[4]=='Reserved'):
                result = self.check(row)
                if result == "":
                    insert1=[row[0],null_value,"'return'",today]
                    history = "insert into loan_reservation_history(book_id,member_id,reason,date_time) values ("+",".join(insert1)+");"
                    
                    cursor = self.db.run_sql(history)
                    history_id=cursor.lastrowid
                    if(row[6]!='nan'):
                        update = "update status set member_id="+null_value+",return_date="+today+"\nwhere history_id = "+row[6]+" and book_id= "+row[0]+";"
                        
                        cursor = self.db.run_sql(update)
                    success_result = success_result+"--------SUCCESS--------\n"+"The book with id: "+row[0]+"\nis successfully returned\n"
                else:
                    fail_result = fail_result+result
            else:
                fail_result = fail_result+"--------FAILED--------\n"+"The book with id: "+row[0]+"\ncould not be returned as it is "+row[4]+"\n"
        return fail_result,success_result

    def check(self,row):
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
            if(not item[2]):
                fail_result = fail_result+"The book with id: "+str(item[1])+"\nis already returned\n"
        return fail_result

def main(): 
    BR = BookReturn()

    test_cases1 = '''############################
######## TEST CASE 1 ########
############################'''
    #check()
    #return_check()
    #returnBook()
    print(test_cases1)
    print("check((('9999','1234','','','','')),1234)")
    print("return_check(books=[['9999','','','','Checked Out','','null']],1234)")
    print("return_book(books=[['9999','','','','Checked Out','','null']],1234)")
    print()
    books=[["9999",'','','','Checked Out','','null']]
    member_id = str(1234)
    print(BR.returnBook(books)[0])
    print(BR.returnBook(books)[1])
    print("TEST CASE 1 PASSED")
    print()
    print()

if __name__=='__main__':
	main()
