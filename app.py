from tkinter import *
from tkinter import ttk
import datetime
import time
import tkinter.messagebox
import sqlite3

class Portal():
    db_name = 'students.db'
    def __init__(self, root):
        self.root = root
        self.root.title('Students Data')

        #Title
        self.photo = PhotoImage(file='icon.png')
        self.label = Label(image=self.photo)
        self.label.grid(row=0, column=0)
        self.label1 = Label(font=('arial', 15, 'bold'), text='School Portal', fg='dark blue')
        self.label1.grid(row=1, column=0)

        #Records
        frame = LabelFrame(self.root, text='Add New Record')
        frame.grid(row=0,column=1)

        Label(frame, text='First Name:').grid(row=1, column=1)
        self.firstname = Entry(frame)
        self.firstname.grid(row=1, column=2)

        Label(frame, text='Last Name:').grid(row=2, column=1)
        self.lastname = Entry(frame)
        self.lastname.grid(row=2, column=2)

        Label(frame, text='Email:').grid(row=3, column=1)
        self.email = Entry(frame)
        self.email.grid(row=3, column=2)

        ttk.Button(frame, text='Add Record', command=self.add).grid(row=7, column=2)
        self.message = Label(text='', fg='red')
        self.message.grid(row=4,column=1)

        self.tree = ttk.Treeview(height=10, columns=['','',''])
        self.tree.grid(row=9, column=0, columnspan=2)
        self.tree.heading('#0', text='id')
        self.tree.column('#0', width=50)
        self.tree.heading('#1', text='First Name')
        self.tree.column('#1', width=200)
        self.tree.heading('#2', text='Last Name')
        self.tree.column('#2', width=200)
        self.tree.heading('#3', text='Email')
        self.tree.column('#3', width=200)

        def tick():
            d = datetime.datetime.now()
            Today = '{:%B %d, %Y}'.format(d)
            mytime = time.strftime('%I:%M:%S %p')
            self.lblInfo.config(text=(mytime+'\t'+Today))
            self.lblInfo.after(200,tick)

        self.lblInfo = Label(font=('arial', 20, 'bold'), fg='dark blue')
        self.lblInfo.grid(row=10, column=0)
        tick()

        #Menu
        Chooser = Menu()
        item1 = Menu()

        item1.add_command(label='Add', command=self.add)
        item1.add_command(label='Edit', command=self.edit)
        item1.add_command(label='Delete', command=self.delete)
        item1.add_separator()
        item1.add_command(label='Help', command=self.help)
        item1.add_command(label='Exit', command=self.exi)



        Chooser.add_cascade(label='File', menu=item1)
        Chooser.add_cascade(label='Add', command=self.add)
        Chooser.add_cascade(label='Edit', command=self.edit)
        Chooser.add_cascade(label='Delete', command=self.delete)
        Chooser.add_cascade(label='Help', command=self.help)
        Chooser.add_cascade(label='Exit', command=self.exi)
        root.config(menu=Chooser)
        self.viewing_records()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def viewing_records(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM students'
        db_table = self.run_query(query)
        for data in db_table:
            self.tree.insert('', 1000, text=data[0], values=data[1:])

    #Add new record
    def validation(self):
        return len(self.firstname.get()) !=0 and len(self.lastname.get()) !=0 and \
               len(self.email.get()) !=0

    def add_record(self):
        if self.validation():
            query = 'INSERT INTO students VALUES (NULL, ?, ?, ?)'
            parameters = (self.firstname.get(), self.lastname.get(), self.email.get())
            self.run_query(query, parameters)
            self.message['text']= 'Record {} {} is added'.format(self.firstname.get(), self.lastname.get())

            self.firstname.delete(0, END)
            self.lastname.delete(0, END)
            self.email.delete(0, END)
        else:
            self.message['text'] = 'Fields not completed!'

        self.viewing_records()

    def add(self):
        ad = tkinter.messagebox.askquestion('Add record', 'Want to add a new record?')
        if ad == 'yes':
            self.add_record()

    def delete_record(self):
        try:
            self.tree.item(self.tree.selection())['values'][1]
        except IndexError as err:
            self.message['text']= 'Select a record to delete'
            return

        self.message['text'] = ''
        number = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM students WHERE id = ?'
        self.run_query(query, (number,))
        self.message['text'] = 'Record {} is deleted'.format(number)
        self.viewing_records()

    def delete(self):
        de = tkinter.messagebox.askquestion('Delete record', 'Want to delete a record?')
        if de == 'yes':
            self.delete_record()

    #Edit
    def edit_box(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as err:
            self.message['text'] = 'Select a record to edit'
            return

        fname = self.tree.item(self.tree.selection())['values'][0]
        lname = self.tree.item(self.tree.selection())['values'][1]
        email = self.tree.item(self.tree.selection())['values'][2]

        self.edit_root = Toplevel()
        self.edit_root.title('Edit Record')

        Label(self.edit_root, text= 'Old Fristname').grid(row=0, column=0, sticky= W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=fname), \
              state='readonly').grid(row=0, column=2)
        Label(self.edit_root, text= 'New Fristname').grid(row=1, column=0, sticky= W)
        new_fname = Entry(self.edit_root)
        new_fname.grid(row=1, column=2)

        Label(self.edit_root, text='Old Lastname').grid(row=2, column=0, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=lname), \
              state='readonly').grid(row=2, column=2)
        Label(self.edit_root, text='New Lastname').grid(row=3, column=0, sticky=W)
        new_lname = Entry(self.edit_root)
        new_lname.grid(row=3, column=2)

        Label(self.edit_root, text='Old Email').grid(row=4, column=0, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=email), \
              state='readonly').grid(row=4, column=2)
        Label(self.edit_root, text='New Email').grid(row=5, column=0, sticky=W)
        new_email = Entry(self.edit_root)
        new_email.grid(row=5, column=2)

        Button(self.edit_root, text='Save Changes',
               command=lambda: self.edit_record(new_fname.get(), fname, new_lname.get(), lname, \
                                                new_email.get(), \
                                                email)).grid(row=12, column=2, sticky=W)
        self.edit_root.mainloop()

    def edit_record(self, new_fname, fname, new_lname, lname, new_email, email):
        query = 'UPDATE students SET FirstName=?, LastName=?, Email=? \
                WHERE FirstName=? AND LastName=? AND Email=?'
        parameters = (new_fname, new_lname, new_email, fname, lname, email)
        self.run_query(query, parameters)
        self.edit_root.destroy()
        self.message['text'] = '{} details were changed to {}'.format(fname, new_fname)
        self.viewing_records()

    def edit(self):
        ed = tkinter.messagebox.askquestion('Edit record', 'Want to Edit a record?')
        if ed == 'yes':
            self.edit_box()

    def help(self):
        tkinter.messagebox.showinfo('Log', 'Report send')

    def exi(self):
        exit = tkinter.messagebox.askquestion('Exit Application', 'Want to close an app?')
        if exit == 'yes':
            root.destroy()


if __name__ == '__main__':
    root = Tk()
    root.geometry('680x480+100+100')
    application = Portal(root)
    root.mainloop()
