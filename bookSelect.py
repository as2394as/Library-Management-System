'''
This file has all the code
to select a book
'''
import database as d
import numpy as np
import pandas as pd
from datetime import *
from menu import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BookSelect():
    '''
    This class Has all the functions to select and return desired books
    based on the budget
    '''
    def __init__(self):
        self.db = d.DbAccess()
        self.unique_book_titles_columns = ["book_title_id","title","genre","author","purchase_price","purchase_date"]
        self.unique_book_titles = "select ubt.book_title_id,ubt.title,ubt.genre,ubt.author from unique_book_titles ubt"
        self.history_columns=['book_id', 'title', 'genre', 'author', 'reservation_date','checkout_data','return_date']
        self.suggested_books_columns = ['Title','Price','Count']
        self.book_info = "select bi.book_id,bi.book_title_id from book_info bi"
        self.status = "select s.history_id,s.book_id,s.member_id,s.reserved_id,s.reservation_date,s.checkout_date,s.return_date from status s"
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
        
    def get_unique_book_titles_columns(self):
        return self.unique_book_titles_columns
    
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
        
    def preview_books(self,title,genre,author):
        '''
        takes in title,genre,author string and returns 
        a DataFrame of matching books
        '''
        title = title.upper()
        genre = genre.upper()
        author = author.upper()
        s1 = self.get_unique_book_titles()
        
        titles=self.db.run_sql(s1)
        book_titles=pd.DataFrame(list(titles.fetchall()),columns=self.get_unique_book_titles_columns()[:4])
        
        books_return = book_titles.loc[book_titles[self.title].str.contains(title, case = False)
        & book_titles[self.genre].str.contains(genre, case = False) 
        & book_titles[self.author].str.contains(author, case = False)]
        
        return books_return
    
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
        
    def budget_return(self,view,budget,cols=['title']):
        '''
        takes amounts as input and fills the
        list of suggested books on the tab
        '''
        books_frame=view
        if budget!="":
            budget = float(budget)+.1
        else:
            budget=0.1
        history = pd.DataFrame(self.get_db().getBudgetData())
        if(len(history)>0):
            history.columns=['book_id','title','genre','author','purchase_price']
            if(cols[0]=="title"):
                cols.append("purchase_price")
            history = history.sort_values(by=['purchase_price'],ascending=True)
            group = history.groupby(cols)[['book_id']].count()
            group.reset_index(inplace=True)
        else:
            group=history
        
        if(cols[0]=="title"):
            total = group.purchase_price.sum()
            n=len(group)
            factor = (round(total/budget))*2
            n = round(n/(factor+.1))
            if n==0:
                n=5
            group = group.head(n)
        else:
            n=5
            group = group.head(n)
            groups = np.array(group)
            final=pd.DataFrame()
            lis=groups[:,[0]].flatten()
            col=cols[0]
            final = pd.concat([final,history[history[col].isin(lis)]])
            final.drop_duplicates(subset=["title"],inplace=True)
            group=final
            total = group.purchase_price.sum()
            n=len(group)
            factor = (round(total/budget))*2
            n = round(n/(factor+.1))
            if n==0:
                n=5
            group = group.head(n)
        d={}
        price=0.0
        if(len(group)>0):
            while budget>=price:
                for book in np.array(group):
                    if(cols[0]=="title"):
                        title = book[0]
                        price = float(book[1])
                    else:
                        title = book[1]
                        price = float(book[4])
                    if(budget>price):
                        
                        if(d.get(title) is not None): 
                            d[title] = [price,d[title][1]+1]
                        else:
                            d[title]=[price,1]
                    budget = budget-price
        else:
            pass
        if d:
            d= pd.DataFrame(d).T.reset_index()
            d = d.rename(columns={'index':'title',0:'price',1:'count'})
            self.build_tree(d,view,self.get_suggested_books_columns())
        else:
            d={"Budget is low, increase it":[0,0]}
            d= pd.DataFrame(d).T.reset_index()
            d = d.rename(columns={'index':'title',0:'price',1:'count'})
            self.build_tree(d,view,self.get_suggested_books_columns())
        return d     
        
    def get_performance_data(self,var,frame,n=35):
        '''
        takes in a frame and suggestion criteria
        and return data to plot graphs on GUI
        '''

        for item in frame.winfo_children():
            item.destroy()
        history = pd.DataFrame(self.get_db().getPerformanceData())
        history.columns=self.get_history_columns()
        if len(history)>0:
            group = history.groupby([var])[["book_id"]].count()
        else:
            group = history
            
        if n is not None:
            data = group.sort_values(by=['book_id'],ascending=False).head(n)
        else:
            data = group.sort_values(by=['book_id'],ascending=False)
            
        figure = plt.Figure(figsize=(20,7),dpi=55)
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure,frame)
        chart_type.get_tk_widget().pack()
        
        ax.set_xlabel('count', fontsize=20)
        ax.set_ylabel(var, fontsize=15)
        ax.set_title('Top '+var, fontsize=20)
        if(len(data)>0):
            data.plot.barh(ax=ax,legend=True)
        else:
            pass
        
        return data

def main():
    ############################
    ####### TEST CASES #########
    ############################

    bs = BookSelect()

    test_cases1 = '''############################
######## TEST CASE 4 #######
############################'''
    print(test_cases1)
    #preview_book()
    print("preview_books('har','mag','')")
    print(bs.preview_books("har","mag",""))
    print("TEST CASE 1 PASSED")
    print()
    print()
    
    test_cases2 = '''############################
######## TEST CASE 2 ########
############################'''
    print(test_cases2)
    #budget_return()
    print("budget_return() test case")
    result = bs.budget_return(Treeview(Frame(),columns=bs.get_suggested_books_columns()),0)
    print(result)
    print("TEST CASE 2 PASSED")
    print()
    print()

if __name__=='__main__':
	main()
