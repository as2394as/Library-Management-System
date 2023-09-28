"""
This module handles the GUI items
and event handeling for all the widgets
"""
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import pandas as pd
import numpy as np
import bookSearch as bs
import bookCheckout as bc
import bookReturn as br
import bookSelect as bS
import database as d
import re
import matplotlib.pyplot as plt
import pickle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Constants:
    '''
    all the constants of menu class are maintained in this class
    '''

    def __init__(self):
        '''
        Constants class
        to store all constants
        for GUI class
        '''
        self.tree_columns = ['Book Id','Title','Author','Genre','Availability']
        self.preview_tree_columns = ['Title Id','Title','Author','Genre']
        self.tree_column_names = ['book_id','title','author','genre','check']
        self.history_columns=['book_id', 'title', 'genre', 'author', 'reservation_date','checkout_data','return_date']
        self.suggested_books_columns = ['Title','Price','Count']
        self.value_label="value"
        self.one_label = "1.0"
        self.book_there_error = "This book is already in selected list"
        self.member_id_error = "Member should not be empty \nand should be 4 digits long"
        self.cart_empty_error = "No book in the cart"
        self.application_name = "Library Management System"
        self.application_size = "1000x700"
        self.book_select_label = "Book Select"
        self.book_preview_label = 'Book Preview'
        self.book_search_label = "Search Book"
        self.border_color = "#658891"
        self.font = "Rockwell"
        self.bold = "bold"
        self.title = "Title"
        self.id_label = "Id"
        self.genre = "Genre"        
        self.author = "Author"
        self.availability = "Availability"
        self.book_id = "Book Id"
        self.key_release = "<KeyRelease>"
        self.book_suggestion_tab_label = 'Book Budget/Suggestions'
        
    def get_columns(self):
        return self.tree_columns
        
    def get_preview_tree_columns(self):
        return self.preview_tree_columns
    
    def get_history_columns(self):
        return self.history_columns

    def get_suggested_books_columns(self):
        return self.suggested_books_columns
        
    def get_column_names(self):
        return self.tree_column_names
        
    def get_value_label(self):
        return self.value_label
        
    def get_one_label(self):
        return self.one_label
        
    def get_book_there_error(self):
        return self.book_there_error
        
    def get_member_id_error(self):
        return self.member_id_error
        
    def get_cart_empty_error(self):
        return self.cart_empty_error
        
    def get_application_name(self):
        return self.application_name
    
    def get_application_size(self):
        return self.application_size
    
    def get_book_select_label(self):
        return self.book_select_label
        
    def get_book_search_label(self):
        return self.book_search_label
        
    def get_book_preview_label(self):
        return self.book_preview_label
    
    def get_border_color(self):
        return self.border_color
        
    def get_font(self):
        return self.font
    
    def get_bold(self):
        return self.bold
    
    def get_title(self):
        return self.title
    
    def get_id_label(self):
        return self.id_label
    
    def get_genre(self):
        return self.genre
    
    def get_author(self):
        return self.author
    
    def get_availability(self):
        return self.availability
    
    def get_book_id(self):
        return self.book_id
    
    def get_key_release(self):
        return self.key_release
    
    def get_book_suggestion_tab_label(self):
        return self.book_suggestion_tab_label

