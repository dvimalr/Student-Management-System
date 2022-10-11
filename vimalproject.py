from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sqlite3 import *
import traceback
import requests
import socket
import bs4

root = Tk()                             #ROOT WINDOW
root.title("S. M. S.")
root.geometry("900x600+400+100")
root.resizable(True, True)

try:
        web_address = "https://ipinfo.io/"
        res = requests.get(web_address)
        data = res.json()
        city_name = data['city']
        location = Label(root, text = city_name, font = ('arial', 20))
        location.place(x = 150, y = 460)

        a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
        a2 = "&q=" + city_name
        a3 = "&appid=c6e315d09197cec231495138183954bd"
        web_address = a1 + a2 + a3
        res= requests.get(web_address)
        data = res.json()
        at = data['main']['temp']
        temp = Label(root, text = at, font  = ('arial', 20))
        temp.place(x = 450, y = 460)

        web_add = "https://www.brainyquote.com/quote_of_the_day"
        res = requests.get(web_add)
        data = bs4.BeautifulSoup(res.text, "html.parser")
        info = data.find('img', {"class":"p-qotd"})
        quote = info['alt']
        q = Label(root, text = quote, font = ('arial', 20), fg = "#1f6f8b", background = '#e4f0da')
        q.place(x = 130, y = 530)

except Exception as e:
        showerror("Error", "Check your Internet Connection")

def f1():
	root.withdraw()
	add_st.deiconify()

def f2():
	add_st.withdraw()
	root.deiconify()

def f3():
        con = None
        try:
                con = connect("VD.db")
                sql = "insert into student values('%d', '%s', '%d');"
                cursor = con.cursor()
                temp=add_st_entrno.get()
                bol=False

                
                if len(temp)==0:
                    showerror("FAILURE", "Roll No should not be empty")
                    bol=False

                elif int(temp) == 0:
                        showerror("FAILURE", "Roll no. cannot be zero")
                        bol=False

                elif int(temp) < 0:
                        showerror("FAILURE", "Roll no.should be positive")
                        bol=False
                    
                elif int(temp) > 0 & int(temp) < 100:
                        bol=True
                        rno = int(temp)
                        
                else:
                        showerror("FAILURE", "Roll No should be between 1 to 100")
                        bol=False
                
                

                name = add_st_entname.get()
                
                #print(len(name))
                temp2=True
                if len(name)==0:
                        showerror("FAILURE", "Name cannot be empty ")
                        temp2=False
                elif not (("A" <= name and name <= "Z") or ("a" <= name and name <= "z") or (name == " ")):
                        showerror("FAILURE", "Name cannot contain numbers ")
                        temp2=False
                elif len(name)<2:
                        showerror("FAILURE", "Name cannot be of one nameacter")
                        temp2=False

                temp3=add_st_entmarks.get()                     
                bol2=False
                

                if len(temp3)==0:
                    showerror("FAILURE", "marks should not be empty")
                    bol2=False
                elif int(temp3)>0 and int(temp3)<=100:
                        marks=int(temp3)
                        bol2=True
                else:
                        showerror("FAILURE", "Invalid Marks")
                        bol2=False
                
                if bol and temp2 and bol2:
                        
                        cursor.execute(sql % (rno, name, marks))
                        con.commit()
                        showinfo("Success", "Record Added")
                    
        except Exception as e:
                showerror("Failure", e)
                traceback.print_exc()
                con.rollback()
                        
        finally:
                if con is not None:
                    con.close()
                    add_st_entrno.delete(0, END)
                    add_st_entname.delete(0, END)
                    add_st_entmarks.delete(0, END)
                    add_st_entrno.focus()

def f4():
	root.withdraw()
	view_st.deiconify()
	view_st_data.delete(1.0, END)
	con = None
	try:
		con = connect("VD.db")
		sql = "select * from student"
		cursor = con.cursor()
		cursor.execute(sql)
		data = cursor.fetchall()
		info = ""
		for d in data:
			info = info + "Rno: " +  str(d[0]) + "Name: " +  str(d[1]) + "Marks: " +  str(d[2]) + "\n"
		view_st_data.insert(INSERT, info)
	except Exception as e:
		showerror("issue", e)
	finally:
		if con is not None:
			con.close()

