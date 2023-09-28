'''
This file has all the code
to search a book
'''
import database as d
import numpy as np
import pandas as pd
from datetime import *
from menu import *


class BookSearch():
    '''
    This class Has all the functions to search and return desired books
    '''

    def __init__(self):
        self.db = d.DbAccess()
        self.unique_book_titles = "select ubt.book_title_id,ubt.title,ubt.genre,ubt.author from unique_book_titles ubt"
        self.history_columns=['book_id', 'title', 'genre', 'author', 'reservation_date','checkout_data','return_date']
        self.suggested_books_columns = ['Title','Price','Count']
        self.book_info = "select bi.book_id,bi.book_title_id from book_info bi"
        self.status = "select s.history_id,s.book_id,s.member_id,s.reserved_id,s.reservation_date,s.checkout_date,s.return_date from status s"
        self.unique_book_titles_columns = ["book_title_id","title","genre","author","purchase_price","purchase_date"]
        self.book_info_columns = ["book_id","book_title_id"]
        self.status_columns = ["history_id","book_id","member_id","reserved_id","reservation_date","checkout_date","return_date"]
        self.book_search_return_columns = ["book_id","member_id","reserved_id","history_id","title","author","genre","reservation_date","checkout_date","return_date"]
        self.filter_books_columns = ['book_id','title','author','genre','check','member_id','history_id']
        self.book_id = "book_id"
        self.history_id = "history_id"
        self.checkout_date = "checkout_date"
        self.return_date = "return_date"
        self.reservation_date = "reservation_date"
        self.reserved_id = "reserved_id"
        self.available = "Available"
        self.checked_out = "Checked Out"
        self.reserved = "Reserved"
        self.book_title_id = "book_title_id"
        self.title = "title"
        self.check = 'check'
        self.genre = "genre"
        self.author = "author"
    
    def get_db(self):
        return self.db
        
    def get_unique_book_titles(self):
        return self.unique_book_titles
    
    def get_history_columns(self):
        return self.history_columns
        
    def get_suggested_books_columns(self):
        return self.suggested_books_columns
        
    def get_book_info(self):
        return self.book_info
        
    def get_status(self):
        return self.status
        
    def get_unique_book_titles_columns(self):
        return self.unique_book_titles_columns
        
    def get_book_info_columns(self):
        return self.book_info_columns
        
    def get_status_columns(self):
        return self.status_columns
    
    def get_book_search_return_columns(self):
        return self.book_search_return_columns
        
    def get_filter_books_columns(self):
        return self.filter_books_columns
        
    def get_reservation_date(self):
        return self.reservation_date
        
    def get_reserved_id(self):
        return self.reserved_id
    
    def get_return_date(self):
        return self.return_date
        
    def get_checkout_date(self):
        return self.checkout_date
    
    def search_book(self,title,book_id,genre,author):
        '''
        takes as input the search string of name and id
        of the book and returns the list of all the books
        in the library with their current statuses
        '''
        title = title.upper()
        genre = genre.upper()
        author = author.upper()
        s1 = self.get_unique_book_titles()
        s2 = self.get_book_info()
        s3 = self.get_status()
        
        titles=self.db.run_sql(s1)
        book_info=self.db.run_sql(s2)
        status_table=self.db.run_sql(s3)
        
        books=pd.DataFrame(list(book_info.fetchall()),columns=self.get_book_info_columns())
        book_titles=pd.DataFrame(list(titles.fetchall()),columns=self.get_unique_book_titles_columns()[:4])
        book_status=pd.DataFrame(list(status_table.fetchall()),columns=self.get_status_columns())
        
        all_books_join = pd.merge(books, book_titles, on=[self.book_title_id], indicator='exists')
        all_books_join = all_books_join.replace(r'^\s*$', np.nan, regex=True)
        
        all_status_join = pd.merge(all_books_join, book_status, on=[self.book_id],how='outer', indicator=True)
        all_status_join = all_status_join.sort_values(by=[self.history_id])
        all_status_join = all_status_join.drop_duplicates(subset=[self.book_id],keep='last')

        books_return = all_status_join.loc[all_status_join[self.title].str.contains(title, case = False) 
        & all_status_join[self.book_id].astype("string").str.contains(book_id) 
        & all_status_join[self.genre].str.contains(genre, case = False) 
        & all_status_join[self.author].str.contains(author, case = False)]
        books_return = books_return[self.get_book_search_return_columns()]
        return self.filter_books(books_return)


    def filter_books(self,books):
        '''
        takes as input books DataFrame
        and returns the current status for each book 
        as a new columns with name check
        '''
        
        books[self.get_reservation_date()] = pd.to_datetime(books[self.get_reservation_date()],format='%d/%m/%Y')
        books[self.get_checkout_date()] = pd.to_datetime(books[self.get_checkout_date()].copy(),format='%d/%m/%Y')
        books[self.get_return_date()] = pd.to_datetime(books[self.get_return_date()].copy(),format='%d/%m/%Y')
        
        books[self.check] = np.where(books[self.get_return_date()].isna(),
        np.where(books[self.get_checkout_date()].isna(),self.available
        ,np.where(books[self.get_reservation_date()].isna(),
        self.checked_out
        ,self.reserved))
        ,np.where(books[self.get_reservation_date()].isna(),
        self.available
        ,self.reserved))
        
        books[self.get_reservation_date()] = str(books[self.get_reservation_date()])
        books[self.get_checkout_date()] = str(books[self.get_checkout_date()])
        books[self.get_return_date()] = str(books[self.get_return_date()])
        books=books[self.get_filter_books_columns()]
        return books
        
    def build_tree(self,books,view,columns):
    
        ''' 
        takes books DataFrame,view and column list as input  
        and builds the Tree View Widget
        '''
        #deleting all books in tree view to give a fresh start every time
        clist = columns
        for row in view.get_children():
            view.delete(row)
        for x in clist:
            view.heading(x, text=x)
        books_rows = books.to_numpy().tolist()
        for i in books_rows:
            view.insert('', "end", values=i)
        return view
        

def main():
    ############################
    ####### TEST CASES #########
    ############################

    bs = BookSearch()

    test_cases3 = '''############################
######## TEST CASE 3 #######
############################'''
    print(test_cases3)
    #search_book()
    print("search_book('','1292','','')")
    print(bs.search_book("","1292","",""))
    print("TEST CASE 3 PASSED")
    print()
    print()

if __name__=='__main__':
	main()
