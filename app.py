import random
import pyttsx3
import speech_recognition as sr
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def text_to_speech(text, language='en', voice_gender='f'):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Select voice based on language and gender
    if language == 'ta':
        if voice_gender == 'm':
            voice_id = 'ta+m1'  # Replace with the desired Tamil male voice ID
        else:
            voice_id = 'ta+f1'  # Replace with the desired Tamil female voice ID
    elif language == 'hi':
        if voice_gender == 'm':
            voice_id = 'hi+m1'  # Replace with the desired Hindi male voice ID
        else:
            voice_id = 'hi+f1'  # Replace with the desired Hindi female voice ID
    else:
        if voice_gender == 'm':
            voice_id = 'en+m3'  # Replace with the desired English male voice ID
        else:
            voice_id = 'en+f3'  # Replace with the desired English female voice ID

    # Set the selected voice
    selected_voice = None
    for voice in voices:
        if voice_id in voice.id:
            selected_voice = voice
            break

    if selected_voice:
        engine.setProperty('voice', selected_voice.id)
    else:
        print(f"Voice not found for voice ID: {voice_id}. Using the default voice.")

    engine.setProperty('rate', 150)  # You can adjust the speech rate here
    engine.say(text)
    engine.runAndWait()


def process_query():
    continue_playing = True
    language_choice = ''
    voice_gender = ''

    while continue_playing:
        r = sr.Recognizer()

        if not language_choice:
            # Language selection
            text_to_speech("Select a language (English, Tamil, Hindi):")
            with sr.Microphone() as source:
                audio = r.listen(source)

            try:
                language_choice = r.recognize_google(audio)
                if language_choice.lower() not in ["en", "ta", "hi"]:
                    language_choice = 'en'
            except sr.UnknownValueError:
                continue

        if not voice_gender:
            # Voice gender selection
            text_to_speech("Select a voice gender (male or female):")
            with sr.Microphone() as source:
                audio = r.listen(source)

            try:
                voice_gender = r.recognize_google(audio)
            except sr.UnknownValueError:
                continue

        text_to_speech("Now you can ask queries.")

        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            question = r.recognize_google(audio)
        except sr.UnknownValueError:
            continue

        if question.lower() == "exit":
            break
        else:
            if "college fees" in question.lower():
                response = "The college fees for Bannari Amman Institute of Technology depend on the course the student has selected."
            elif "campus review" in question.lower():
                response = "Bannari Amman Institute of Technology has a sprawling campus with state-of-the-art facilities. The campus provides a conducive environment for learning and offers various amenities to students."
            elif "testimonials" in question.lower():
                response = "Bannari Amman Institute of Technology has received positive testimonials from many students and alumni. They appreciate the quality of education, supportive faculty, and the opportunities provided for overall development."
            elif "ratings" in question.lower():
                response = "BIT has been rated highly by various ranking agencies and students. It is known for its academic excellence, infrastructure, and placement opportunities."
            elif "achievements" in question.lower():
                response = "Bannari Amman Institute of Technology has achieved several accolades in the field of technical education. They have excelled in areas like research, innovation, and industry collaborations."
            elif "nirf ranking" in question.lower():
                response = "As of my knowledge cutoff in September 2021, Bannari Amman Institute of Technology was ranked among the top engineering institutes in India by the National Institutional Ranking Framework (NIRF). For the latest ranking information, I recommend checking the NIRF official website."
            elif "infrastructure" in question.lower():
                response = "BIT boasts a modern infrastructure with well-equipped laboratories, libraries, sports facilities, hostels, and more. The campus provides a comfortable and conducive environment for learning and extracurricular activities."
            elif "location" in question.lower():
                response = "Bannari Amman Institute of Technology is located in Sathyamangalam, Erode district, Tamil Nadu, India. The campus is situated in a serene and scenic environment, offering a peaceful atmosphere for students."
            else:
                response = "I'm sorry, I don't have the ability to answer that question yet."

            text_to_speech(response, language_choice, voice_gender)

        while True:
            text_to_speech("Do you have any other queries? Say 'yes' or 'no'.")
            with sr.Microphone() as source:
                audio = r.listen(source)

            try:
                next_question = r.recognize_google(audio)

                if next_question.lower() == "yes":
                    break
                elif next_question.lower() == "no":
                    continue_playing = False
                    break
            except sr.UnknownValueError:
                continue

    text_to_speech("Thank you for using the query system. Goodbye!")
    return redirect('/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    return process_query()

if __name__ == '__main__':
    app.run(debug=True)

