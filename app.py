import openai
import speech_recognition as sr
import whisper
import pyttsx3


def generate_answer(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  ##
        messages=messages,
        max_tokens=1000,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]


def talk(text):
    engine.say(text)
    engine.runAndWait()
    engine.stop()


openai.api_key = "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"
r = sr.Recognizer()
mic = sr.Microphone()
model = whisper.load_model("base")
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 360)
engine.setProperty('voice', voices[0].id)
mensagens = [{"role": "system", "content": "Você é uma assistente simpática, vou te chamar de Joana. E meu nome é Tiago!"}]
adjust_ambient = True
while True:
    text = ""
    question = ""
    with mic as font:
        if adjust_ambient:
            r.adjust_for_ambient_noise(font)
            adjust_ambient = False
        print("Fale alguma coisa!")
        audio = r.listen(font)
        print("Enviando para reconhecimento!")
        question = r.recognize_google(audio, language="pt-BR")
    if ("esligar" in question) or question.startswith("sair"):
        print(question, "Saindo...")
        talk("Desligando...")
        break
    elif question == "":
        print("Sem som!")
        continue
    else:
        print("Você:", question)
        mensagens.append({"role": "user", "content": str(question)})
        answer = generate_answer(mensagens)
        print("Joana:", answer[0])
        mensagens.append({"role": "assistant", "content": answer[0]})
        talk(answer[0])
print("Até a próxima!")
