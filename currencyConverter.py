from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
import requests
import socket
from bs4 import BeautifulSoup

def is_number(s):
    '''for checking if a string is a number or not'''
    try:
        float(s)
        return True
    except ValueError:
        return False


def getData(url):
    '''for getting data from url'''
    r=requests.get(url)
    return r.text


def convert():
    '''to convert the value entered in the entry widget to a specific currency value'''
    if is_number(valueEntry.get()):
        result=float(valueEntry.get())*float(currencyDict[currencyBox.get()])
        tmsg.showinfo(u"\u20B9 Rates",f"\u20B9 {valueEntry.get()} = {round(result,2)} {currencyBox.get()}")
    else:
        tmsg.showerror(u"\u20B9 Rates",u"Enter valid value in INR(\u20B9)")


if __name__ == '__main__':
    window = Tk()

    window.geometry('500x350')
    window.title("Rates")
    window.wm_iconbitmap("currencyConverter.ico")
    Label(text=	u"\u20B9 Rates", font="lucida 30 bold").grid(row=0,column=0,padx=20,pady=20)
    Label(text=u"Converts \u20B9 value to currency value", font=("lucida", 10),fg="red4").grid(row=0, column=1)
    ttk.Label(window, text=u"Enter value in INR(\u20B9):",
              font=("Times New Roman", 15)).grid(column=0,
                                                 row=1, padx=10, pady=5)

    valueEntry = Entry(window,font="times 15")
    valueEntry.insert(0,'0')
    valueEntry.grid(row=1,column=1)

    currency =StringVar()
    ttk.Label(window, text=u"Select a currency:",
              font=("Times New Roman", 15)).grid(column=0,
                                                 row=2, padx=10, pady=25)

    currencyBox = ttk.Combobox(window, width=27,textvariable=currency,font=("Times New Roman", 12))

    IPaddress = socket.gethostbyname(socket.gethostname())
    currencyDict = {}
    if IPaddress == "127.0.0.1":
        '''If there is no internet connection then fetch the currency data from the saved file'''
        ncurrencyList = []
        try:
            with open("currencyData.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    parsed = line.split(",")
                    ncurrencyList.append(parsed[0])
                    currencyDict[parsed[0]] = parsed[1][:len(parsed[1])]

            currencyBox['values'] = tuple(ncurrencyList)
        except Exception as e:
            tmsg.showerror("No internet","Check Your Internet connection\n\nConnect to Internet \nAnd"
                                         " Open the App again")
            quit()

    else:
        '''If there is internet then fetch currency data from url'''
        myHtmlData = getData("https://www.x-rates.com/table/?from=INR&amount=1")
        soup = BeautifulSoup(myHtmlData, 'html.parser')
        list1 = []
        for tr in soup.find_all('tbody')[1].find_all('tr'):
            tempLi = []
            for td in tr.find_all('td'):
                tempLi.append(td.get_text())
            list1.append(tempLi)

        currencyList=[]
        valueList=[]
        for i in range(len(list1)):
            currencyList.append(list1[i][0])
            valueList.append(list1[i][1])
        for i in range(len(currencyList)):
            currencyDict[currencyList[i]]=valueList[i]
        with open("currencyData.txt","w") as f:
            for i in range(len(currencyList)):
                f.write(currencyList[i]+","+str(valueList[i])+"\n")
        currencyBox['values'] = tuple(currencyList)

    currencyBox.grid(row=2,column=1,pady=25)
    currencyBox.current(1)

    Button(text="Convert",font=("Times New Roman", 15),command=convert,bg="cyan").grid(column=0,row=3, padx=10, pady=40)

    window.mainloop()