def f5():
	view_st.withdraw()
	root.deiconify()

def f6():
        root.withdraw()
        update_st.deiconify()

def f7():
        con = None
        try:
                con = connect("VD.db")
                sql = "update student set name = '%s',marks = '%d' where rno = '%d'"
                rno = int(update_st_entrno.get())
                
                name = update_st_entname.get()
                temp4=True
                if len(name)==0:
                        showerror("FAILURE", "Name cannot be empty ")
                        temp4=False
                elif not name.isalpha():
                        showerror("FAILURE", "Name cannot contain numbers ")
                        temp4=False
                elif len(name)<2:
                        showerror("FAILURE", "Name cannot be of one nameacter")
                        temp4=False

                #marks = int(update_st_entmarks.get())
                temp5=update_st_entmarks.get()                     
                bol3=False
                

                if len(temp5)==0:
                    showerror("FAILURE", "marks should not be empty")
                    bol3=False
                elif int(temp5)>0 and int(temp5)<=100:
                        marks=int(temp5)
                        bol3=True
                else:
                        showerror("FAILURE", "Invalid Marks")
                        bol3=False
                
                if bol3 and temp4 and temp5:

                        cursor = con.cursor()
                        cursor.execute(sql % (name, marks, rno))
                        if cursor.rowcount == 1:
                                con.commit()
                                showinfo("Success", "Record Updated")
                        else:
                                showerror("FAILURE", "Record does not exists")

        except Exception as e:
                showerror("Issue", e)
                
        finally:
                if con is not None:
                        con.close()
                        update_st_entrno.delete(0, END)
                        update_st_entname.delete(0, END)
                        update_st_entmarks.delete(0, END)
                        update_st_entrno.focus()

def f8():
	update_st.withdraw()
	root.deiconify()

def f9():
        root.withdraw()
        delete_st.deiconify()

def f10():
        con = None
        try:
                con = connect("VD.db")
                rno = int(delete_st_entrno.get())
                sql = "delete from student where rno = '%d' "
                cursor = con.cursor()
                cursor.execute(sql % (rno))
                if cursor.rowcount == 1:
                        con.commit()
                        showinfo("Success", "Record Deleted")
                else:
                        showerror("FAILURE", "Record does not exists")

        except Exception as e:
                showerror("issue", e)
                
        finally:
                if con is not None:
                        con.close()
                        delete_st_entrno.delete(0, END)


def f11():
	delete_st.withdraw()
	root.deiconify()

def f12():
        try:
                con=connect("VD.db")
                cursor=con.cursor()
                cursor.execute("SELECT name, marks  FROM student")
                resultt = cursor.fetchall()
                final_resultt = [i[0] for i in resultt]
                final_resultt1 = [i[1] for i in resultt]
        except Exception as e:
                showerror("issue",e)
        plt.bar(final_resultt,final_resultt1, linewidth=2)
        plt.grid(True)
        plt.xlabel("Name")
        plt.ylabel("Marks")
        plt.title("Batch Information!")
        plt.show()



btnAdd = Button(root, text = "Add", width = 10, font = ('Arial', 18, 'bold'), command = f1)
btnView = Button(root, text = "View", width = 10, font = ('Arial', 18, 'bold'), command = f4)
btnUpdate = Button(root, text = "Update", width = 10, font = ('Arial', 18, 'bold'), command = f6)
btnDelete = Button(root, text = "Delete", width = 10, font = ('Arial', 18, 'bold'), command = f9)
btncharts = Button(root, text = "Charts", width = 10, font = ('Arial', 18, 'bold'), command = f12)
lblLoc = Label(root, text = "Location:", font = ('Arial', 22, 'bold'))
lblTemp = Label(root, text = "Temp:", font = ('Arial', 22, 'bold'))
lblQOTD = Label(root, text = "QOTD:", font = ('Arial', 22, 'bold'))

btnAdd.pack(pady = 20)
btnView.pack(pady = 20)
btnUpdate.pack(pady = 20)
btnDelete.pack(pady = 20)
btncharts.pack(pady = 20)
lblLoc.place(x = 10, y = 460)
lblTemp.place(x = 350, y = 460)
lblQOTD.place(x = 10, y = 530)

