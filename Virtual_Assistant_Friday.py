import pyttsx3
import datetime 
import speech_recognition as sr
import webbrowser as wb
import os
import openai

# Cài đặt API key của bạn
openai.api_key = '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'

def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine='davinci',  # Tên mô hình GPT bạn muốn sử dụng
        prompt=prompt,
        max_tokens=5000,  # Số lượng từ tối đa trong câu trả lời từ GPT
        temperature=1.0,  # Độ đa dạng của câu trả lời từ GPT (0.2-1.0)
        n=100,  # Số lượng câu trả lời bạn muốn nhận từ GPT
        stop=None,  # Chuỗi ký tự để dừng việc sinh câu trả lời từ GPT (tùy chọn)
        timeout=50  # Thời gian tối đa để gửi câu hỏi tới GPT và nhận câu trả lời
    )

    if 'choices' in response and len(response['choices']) > 0:
        answer = response['choices'][0]['text'].strip()
        return answer

    return None

friday=pyttsx3.init()
voices = friday.getProperty('voices')
friday.setProperty('voice', voices[1].id) 

def speak(audio):
    print('F.R.I.D.A.Y: ' + audio)
    friday.say(audio)
    friday.runAndWait()
   
    
def time():
    Time=datetime.datetime.now().strftime("%I:%M:%p") 
    speak("It is")
    speak(Time)

def welcome():
        #Chao hoi
        hour=datetime.datetime.now().hour
        if hour >= 6 and hour<12:
            speak("Good Morning Sir!")
        elif hour>=12 and hour<18:
            speak("Good Afternoon Sir!")
        elif hour>=18 and hour<24:
            speak("Good Evening sir")
        speak("How can I help you,boss") 


def command():
    c=sr.Recognizer()
    with sr.Microphone() as source:
        c.pause_threshold=2
        audio=c.listen(source)
    try:
        query = c.recognize_google(audio,language='en-US')
        print("Tony Lèo: "+query)
    except sr.UnknownValueError:
        print('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Your order is: '))
    return query

if __name__  =="__main__":
    welcome()

    while True:
        query=command().lower()
        #All the command will store in lower case for easy recognition
        if "google" in query:
            speak("What should I search,boss")
            search=command().lower()
            url = f"https://google.com/search?q={search}"
            wb.get().open(url)
            speak(f'Here is your {search} on google')
        
        elif "youtube" in query:
            speak("What should I search,boss")
            search=command().lower()
            url = f"https://youtube.com/search?q={search}"
            wb.get().open(url)
            speak(f'Here is your {search} on youtube')

        elif "quit" in query:
            speak("Friday is off. Goodbye boss")
            quit()
        elif "open video" in query:
            meme =r"C:\Users\Admin\Desktop\test\meme.mp4"
            os.startfile(meme)
        elif 'time' in query:
            time()
        else:
            # Gửi câu hỏi từ người dùng tới GPT và nhận câu trả lời
            response = chat_with_gpt(query)
            if response:
                speak(response)
            else:
                speak("I'm sorry, I don't know the answer. Would you like to teach me?")
                teach = command().lower()
                if 'yes' in teach:
                    speak("Please provide me with the answer.")
                    answer = command()