class GUI:
    '''
    all the gui widgets are maintained here
    '''

    def __init__(self,window,db):
        '''
        GUI class to create all the wdgets and tabs takes
        one window object and returns the GUI object
        '''
        self.main_win=window
        self.db = db
        self.constants = Constants()
        self.BS = bs.BookSearch()
        self.BC = bc.BookCheckout()
        self.BR = br.BookReturn()
        self.book_select = bS.BookSelect()
        self.tab_parent = Notebook(self.get_window())
        self.get_tab_parent().pack()
        self.get_window().title(self.get_constants().get_application_name())
        self.get_window().geometry(self.get_constants().get_application_size())
        self.valid_float = (self.get_window().register(self.validate_float))
        self.valid_int = (self.get_window().register(self.validate_int))
        self.valid_str = (self.get_window().register(self.validate_str))
        self.member_id=StringVar()
        self.books_selected = []
        self.book_list,self.selected_list,self.success = self.create_book_search_tab(self.get_tab_parent())
        self.book_list_for_preview,self.image_frame,self.details_frame = self.create_book_preview(self.get_tab_parent())
        self.performnace_frame = self.create_performance_tab(self.get_tab_parent())
        self.data_plot = self.get_book_select().get_performance_data('genre',self.performnace_frame)
    
    
    def get_window(self):
        return self.main_win

    def get_db(self):
        return self.db
    
    def get_constants(self):
        return self.constants
    
    def get_BS(self):
        return self.BS
    
    def get_BC(self):
        return self.BC
    
    def get_BR(self):
        return self.BR
        
    def get_book_select(self):
        return self.book_select
    
    def get_tab_parent(self):
        return self.tab_parent
    
    def get_valid_float(self):
        return self.valid_float
        
    def get_valid_int(self):
        return self.valid_int
    
    def get_valid_str(self):
        return self.valid_str
        
    def get_member_id(self):
        return self.member_id
        
    def get_books_selected(self):
        return self.books_selected
    
    def get_book_list(self):
        return self.book_list

    def get_book_list_for_preview(self):
        return self.book_list_for_preview
        
    def get_selected_list(self):
        return self.selected_list
        
    def get_success_box(self):
        return self.success
    
    def get_performance_graph_frame(self):
        return self.performnace_frame

    def get_image_frame(self):
        return self.image_frame

    def get_details_frame(self):
        return self.details_frame

    def add_book(self,from_view,to_view):
        '''
        adds the selected books from the Tree View
        to the cart widget(selected_list) list
        on click of add button
        '''
        #checking if book already in selected list and  
        #showing error if true otherwise adding the book
        items = from_view.selection()
        get_content = to_view.get(0, END)
        for i in items:
            row=list(from_view.item(i,self.get_constants().get_value_label()))
            if(row[0] not in ''.join(get_content)):
                self.get_books_selected().append(row)
                to_view.insert(END,  " : ".join([row[0],row[1]]))
            else:
                self.get_success_box().delete(self.get_constants().get_one_label(), END)
                self.get_success_box().insert(INSERT,self.get_constants().get_book_there_error())
        return to_view
            

                
    def clear_lists(self):
        '''
        clears all the lists in the GUI object
        '''
        self.get_books_selected().clear()
        self.get_selected_list().delete(0,END)
        for i in self.get_book_list().get_children():
            self.get_book_list().delete(i)
            
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
            
    def remove_book(self,selected_list):
        '''
        takes in the cart widget
        and clears the all rows in it
        '''
        for item in reversed(selected_list.curselection()):
            book_id = selected_list.get(item).split(" : ")[0]
            selected_list.delete(item)
            for b in self.get_books_selected():
                if(''.join(b).__contains__(book_id)):
                    self.get_books_selected().remove(b)
        return selected_list
    
    def return_book(self,books_selected):
        '''
        takes as input the selected books list and member id
        and calls return book functionality of BookReturn Class
        to return all the books in the cart widget if
        they are checkedout by the same member with the member_id
        otherwise show errors on the window
        '''
        if(len(books_selected)>0):
            failedMsg,successfulMsg = self.get_BR().returnBook(books_selected)
            self.get_success_box().delete(self.get_constants().get_one_label(), END)
            self.get_success_box().insert(INSERT,failedMsg)
            self.get_success_box().insert(INSERT,successfulMsg)
            self.clear_lists()
            return failedMsg,successfulMsg
        else:
            self.get_success_box().delete(self.get_constants().get_one_label(), END)
            self.get_success_box().insert(INSERT,self.get_constants().get_cart_empty_error())
            return self.get_constants().get_cart_empty_error()
            
    def reserve_book(self,books_selected,member_id):
        '''
        takes as input the selected books list and member id
        and calls reserve book functionality of BookCheckout class
        to reserve all the books in the cart widget if
        they are in checkedout status in the name of 
        member with is as member_id
        otherwise show errors on the window
        '''
        if(len(books_selected)>0):
            if(len(member_id)==4):
                failedMsg,successfulMsg = self.get_BC().reserveBook(books_selected,member_id)
                self.get_success_box().delete(self.get_constants().get_one_label(), END ) 
                self.get_success_box().insert(INSERT,failedMsg)
                self.get_success_box().insert(INSERT,successfulMsg)
                self.clear_lists()
                return failedMsg,successfulMsg
            else:
                self.get_success_box().delete(self.get_constants().get_one_label(), END)
                self.get_success_box().insert(INSERT,self.get_constants().get_member_id_error())
                return self.get_constants().get_member_id_error()
        else:
            self.get_success_box().delete(self.get_constants().get_one_label(), END)
            self.get_success_box().insert(INSERT,self.get_constants().get_cart_empty_error())
            return self.get_constants().get_cart_empty_error()
            
    def checkout(self,books_selected,member_id):
        '''
        takes as input the selected books list and member id
        and calls return book functionality of BookReturn Class
        to return all the books in the cart widget if
        they are Available and assigns it in 
        the name of member with id as member_id
        otherwise show errors on the window
        '''
        if(len(books_selected)>0):
            if(len(member_id)==4):
                failedMsg,successfulMsg = self.get_BC().checkout(books_selected,member_id)
                self.get_success_box().delete(self.get_constants().get_one_label(), END)
                self.get_success_box().insert(INSERT,failedMsg)
                self.get_success_box().insert(INSERT,successfulMsg)
                self.clear_lists()
                return failedMsg,successfulMsg
            else:
                self.get_success_box().delete(self.get_constants().get_one_label(), END)
                self.get_success_box().insert(INSERT,self.get_constants().get_member_id_error())
                return self.get_constants().get_member_id_error()
        else:
            self.get_success_box().delete(self.get_constants().get_one_label(), END)
            self.get_success_box().insert(INSERT,self.get_constants().get_cart_empty_error())
            return self.get_constants().get_cart_empty_error()
        
    def validate_float(self, value):
        '''
        validates any input field to 
        enter only float values
        '''
        if value:
            try:
                float(value)
                return True
            except ValueError:
                return False
        else:
            return True
            
    def validate_int(self, value):
        '''
        validates any input field to 
        enter only int values
        '''
        if value:
            try:
                int(value)
                return True
            except ValueError:
                return False
        else:
            return True

     
    def validate_str(self, value):
        '''
        validates any input field to 
        enter any String values
        '''
        if value:
            pattern = re.compile('^[A-Za-z0-9' '\s\,\.\&\£\$\#\=_-]*$')
            
            if pattern.match(value):
                return True
            else:
                return False
        else:
            return True 
    
    def book_search_text_picker(self,x,name,search_id,genre,author):
        '''
        for search tab
        picks text and number from the seach bars to search 
        the books and populate TreeView with the available book
        '''
        books=self.get_BS().search_book(name.get(),search_id.get(),genre.get(),author.get())
        self.get_BS().build_tree(books,self.get_book_list(),self.get_constants().get_columns())

        
    def create_book_search_tab(self,tab_parent):
        '''
        Creates book search tab
        takes parent tab as input and packs
        required widgets on search tab
        '''
        select_tab = Frame(tab_parent,width=800,height=500)
        tab_parent.add(select_tab, text=self.get_constants().get_book_select_label())
        
        frame1 = tk.Frame(select_tab,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1)
        frame1.pack()
        
        frame2 = tk.Frame(frame1,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1)
        frame2.pack()

        name = StringVar()
        search_id = StringVar()
        genre = StringVar()
        author = StringVar()

        selected_books_label=Label(frame2,font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()),text=self.get_constants().get_book_search_label())
        selected_books_label.pack()
        
        search_label=Label(frame2,font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()) ,text=self.get_constants().get_title())
        search_label.pack(side=LEFT)
        textbox=Entry(frame2,width=30, textvariable=name,validate = 'key', validatecommand = (self.get_valid_str(),'%P'))
        textbox.pack(side=LEFT)
        textbox.bind(self.get_constants().get_key_release(),lambda x: self.book_search_text_picker(x,name,search_id,genre,author))

        search_id_label=Label(frame2,font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()),text = self.get_constants().get_id_label())
        search_id_label.pack(side=LEFT)
        idbox=Entry(frame2,width=30, textvariable=search_id,validate = 'key', validatecommand = (self.get_valid_int(),'%P'))
        idbox.pack(side=LEFT)
        idbox.bind("<KeyRelease>",lambda x: self.book_search_text_picker(x,name,search_id,genre,author))
        
        search_genre=Label(frame2,font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()),text = self.get_constants().get_genre())
        search_genre.pack(side=LEFT)
        textbox_genre=Entry(frame2,width=30, textvariable=genre,validate = 'key', validatecommand = (self.get_valid_str(),'%P'))
        textbox_genre.pack(side=LEFT)
        textbox_genre.bind(self.get_constants().get_key_release(),lambda x: self.book_search_text_picker(x,name,search_id,genre,author))

        search_author=Label(frame2,font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()) ,text=self.get_constants().get_author())
        search_author.pack(side=LEFT)
        textbox_author=Entry(frame2,width=30, textvariable=author,validate = 'key', validatecommand = (self.get_valid_str(),'%P'))
        textbox_author.pack(side=LEFT)
        textbox_author.bind(self.get_constants().get_key_release(),lambda x: self.book_search_text_picker(x,name,search_id,genre,author))
        frame3 = tk.Frame(frame1,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1)
        frame3.pack()

        tree = Treeview(frame3,columns=self.get_constants().get_columns(), show="headings", height=10,selectmode='extended')
        tree.column('#0', width=0, stretch=NO)
        tree.column(self.get_constants().get_book_id(), anchor=CENTER, width=100)
        tree.column(self.get_constants().get_title(), anchor=CENTER, width=300)
        tree.column(self.get_constants().get_author(), anchor=CENTER, width=100)
        tree.column(self.get_constants().get_genre(), anchor=CENTER, width=100)
        tree.column(self.get_constants().get_availability(), anchor=CENTER, width=100)
        
        updown = Scrollbar(frame3,orient="vertical",command=tree.yview)
        updown.pack(side=RIGHT,fill=Y)
        
        tree.config(yscrollcommand=updown.set)
        tree.pack()

        frame4 = tk.Frame(frame1)
        frame4.pack()
        
        frame5 = tk.Frame(frame1)
        frame5.pack()
        
        frame5_1 = Frame(frame5)
        frame5_1.pack(side=LEFT)
        frame5_2 = Frame(frame5)
        frame5_2.pack(side=RIGHT)
        
        add_button = Button(frame4,text='add to cart',command= lambda : self.add_book(self.get_book_list(),self.get_selected_list()))
        add_button.pack(side= LEFT)

        remove_button = Button(frame4,text='remove from cart',command = lambda : self.remove_book(self.get_selected_list()))
        remove_button.pack(side= RIGHT)
        
        selected_books_label=Label(frame5_1,font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()),text='Cart          ')
        selected_books_label.pack()
        selected_scrollbar = Scrollbar(frame5_1, orient= 'vertical')
        selected_scrollbar.pack(side=RIGHT,fill=Y)
        booklist1 = Listbox(frame5_1,font=(self.get_constants().get_font(), 10, self.get_constants().get_bold()),yscrollcommand=selected_scrollbar.set,width=55,height=15,selectmode = EXTENDED)
        booklist1.pack()
        selected_scrollbar.config(command=booklist1.yview)
        
        status_label=Label(frame5_2,font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()),text='        Result Box')
        status_label.pack()
        status_scrollbar = Scrollbar(frame5_2, orient= 'vertical')
        status_scrollbar.pack(side=RIGHT,fill=Y)
        status_textbox=Text(frame5_2,width=50,height=15,fg='black',yscrollcommand=status_scrollbar.set)
        status_textbox.pack()
        status_scrollbar.config(command=status_textbox.yview)
        
        frame6 = tk.Frame(frame1,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1)
        frame6.pack()
        
        self.member_id=StringVar()
        
        
        search_label_id=Label(frame6,text='Enter member id')
        search_label_id.pack(side=LEFT)
        member_id_text=Entry(frame6,width=30, textvariable=self.get_member_id(),validate = 'key', validatecommand = (self.get_valid_int(),'%P'))
        member_id_text.pack(side=LEFT)
        
        checkout_button = Button(frame6,text='Checkout',command= lambda : self.checkout(self.get_books_selected(),self.get_member_id().get()))
        checkout_button.pack(side=LEFT)
        
        return_button = Button(frame6,text='return',command = lambda : self.return_book(self.get_books_selected()))
        return_button.pack(side=LEFT)
        
        reserve_button = Button(frame6,text='Reserve',command= lambda : self.reserve_book(self.get_books_selected(),self.get_member_id().get()))
        reserve_button.pack(side=LEFT)
        
        
        return tree,booklist1,status_textbox

    def get_image(self,book_name):
        """
        This function handles getting book_title_id
        based on the book_name passed as input
        from the db table unique_book_titles
        """
        
        image_id = self.get_db().get_image_id(book_name)
        if(image_id is not None):
            if(len(pd.DataFrame(image_id).book_title_id)>0):
                image_id = pd.DataFrame(image_id).book_title_id[0]
            else:
                image_id=0
            image = self.get_db().get_image(int(image_id))
            if(len(pd.DataFrame(image).photo)>0):
                image = pd.DataFrame(image).photo[0]
                return image
        return None
        
    def OnSingleClick(self,event):
        '''
        Event Handler for Tree view 
        on the Preview Screen to select_tab
        a book and show its image
        '''
        
        plt.close()
        tree = self.get_book_list_for_preview()
        item = tree.selection()
        image = self.get_image(tree.item(item,self.get_constants().get_value_label())[1])
        for i in self.get_image_frame().winfo_children():
            i.destroy()
            
        for i in self.get_details_frame().winfo_children():
            i.destroy()
            
        title_label=Label(self.get_details_frame(),font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()) ,text=self.get_constants().get_title()+'  :'+tree.item(item,self.get_constants().get_value_label())[1])
        title_label.pack(side=TOP)
        author_label=Label(self.get_details_frame(),font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()) ,text=self.get_constants().get_author()+' :    '+tree.item(item,self.get_constants().get_value_label())[3])
        author_label.pack(side=TOP)
        genre_label=Label(self.get_details_frame(),font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()) ,text=self.get_constants().get_genre()+' :              '+tree.item(item,self.get_constants().get_value_label())[2])
        genre_label.pack(side=TOP)
        
        fig = plt.figure(figsize=(5,5),dpi=50)
        fig.subplots_adjust(left=0.00, bottom=0.01, right=0.99, top=0.99, wspace=0, hspace=0)
        canvas = FigureCanvasTkAgg(fig, self.get_image_frame())
        canvas.get_tk_widget().pack()
        
        if image is not None:
            photo = pickle.loads(image)
            plt.axis('off')
            plt.imshow(photo)
            
    def book_search_text_picker_for_preview(self,x,name,genre,author):
        '''
        For preview tab
        picks text and number from the seach bars to search 
        the books and populate TreeView with the available book
        '''
        books=self.get_book_select().preview_books(name.get(),genre.get(),author.get())
        self.get_BS().build_tree(books,self.get_book_list_for_preview(),self.get_constants().get_preview_tree_columns())
    
    def create_book_preview(self,tab_parent):
        '''
        This Function accepts the parent tab and 
        creates the preview tab on the GUI
        '''
        select_tab = Frame(tab_parent,width=800,height=500)
        tab_parent.add(select_tab, text=self.get_constants().get_book_preview_label())
        
        frame1 = tk.Frame(select_tab,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1)
        frame1.pack()
        
        frame2 = tk.Frame(frame1,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1)
        frame2.pack()

        frame4 = tk.Frame(select_tab,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1)
        frame4.pack()
        
        image_frame = tk.Frame(frame4,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1,name="image_frame")
        image_frame.pack(side=LEFT)
        
        details_frame = tk.Frame(frame4,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1,name="details_frame")
        details_frame.pack(side=RIGHT)
        

        name = StringVar()
        search_id = StringVar()
        genre = StringVar()
        author = StringVar()

        selected_books_label=Label(frame2,font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()),text=self.get_constants().get_book_preview_label())
        selected_books_label.pack()
        
        search_label=Label(frame2,font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()) ,text=self.get_constants().get_title())
        search_label.pack(side=LEFT)
        textbox=Entry(frame2,width=30, textvariable=name,validate = 'key', validatecommand = (self.get_valid_str(),'%P'))
        textbox.pack(side=LEFT)
        textbox.bind(self.get_constants().get_key_release(),lambda x: self.book_search_text_picker_for_preview(x,name,genre,author))
        
        search_genre=Label(frame2,font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()) ,text=self.get_constants().get_genre())
        search_genre.pack(side=LEFT)
        textbox_genre=Entry(frame2,width=30, textvariable=genre,validate = 'key', validatecommand = (self.get_valid_str(),'%P'))
        textbox_genre.pack(side=LEFT)
        textbox_genre.bind(self.get_constants().get_key_release(),lambda x: self.book_search_text_picker_for_preview(x,name,genre,author))

        search_author=Label(frame2,font=(self.get_constants().get_font(), 15, self.get_constants().get_bold()) ,text=self.get_constants().get_author())
        search_author.pack(side=LEFT)
        textbox_author=Entry(frame2,width=30, textvariable=author,validate = 'key', validatecommand = (self.get_valid_str(),'%P'))
        textbox_author.pack(side=LEFT)
        textbox_author.bind(self.get_constants().get_key_release(),lambda x: self.book_search_text_picker_for_preview(x,name,genre,author))
        frame3 = tk.Frame(frame1,highlightbackground="#658891", highlightthickness=1)
        frame3.pack()

        tree = Treeview(frame3,columns=self.get_constants().get_preview_tree_columns(), show="headings", height=10,selectmode='extended')
        tree.column('#0', width=0, stretch=NO)
        tree.column('Title Id', anchor=CENTER, width=100)
        tree.column('Title', anchor=CENTER, width=300)
        tree.column('Author', anchor=CENTER, width=100)
        tree.column('Genre', anchor=CENTER, width=100)
        updown = Scrollbar(frame3,orient="vertical",command=tree.yview)
        updown.pack(side=RIGHT,fill=Y)
        
        tree.config(yscrollcommand=updown.set)
        tree.pack()
        tree.bind("<ButtonRelease-1>", self.OnSingleClick)
        
        return tree,image_frame,details_frame
        
    def OptionMenu_CheckButton(self,var):
        '''
        event handler for change of filter criteria
        from the option box on the screen
        '''
        self.get_book_select().get_performance_data(var,self.get_performance_graph_frame())
        
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
        history.columns=['book_id','title','genre','author','purchase_price']
        if(cols[0]=="title"):
            cols.append("purchase_price")
        history = history.sort_values(by=['purchase_price'],ascending=True)
        group = history.groupby(cols)[['book_id']].count()
        group.reset_index(inplace=True)
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
        
        
    def create_performance_tab(self,tab_parent):  
        '''
        takes parent tab and creates the performance tab and 
        puts it on the parent tab
        '''
        performance_tab = Frame(tab_parent,width=800,height=500)
        tab_parent.add(performance_tab, text="Budget")
        
        frame1=tk.Frame(performance_tab,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1)
        frame1.pack()
        frame2 = tk.Frame(performance_tab,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1)
        frame2.pack()
        
        frame3=tk.Frame(performance_tab,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1)
        frame3.pack()
        
        frame4=tk.Frame(performance_tab,highlightbackground=self.get_constants().get_border_color(), highlightthickness=1)
        frame4.pack()
        
        selected_books_label=Label(frame1,font=("Rockwell", 15, 'bold'),text=self.get_constants().get_book_suggestion_tab_label())
        selected_books_label.pack()

        variable = StringVar()
        label = Label(frame1, text='Select Popular Criteria')
        w = OptionMenu(frame1, variable, "genre","genre", "author", "title",command = self.OptionMenu_CheckButton)
        label.pack(side=LEFT)
        w.pack(side=RIGHT)

        budget_amount=StringVar()
        search_label=Label(frame3,text='Enter the budget in £')
        search_label.pack(side=LEFT)
        budget_amount_textbox=Entry(frame3,width=30, textvariable=budget_amount, validate = 'key', validatecommand = (self.get_valid_float(),'%P'))
        budget_amount_textbox.pack(side=LEFT)
        
        selected_books_label=Label(frame4,font=("Rockwell", 15, 'bold'),text='Suggested Books')
        selected_books_label.pack()
        
        tree = Treeview(frame4,columns=self.get_constants().get_suggested_books_columns(), show="headings", height=10,selectmode='extended')

        lookup_button = Button(frame3,text='Look Up',command= lambda : self.get_book_select().budget_return(tree,budget_amount.get(),[variable.get()]))
        lookup_button.pack(side=LEFT)
        
        tree.column('#0', width=0, stretch=NO)
        tree.column('Title', anchor=CENTER, width=300)
        tree.column('Price', anchor=CENTER, width=100)
        tree.column('Count', anchor=CENTER, width=100)
        updown = Scrollbar(frame4,orient="vertical",command=tree.yview)
        updown.pack(side=RIGHT,fill=Y)
        
        tree.config(yscrollcommand=updown.set)
        tree.pack()
        
        return frame2

