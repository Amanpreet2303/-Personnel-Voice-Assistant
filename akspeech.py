from urllib.parse import quote_from_bytes
import speech_recognition as sr
import pyttsx3
import wikipedia
import pywhatkit
import datetime
import wolframalpha
import webbrowser
import pyjokes
import requests,json
from bs4 import BeautifulSoup 
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import smtplib
  


listener=sr.Recognizer()
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
def talk(text):
    engine.say(text)
    engine.runAndWait()
def horoscope(zodiac_sign: int, day: str) -> str:
    
      # website taking the user input variables
    url = (
        "https://www.horoscope.com/us/horoscopes/general/"
        f"horoscope-general-daily-{day}.aspx?sign={zodiac_sign}" 
    )
      
    # soup will contain all the website's data
    soup = BeautifulSoup(requests.get(url).content, 
                         "html.parser") 
    # print(soup)
      
    # we will search for main-horoscope
    # class and we will simply return it
    return soup.find("div", class_="main-horoscope").p.text 
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
     
    # Enable low security in gmail
    server.login('your email id', 'your email password')
    server.sendmail('your email id', to, content)
    server.close()
def take_command():
    try:
        with sr.Microphone() as source:
            talk("Try speaking something ")
            print("i am listening")
            voice=listener.listen(source)
            command=listener.recognize_google(voice)
            command=command.lower()
            print(command)
            if 'play' in command:
                song=command.replace('play',' ')
                talk("playing"+song)
                pywhatkit.playonyt(song)
            elif  'tell me about' in command:
                 talk('Searching Wikipedia...')
                 command = command.replace("wikipedia", "")
                 results = wikipedia.summary(command, sentences = 2)
                 talk("According to Wikipedia")
                 print(results)
                 talk(results)
            elif 'time' in command:
                time=datetime.datetime.now().strftime('%I:%M %p')#I is the 12 hour  format ofgetting  time'
                print(time)
                talk("the current time is"+time)

            elif 'what is your name' in command:
                talk("My name is Maria, how can i help you")
           
            elif 'who' in command:
                person= command.replace('who','')
                info=wikipedia.summary(person,2)
                print(info)
                talk(info)
            elif 'are you a ghost' in command:
                talk("no im your voice assistant")
            elif 'joke' in command:
                jokevar=pyjokes.get_joke()
                print(jokevar)
                talk(jokevar)
           
            elif 'weather' in command:
                api_key="d9772b5adc1dab9740024738f4554a86"
                base="https://api.openweathermap.org/data/2.5/weather?"
                city=command.replace("tell me the weather report of",'')
                complete_url = base + "appid=" + api_key + "&q=" + city
                response = requests.get(complete_url)
                x = response.json()
                if x["cod"] != "404":
                    y = x["main"]
                    temperature = int(y["temp"]-273)
                    pressure = y["pressure"]
                    humidity = y["humidity"]
                   
                    z = x["weather"]
 
   
                    description = z[0]["description"]
                    print("the weather report of "+city+" is")
                   
                    print(" Temperature (in celsius)=" +
                    str(temperature) +"°C"
                    "\n atmospheric pressure (in hPa unit) = " +
                    str(pressure) +
                    "\n humidity (in percentage) = " +
                    str(humidity) +"%"
                    "\n description = " +
                    str(description))
                    talk("the weather report of "+city+"  is")
                    talk(" Temperature is " +
                    str(temperature) +"degree celsius"+
                    "\n atmospheric pressure (in hPa unit) is " +
                    str(pressure) +
                    "\n humidity (in percentage) is " +
                    str(humidity) +"%"
                    "\n description is " +
                    str(description))
                    talk("have a nice day!")
                else:
                    talk("oops! coudlnt' find the city")
                    print("cant get the report as the city couldnt be found")
            elif "repeat" in command:
                    rep=command.replace("repeat after me that",'')
                    talk(rep)
            elif "open maps" in command:
                talk("opening maps")
                webbrowser.open("https://www.google.com/maps")
            elif "open youtube" in command:
                talk("openeing youtube")
                webbrowser.open("https://www.youtube.com/")

            elif "calender" in command:
                talk("openeing calender")
                webbrowser.open("https://calendar.google.com/calendar/u/0/r")
            elif "calculate" in command:
                app_id =" AY8KQQ-7UKXP2YGLK"
                client = wolframalpha.Client(app_id)
                indx = command.lower().split().index('calculate')
                query = command.split()[indx + 1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                talk("calculating")
                print ('%.2f'%answer)
                talk("The answer is " + '%.2f'%answer)
            elif "horoscope" in command:
                dic={'Aries':1,'Taurus':2,'Gemini':3,
                'Cancer':4,'Leo':5,'Virgo':6,'Libra':7,
                'Scorpio':8,'Sagittarius':9,'Capricorn':10,
                'Aquarius':11,'Pisces':12} 
      
    # asking for user's input
                talk("mention your zodiac sign from the given list")
                print('Choose your zodiac sign from below list : \n',
                '[Aries,Taurus,Gemini,Cancer,Leo,Virgo,Libra,\
                Scorpio,Sagittarius,Capricorn,Aquarius,Pisces]') 
      
                zodiac_sign = dic[input("Input your zodiac sign : ")]
                talk("tell the day")
                print("On which day you want to know your horoscope ?\n",
                "Yesterday\n", "Today\n", "Tomorrow\n")
                day = input("Input the day : ").lower()
      
                # the data will be sent to the horoscope function
                horoscope_text = horoscope(zodiac_sign, day) 
      
    # then we will simply print the resulting string
                print(horoscope_text) 
                talk(horoscope_text)
            elif "mail" in command:
                try:
                    talk("What are the contents")
                    content = input("enter content of the mail   ")
                    talk("whome should i send")
                    reciever = input("to whom   ")   
                    sendEmail(reciever, content)
                    talk("Email has been sent !")
                except Exception as f:
                    print(f)
                    talk("I am not able to send this email")

  
            else:
                talk(" Please repeat again")
           
    except:
        pass
    return command
# def run_alexa():
#     command=take_command( )

# run_alexa()




if __name__ == "__main__":
 
    root=Tk()
root.title("maria")
root.geometry("520x420")
img=ImageTk.PhotoImage(Image.open('asis.png'))
panel=Label(root, image=img)
panel.pack(side="right",fill="both",expand='no')

usertext=StringVar()
usertext.set("Your Personnel Voice Assistant")
userFrame=LabelFrame(root,text="Maria", font=("Railways",24,"bold"))
userFrame.pack(fill="both",expand="yes")
listbox = Listbox(root,background="blue",width=50)  
    
listbox.insert(1,"•What is the time?")  
listbox.insert(2, "•Play *Song_Name")
listbox.insert(2, "•What is your name?")  
    
listbox.insert(3, "•Who is Sahrukh khan?")  
    
listbox.insert(4, "•Tell me a joke") 

listbox.insert(5, "•Open google ,youtube, maps or calender?")  
listbox.insert(6,"•Tell me the weather reprt of (the city name)")
listbox.insert(7,"•Tell me my horoscope")
listbox.insert(8,"•Make your assistant repeat after you!")
listbox.insert(9,"•Make calculations by speaking calculate the .....")





    
listbox.pack()

top=Message(userFrame,textvariable=usertext, bg="black",fg="white")
top.config(font=("Century Gothic",15,"bold"))
top.pack(side="top",fill="both",expand="yes")
btnsp=Button(root,text="Speak",font=("Railways",15,"bold"),command=take_command,bg="yellow",fg="Black").pack(fill='x', expand="no")

btncl=Button(root,text="Exit",font=("Railways",13,"bold"),command=root.destroy,bg="brown",fg="white").pack(fill='x', expand="no")






 


root.mainloop()