add_st = Toplevel(root)                 # ADD STUDENT WINDOW
add_st.title("Add St.")
add_st.geometry("500x600+500+100")
add_st.resizable(False, False)

add_st_lblrno = Label(add_st, text = "enter rno:", font = ('arial', 18, 'bold'))
add_st_entrno = Entry(add_st, bd = 5, font = ('arial', 18, 'bold'))
add_st_lblname = Label(add_st, text = "enter name:", font = ('arial', 18, 'bold'))
add_st_entname = Entry(add_st, bd = 5, font = ('arial', 18, 'bold'))
add_st_lblmarks = Label(add_st, text = "enter marks:", font = ('arial', 18, 'bold'))
add_st_entmarks = Entry(add_st, bd = 5, font = ('arial', 18, 'bold'))
add_st_btnsave = Button(add_st, text = "Save", width = 20, font = ('arial', 22, 'bold'), command = f3)
add_st_btnback = Button(add_st, text = "Back", width = 20, font = ('arial', 22, 'bold'), command = f2)

add_st_lblrno.pack(pady = 10)
add_st_entrno.pack(pady = 10)
add_st_lblname.pack(pady = 10)
add_st_entname.pack(pady = 10)
add_st_lblmarks.pack(pady = 10)
add_st_entmarks.pack(pady = 10)
add_st_btnsave.pack(pady = 20)
add_st_btnback.pack(pady = 10)
add_st.withdraw()

view_st = Toplevel(root)                # VIEW STUDENT WINDOW
view_st.title("View St.")
view_st.geometry("500x600+500+100")
view_st.resizable(False, False)

view_st_data = ScrolledText(view_st, width = 36, height = 10, font = ('arial', 18, 'bold'))
view_st_btnback = Button(view_st, text = "Back", font = ('arial', 18, 'bold'), command = f5)

view_st_data.pack(pady = 10)
view_st_btnback.pack(pady = 10)
view_st.withdraw()

update_st = Toplevel(root)              # UPDATE STUDENT WINDOW
update_st.title("Update St.")
update_st.geometry("500x600+500+100")
update_st.resizable(False, False)

update_st_lblrno = Label(update_st, text = "enter rno:", font = ('arial', 18, 'bold'))
update_st_entrno = Entry(update_st, bd = 5, font = ('arial', 18, 'bold'))
update_st_lblname = Label(update_st, text = "enter name:", font = ('arial', 18, 'bold'))
update_st_entname = Entry(update_st, bd = 5, font = ('arial', 18, 'bold'))
update_st_lblmarks = Label(update_st, text = "enter marks:", font = ('arial', 18, 'bold'))
update_st_entmarks = Entry(update_st, bd = 5, font = ('arial', 18, 'bold'))
update_st_btnsave = Button(update_st, text = "Save", width = 20, font = ('arial', 22, 'bold'), command = f7)
update_st_btnback = Button(update_st, text = "Back", width = 20, font = ('arial', 22, 'bold'), command = f8)

update_st_lblrno.pack(pady = 10)
update_st_entrno.pack(pady = 10)
update_st_lblname.pack(pady = 10)
update_st_entname.pack(pady = 10)
update_st_lblmarks.pack(pady = 10)
update_st_entmarks.pack(pady = 10)
update_st_btnsave.pack(pady = 20)
update_st_btnback.pack(pady = 10)
update_st.withdraw()

delete_st = Toplevel(root)              # DELETE STUDENT WINDOW
delete_st.title("Delete St.")
delete_st.geometry("500x600+500+100")
delete_st.resizable(False, False)

delete_st_lblrno = Label(delete_st, text = "enter rno:", font = ('arial', 18, 'bold'))
delete_st_entrno = Entry(delete_st, bd = 5, font = ('arial', 18, 'bold'))
delete_st_btnsave = Button(delete_st, text = "Delete", width = 20, font = ('arial', 22, 'bold'), command = f10)
delete_st_btnback = Button(delete_st, text = "Back", width = 20, font = ('arial', 22, 'bold'), command = f11)

delete_st_lblrno.pack(pady = 10)
delete_st_entrno.pack(pady = 10)
delete_st_btnsave.pack(pady = 20)
delete_st_btnback.pack(pady = 10)
delete_st.withdraw()

root.mainloop()
