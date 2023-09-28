# LibraryManagementSystem
Library Management System built using python

My Library Application

It is a very complex application with 4 sections

1.	GUI
2.	Database
3.	book return/checkout/reserve
4.	suggest books

Let’s talk about GUI first

GUI has a window and 3 tabs
First is the Search Tab:
•	Here you can search the books and go for the return/checkout/reserve sections to do the desired task.
•	Here the first Tree view(List of all the books in the library) will automatically populate as you enter allowed values in the Entry Boxes for ID, Title, Genre and Author.
•	You will also see the Current Availability status of the book. 
•	You can enter values in all Entry Boxes simultaneously and the view will filter automatically based on all 4 Entry Boxes.
•	In the Tree view you can select one or more books at once and then use add/remove buttons to add/remove books in your cart.
•	If you try to add a book that is already in the cart the appropriate error message will be shown in the Result box widget which is just to show error and success messages.
•	 Below the Tree view a List Box widget which is the cart where to add the selected books.
•	Now you can choose to checkout, reserve or return the books and also enter the member id for which you want to do the operation.
•	Based on the Current Availability status the operation will be performed and appropriate error message will be shown for example
“The book with id:1397
could not be booked as it is Checked Out “
“The book with id:2431
is successfully checked out”
•	The member ID check is also there which shows an error if the member id is not present or is not 4 digit long.
	Special checks are there to ensure that the reserved books which were returned can also be rebooked by the same member who reserved the 
	book apart from anyone else with the appropriate error and success message for this particular scenario.
	Reserved book can also be returned and it is made sure that the Current Availability status shows that book as in reserved status unless it is checked out.
There are 3 statuses a book can be in
1.	Checked Out
2.	Reserved
3.	Available
•	A member can only checkout available books or the reserved books which were returned by the person who checked the book out.
•	A member can only reserve a book that is checked out
•	A member can return books that are checked out and reserved based on what is the member id that is returning the book and the current value of the reserved id 
	and member id for that particular book in the db.
All the Entry Boxes and controlled by  validation function which only allow valid values to be entered in the box for example ID Entry Box will 
not allow anything other than digits(not even float only numbers)
Similarly Title Will only allow strings and some special characters only like -,£,& etc

Next Comes the Preview Tab:
This Tab is to view covers and information of all the distinct books in the library. 
•	You can search the books from the 2 entry boxes given for Title, Genre, Author.
•	When the Tree view populates you can click on a book and below the tree view a frame will be populated with the stored image of the book along with the details of the book.
•	First 150 out of the 300+ books have an image stored for them in the db others will have a blank white screen. 
I am proud of this module as I used beautiful soup to get the images out of the web and store in the DB and automatically map the book_title_id with the image id in the book_image table.

Next We have the Suggest Books Tab:
•	Here You will see a graph depicting the trending books, authors and genres in the beginning which is populated based on the book genres at the top and dynamically 
	gets the latest data from the history table every time you change the filter criteria to any other available options like Top Genre, Top Title, Top Author
•	The Graph gets the data from the loan_reservation_history table which is updated every time a books is booked reserved or returned.
•	Also Below is an Entry Box which also based on the filter criteria as it suggests the books the librarian should buy based on the Budget 
	he/she passes and the filter criteria selected.
•	It show appropriate error messages if the budget is too high or to small.
I m Proud of this section as it shows the suggestions based on trending genre, author and books and also takes into considerstion the budget provided by the librarian

ALL the test cases at the end of the file are written in such a way that they test each function in the file.