def main():
    ############################
    ####### MAIN GUI ###########
    ############################

    Db = d.DbAccess()
    Db.initialiseDb()    
    window = Tk()
    gui=GUI(window,Db)
    di={"book_id":["1292"],"member_id":["1234"],"reserved_id":[],"history_id":[],"title":["abc"],"author":["abc"],"genre":["abc"],"reservation_date":[],"checkout_date":[],"return_date":[]}
    test_cases1 = '''############################
######## TEST CASE 1 ########
############################'''
    print(test_cases1)
    #get_image()
    print("get_image() test case")
    print("image lenght:",gui.get_image("Artemis Fowl"))
    print("TEST CASE 1 PASSED")
    print()
    print()

    test_cases2 = '''############################
######## TEST CASE 2 ########
############################'''
    print(test_cases2)
    #validate_str()
    print("validate_str() test case")
    print("Valid String:",gui.validate_str("Artemis Fowl"))
    print("TEST CASE 2 PASSED")
    print()
    print()

    test_cases3 = '''############################
######## TEST CASE 3 ########
############################'''
    print(test_cases3)
    #validate_int()
    print("validate_int() test case")
    print("Valid int:",gui.validate_int("123"))
    print("TEST CASE 3 PASSED")
    print()
    print()

    test_cases4 = '''############################
######## TEST CASE 4 ########
############################'''
    print(test_cases4)
    #validate_float()
    print("validate_float() test case")
    print("Valid float:",gui.validate_float("123.0"))
    print("TEST CASE 4 PASSED")
    print()
    print()

    test_cases5 = '''############################
######## TEST CASE 5 ########
############################'''
    print(test_cases5)
    #checkout()
    print("checkout() test case")
    book = pd.DataFrame(di,index=[])
    print("Checkout: ",gui.checkout(book,"1234"))
    print("TEST CASE 5 PASSED")
    print()
    print()

    test_cases6 = '''############################
######## TEST CASE 6 ########
############################'''
    print(test_cases6)
    #return_book()
    print("return_book() test case")
    book = pd.DataFrame(di,index=[])
    print("Return Book: ",gui.return_book(book))
    print("TEST CASE 6 PASSED")
    print()
    print()

    test_cases7 = '''############################
######## TEST CASE 7 ########
############################'''
    print(test_cases7)
    #reserve_book()
    print("reserve_book() test case")
    book = pd.DataFrame(di,index=[])
    print("Reserve Book: ",gui.reserve_book(book,"1234"))
    print("TEST CASE 7 PASSED")
    print()
    print()

    test_cases8 = '''############################
######## TEST CASE 8 ########
############################'''
    print(test_cases8)
    #add_book()
    print("add_book() test case")
    tree = Treeview()
    print("add Book List: ",gui.add_book(tree,Listbox()).get(0, END))
    print("TEST CASE 8 PASSED")
    print()
    print()
    
    test_cases9 = '''############################
######## TEST CASE 4 #######
############################'''
    print(test_cases1)
    #preview_book()
    print("preview_books('har','mag','')")
    print(gui.get_book_select().preview_books("har","mag",""))
    print("TEST CASE 1 PASSED")
    print()
    print()
    
    test_cases10 = '''############################
######## TEST CASE 2 ########
############################'''
    print(test_cases2)
    #budget_return()
    print("budget_return() test case")
    result = gui.get_book_select().budget_return(Treeview(Frame(),columns=gui.get_constants().get_suggested_books_columns()),0)
    print(result)
    print("TEST CASE 2 PASSED")
    print()
    print()

    
    window.mainloop()

if __name__=='__main__':
	main()
