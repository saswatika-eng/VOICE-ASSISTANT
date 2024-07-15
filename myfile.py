from __future__ import print_function
import warnings
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import datetime
import calendar
import random
import wikipedia
import os   
import json       
import playsound
import webbrowser  
import pyjokes
import requests

warnings.filterwarnings("ignore")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(audio):
    engine.say(audio)
    engine.runAndWait()

def rec_audio():
    recog = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recog.listen(source)

    data = " "
    try:
        data = recog.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Assistant could not understand the audio.")
    except sr.RequestError as ex:
        print("Request error from Google Speech Recognition" + ex)

    return data

def response(text):
    print(text)
    tts = gTTS(text=text, lang="en")
    audio = "Audio.mp3"
    tts.save(audio)
    playsound.playsound(audio)
    os.remove(audio)

def call(text):
    action_call = "assistant"

    text = text.lower()

    if action_call in text:
        return True
    

    return False

def today_date():
    now = datetime.datetime.now()
    date_now = datetime.datetime.today()
    week_now = calendar.day_name[date_now.weekday()]
    month_now = now.month
    day_now = now.day

    months = [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ] 
    ordinals = [
        "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th",
        "11th", "12th", "13th", "14th", "15th", "16th", "17th", "18th",
        "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th",
        "27th", "28th", "29th", "30th", "31st"
    ]

    return "Today is " + week_now + ", " + months[month_now - 1] + " the " + ordinals[day_now - 1] + "."
    
def say_hello(text):
    greet = ["hi", "hey", "hola", "greetings", "wassup", "hello"]

    response = ["howdy", "whats good", "hello", "hey there"]

    for word in text.split():
        if word.lower() in greet:
            return random.choice(response) + "."
        
    return ""

def wiki_person(text):
    list_wiki = text.split()
    for i in range(0, len(list_wiki)):
        if i + 3 <= len(list_wiki) - 1 and list_wiki[i].lower() == "who" and list_wiki[i + 1].lower() == "is":
            return list_wiki[i + 2] + " " + list_wiki[i + 3]


def assistant(data):
    global response
    if "how are you" in data:
        listening = True
        response("I am well")

    elif "time" in data:
        listening = True
        now = datetime.datetime.now()
        meridiem = ""
        if now.hour >= 12:
            meridiem = "p.m"
            hour = now.hour - 12
        else:
            meridiem = "a.m"
            hour = now.hour

        if now.minute < 10:
            minute = "0" + str(now.minute)
        else:
            minute = str(now.minute)

        response("It is " + str(hour) + ":" + minute + " " + meridiem + " .")

    elif "date" in data:
        listening = True
        get_date = today_date()
        response(get_date)

    elif "who are you" in data or "define yourself" in data:
        listening = True
        response("Hello, I am Person. Your personal Assistant. I am here to make your life easier.You can command me to perform various tasks such as calculating sums or opening applications etcetera")

    elif "your name" in data:
        listening = True
        response("My name is Person.")

    elif "who am I" in data:
        listening = True
        response("You must probably be a human.")

    elif "why do you exist" in data or "why did you come" in data:
        listening = True
        response("It is a secret")

    elif "who created you" in data or "who made you" in data:
        listening = True
        response("I have been created by Saswatika.")

    elif "favourite colour" in data or "favorite color" in data:
        listening = True
        response("My favourite colour is blue.")


    elif "weather" in data:
        listening = True
        api_key = "enter api key"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        response("Please tell me the city name")
        city_name = rec_audio()
        complete_url = base_url + "q=" + city_name + "&appid=" + api_key
        response(complete_url)
        weather_response = requests.get(complete_url)
        x = weather_response.json()

        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"] 
            weather_description = z[0]["description"]
            response("Temperature in Kelvin: " +
                     str(current_temperature) +
                     "\nAtmospheric pressure (hPa): " +
                     str(current_pressure) +
                     "\nHumidity (%): " +
                     str(current_humidity) +
                     "\nDescription: " +
                     str(weather_description))
        else:
            response("City Not Found")
            
    elif "what is the weather in" in data:
        key = "enter api key"
        weather_url = "https://api.openweathermap.org/data/2.5/weather?"
        ind = data.split().index("in")
        location = data.split()[ind + 1:]
        location = " ".join(location)
        url = weather_url + "appid=" + key + "&q=" + location
        js = requests.get(url).json()
        if js["cod"] != "404":
            weather = js["main"]
            temperature = weather["temp"]
            temperature = temperature - 273.15
            humidity = weather["humidity"]
            desc = js["weather"][0]["description"]
            weather_response = " The temperature in Celsius is " + str(temperature) + " The humidity is " + str(humidity) + " and the weather description is " + str(desc)
            response(weather_response)
        else:
            response("City Not Found")


    elif "open" in data.lower():
        listening = True
        if "chrome" in data.lower():
            response ="Opening Google Chrome"
            os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        elif "excel" in data.lower():
            response = "Opening Microsoft Excel"
            os.startfile(
                r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"
            )
        elif "vs code" in data.lower():
            response = "Opening visual studio code"
            os.startfile(
                         r"C:\Users\Acer\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        elif "youtube" in data.lower():
            response = "Opening youtube"
            webbrowser.open(
                r"https://youtube.com/"
            )
        elif "google" in data.lower():
            response = "Opening google"
            webbrowser.open(
                r"https://google.com"
            )

        else:
            response("Application not available")
        print(response)

    elif "youtube" in data.lower():
        ind = data.lower().split().index("youtube")
        search = data.split()[ind + 1:]
        webbrowser.open(
                    "http://www.youtube.com/results?search_query=" +
                    "+".join(search)
                )
        response = "Opening " + " ".join(search) + " on youtube"
        print(response)

    elif "search" in data.lower():
        ind = data.lower().split().index("search")
        search = data.split()[ind + 1:]
        webbrowser.open(
                    "https://www.google.com/search?q=" + "+".join(search)

                )
        response = "Searching " + " ".join(search) + " on google"
        print(response)

    elif "google" in data.lower():
        ind = data.lower().split().index("google")
        search = data.split()[ind + 1:]
        webbrowser.open(
                    "https://www.google.com/search?q=" + "+".join(search)
                )
        response = "Searching " + " ".join(search) + " on google" 
        print(response)


    elif "wikipedia" in data or "Wikipedia" in data:
        listening = True
        response("Checking the wikipedia ")
        data = data.split(" ")
        data = " ".join(data[2:])
        try:
            wiki_data = wikipedia.summary(data, sentences=3)
            response("According to Wikipedia")
            response(wiki_data)
        except:
            response("Can't find the relevant data on wikipedia")


    elif "news" in data:
        listening = True
        news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
        response("Here are some headlines from the Times of India, Happy reading")

    elif "search" in data:
        listening = True
        data = data.split(" ")
        data = " ".join(data[1:])
        webbrowser.open_new_tab(data)

    elif "joke" in data:
        listening = True
        response(pyjokes.get_joke())

    return listening



if __name__ == "__main__":
    response("Hi, I am Person. What can I do for you?")
    listening = True
    while listening == True:
        data = rec_audio()
        listening = assistant(data)

