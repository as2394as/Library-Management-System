'''
In this module are present all the functions
related to database operations
'''
import os
import sqlite3
import pandas as pd
import numpy as np
from datetime import date
import subprocess  as sp
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pickle

class DbAccess:
    '''
    this class creatsand maintains the connections
    with the database and provide data access layer
    '''

    def __init__(self):
        file = "Library.db"
        self.conn = self.createConnection(file)
        
    def createConnection(self,db):
        """ create database connection
        """
        
        self.conn = None
        try:
            self.conn = sqlite3.connect(db)
        except Error as e:
            print("Error in creating connection: "+e)
        return self.conn
        
    def run_sql(self,s):
    
        cursor = self.conn.execute(s)
        self.conn.commit()
        return cursor
        
    def createTables(self,conn):
        cur = conn.cursor()
        book_info="CREATE TABLE if not exists book_info"\
        "(book_title_id integer,"\
        "title text,"\
        "genre text,"\
        "author text,"\
        "purchase_price integer,"\
        "purchase_date text"\
        ");"

        unique_books="CREATE TABLE if not exists unique_book_titles"\
        "(id integer,"\
        "book_title_id integer,"\
        ");"
        cur.execute(book_info)
        rows = cur.fetchall()
        
    def getPerformanceData(self):
        history = pd.read_sql("select h.book_id 'book_id', t.title,t.genre,\
        t.author, '','','' from \
        loan_reservation_history h left join book_info as b on b.book_id=h.book_id left \
        join unique_book_titles as t on t.book_title_id =b.book_title_id" , con=self.conn)
        return history
        
    def getBudgetData(self):
        history = pd.read_sql("select b.book_id,t.title,t.genre, t.author,t.purchase_price from\
        loan_reservation_history as h left join book_info as b on b.book_id=h.book_id left\
        join unique_book_titles as t on t.book_title_id =b.book_title_id" , con=self.conn)
        return history
    
    def get_image(self,image_id):
        image = pd.read_sql("select photo from book_image where book_title_id="+str(image_id)+";",con=self.conn)
        return image
        
    def get_image_id(self,book_name):
        return pd.read_sql("select book_title_id from unique_book_titles where title='"+book_name+"';",con=self.conn)
    
    def create_image_db(self,books_file):

        sqlite_insert_blob_query = """ INSERT INTO book_image(book_title_id, photo) VALUES (?, ?)"""
        sqliteConnection = self.conn
        cwd="C:\\books"
        cursor = sqliteConnection.cursor()
        books = pd.read_csv(books_file)
        i=0
        print(len(books)-1)
        for filename in os.listdir(cwd):
            if(i<len(books)-1):
                img = mpimg.imread(cwd+"\\"+filename)
                empPhoto=pickle.dumps(img)
                data_tuple = (filename[:5], empPhoto)
                cursor.execute(sqlite_insert_blob_query, data_tuple)
                sqliteConnection.commit()
            else:
                break
            i=i+1

    def insertData(self,file,history,conn):
        books = pd.read_csv(file)
        history=pd.read_csv(history)


        book_counts = books.groupby(["title","author"])["id"].count()
        count = pd.DataFrame(book_counts)
        count.rename(columns={"title":"title","id":"count"},inplace=True)
        
        books = books.merge(count,on="title")
        
        
        
        
        books.drop_duplicates(subset=["title"],inplace=True)
        books["book_title_id"] =range(1001,1001+len(books))
        unique_books = books[["book_title_id","title","genre","author","purchase_date","purchase_price"]]
        all_books = books[["id","book_title_id"]]
        all_books.reset_index(drop=True,inplace=True)
        all_books.to_sql('book_info', con=conn, if_exists='replace')
        
        unique_books.reset_index(drop=True,inplace=True)
        unique_books.to_sql('unique_book_titles', con=conn, if_exists='replace')

        history.reset_index(drop=True,inplace=True)
        count_his=range(1001,1001+len(history))
        history["history_id"]=count_his
        history["reason"]="-"

        history1 = history[["history_id","book_id","member_id","reason"]]

        status = history.drop_duplicates(subset=["book_id"],inplace=True,keep='last')


        status = history.iloc[:,:]
        status["history_id"]=history["history_id"]
        status["reserved_id"]=np.nan
        
        history1.to_sql('loan_reservation_history', con=conn, if_exists='replace')
        status.to_sql('status',con=conn,if_exists = 'replace')
        conn.commit()

    def initialiseDb(self):
        bookFileName = "Book_Info.txt"
        histotyFileName = "Loan_reservation_History.txt"
        c = self.conn.cursor()
        self.createTables(self.conn)
        self.insertData(bookFileName,histotyFileName,self.conn)

        c.executescript('''
        PRAGMA foreign_keys=off;
        BEGIN TRANSACTION;

        
        ALTER TABLE unique_book_titles RENAME TO UB1;
        CREATE TABLE unique_book_titles
        (
        book_title_id integer PRIMARY KEY,
        title text,
        genre text,
        author text,
        purchase_price integer,
        purchase_date text
        );
        INSERT INTO unique_book_titles SELECT book_title_id,title,genre,author,purchase_price,purchase_date FROM UB1;

        ALTER TABLE book_info RENAME to UB;
        CREATE TABLE book_info (
        book_id,
        book_title_id,
        PRIMARY KEY(book_id),
        FOREIGN KEY(book_title_id) REFERENCES unique_book_titles(book_title_id));
        INSERT INTO book_info SELECT id,book_title_id from UB;


        ALTER TABLE loan_reservation_history RENAME to HIS2;
        CREATE TABLE loan_reservation_history (
        history_id integer PRIMARY KEY AUTOINCREMENT,
        book_id integer,
        member_id integer,
        reason text,
        date_time text,
        FOREIGN KEY(book_id) REFERENCES book_info(book_id));
        INSERT INTO loan_reservation_history SELECT history_id,book_id,member_id,reason,DATE('now') from HIS2;


        ALTER TABLE status RENAME to HIS1;
        CREATE TABLE status (
        history_id integer PRIMARY KEY,
        book_id integer,
        member_id integer,
        reserved_id integer,
        reservation_date text,
        checkout_date text,
        return_date text,
        FOREIGN KEY(history_id) REFERENCES loan_reservation_history(history_id),
        FOREIGN KEY(book_id) REFERENCES book_info(book_id));
        INSERT INTO status SELECT history_id,book_id,member_id,reserved_id,reservation_date,checkout_date,return_date from HIS1;
        
        

        DROP TABLE HIS1;
        DROP TABLE HIS2;
        DROP TABLE UB1;
        DROP TABLE UB;
        COMMIT;

        PRAGMA foreign_keys=on;
        ''')
        
        #self.create_image_db(bookFileName)

        
def main():
    Db = DbAccess()
    #Db.initialiseDb()
    
    test_cases1 = '''############################
######## TEST CASE 1 ########
############################'''
    print(test_cases1)
    #initialiseDb()
    Db.initialiseDb()
    print("initialiseDb() test case")
    print("TEST CASE 1 PASSED")
    print()
    print()
    
    test_cases2 = '''############################
######## TEST CASE 2 ########
############################'''
    print(test_cases2)
    #get_image_id()
    print(len(Db.get_image_id('Matilda')))
    print("get_image_id() test case")
    print("TEST CASE 2 PASSED")
    print()
    print()
    
    test_cases3 = '''############################
######## TEST CASE 3 ########
############################'''
    print(test_cases3)
    #get_image()
    print(len(Db.get_image('1001')))
    print("get_image() test case")
    print("TEST CASE 3 PASSED")
    print()
    print()
    
    test_cases4 = '''############################
######## TEST CASE 4 ########
############################'''
    print(test_cases4)
    #getPerformanceData()
    print(len(Db.getPerformanceData()))
    print("getPerformanceData() test case")
    print("TEST CASE 4 PASSED")
    print()
    print()
    
if __name__ == '__main__':
    main()
