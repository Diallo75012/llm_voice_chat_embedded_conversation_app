import requests
import tempfile
import os
from scipy.io.wavfile import write
import sounddevice as sd
import pyttsx3
import threading
from faster_whisper import WhisperModel
from openai import OpenAI
import json

from datetime import datetime
import pgvector_langchain
from pgvector_langchain import (
  chunk_doc,
  vector_db_create,
  vector_db_retrieve,
  add_document_and_retrieve,
  vector_db_override,
  create_embedding_collection,
  similarity_search,
  MMR_search,
  ollama_embedding,
  answer_retriever
)
 
import time

from dotenv import load_dotenv
from flask import Flask, request
from database import init_db, SessionLocal
from models import PgRecord, ConversationEmbedding
from flask import Flask, request, jsonify

# access to env vars
load_dotenv()
# create flask app
app = Flask(__name__)
# Initialize the database
init_db()
# Openai key
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# Point to the local server
client = OpenAI(base_url="http://localhost:1235/v1", api_key="not-needed")

# Initialize Whisper model and text-to-speech engine
# whisper_model = WhisperModel()
model = "base.en"
whisper_compute_type = "int8"
whisper = WhisperModel(
  model,
  device="auto",
  compute_type=whisper_compute_type
)
tts_engine = pyttsx3.init()
# Set to use a female voice
# tts_engine.setProperty('voice', tts_engine.getProperty('voices')[1].id)
tts_engine.setProperty('voice', 'english+f4') 

### VARS
start_record_word = os.getenv("START_CHAT_KEYWORD")
stop_application_word = os.getenv("STOP_CHAT_APPLICATION_KEYWORD")
connection_string = pgvector_langchain.CONNECTION_STRING
connection_name = pgvector_langchain.CONNECTION_NAME
file_record_to_be_enbedded = os.getenv("FILE_RECORD_TO_BE_EMBEDDED")
stop_app = False

### HELPER FUNCTIONS

"""
# Example function to insert data
def insert_data(question, answer):
    embedding = generate_embedding(question + " " + answer)
    conn = engine.connect()
    conn.execute(vector_data.insert().values(
        unique_identifier=uuid.uuid4(),
        data_vector=embedding,
        other_data=f"Question: {question} Answer: {answer}"
    ))
    conn.close()
"""
def record_audio_to_file(duration=10, sample_rate=44100):
    # Record audio and save to a temporary file.
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    write(temp_file.name, sample_rate, recording)
    return temp_file.name

def transcribe_audio(audio_file):
    # Transcribe speech from an audio file using Faster Whisper.
    result = whisper.transcribe(audio_file)
    print("Transribe audio Result: ", result)
    text = ""
    for segment in result[0]:
        print("Segment: ", segment)
        text += segment.text + " "
    return text

def speak(text):
    # Voice the given text.
    tts_engine.say(text)
    tts_engine.runAndWait()

def query_llm(text, server_url="http://localhost:1235"):
    # Send text to the LLM via LMStudio and get a response.
    response = client.chat.completions.create(
                 model="junko-model",
                 messages=[
                   {"role": "system", "content": "You are providing quick short answers in 30 words max."},
                   {"role": "user", "content": f"{text}"},
                 ],
                 temperature=0.7,
               )

    answer = json.loads(response.json())
    
    return answer['choices'][0]['message']['content']

def continuous_listen():
  global file_record_to_be_enbedded, start_record_word, stop_application_word
    # Listen continuously for the start and stop words.
    while True:
      audio_file = record_audio_to_file(duration=3)
      transcription = transcribe_audio(audio_file)
      os.unlink(audio_file)  # Clean up the temporary file every 3 seconds while waiting for the keyword to be activated

      # keyword to start speech
      if start_record_word in transcription.lower():
        speak("Hello!... I am ready and listening.")
        audio_file = record_audio_to_file(duration=12)
        transcription = transcribe_audio(audio_file)
        os.unlink(audio_file)
        speak("Okay! ...I'll come back to you!")
        response = query_llm(transcription)
        # Write conversation to a file in a structured way
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        to_be_embedded = [
          { 
            "question" : f"{transcription}",
            "answer" : f"{response}",
            "time": f"{now}",
          }
        ]
        # improvement: filename could be variabalized, input or env var
        with open(file_record_to_be_enbedded, "a") as cr:
          cr.append(jsonify(to_be_embedded))
          cr.appen("\n\n") # could be used later on as separator for embeddings chunks "\n\n"
        # answer to user
        speak(response)

      # keyword to stop the application
      elif stop_application_word in transcription.lower():
        speak("Stop word detected. Goodbye! The background process is still recording, the application will stop when it is done. .... See You Next Time!")
        stop_app = True
        last_embedding = process_embeddings_periodically(collection_name, connection_string)
        if last_embedding == "stop":
          break


# when the app stops the job stops
def process_embeddings_periodically(collection_name, connection_string):
  global collection_name, connection_string, file_record_to_be_enbedded, stop_app
  # after 2.5mn it starts embedding the recorded conversations
  time.sleep(150)
  all_docs = chunk_doc("/home/creditizens/voice_llm", [file_record_to_be_enbedded,]) # list_documents_txt
  if stop_app == True:
    create_embedding_collection(all_docs, collection_name, connection_string)
    print("Last record embedded, application will stop now!")
    return "stop"
  else:
    # add fetching data to save to database and then in the while loop when the embedding is done, delete the record completely
    while True:
      # Placeholder for your logic to read Q/A data, generate embeddings, and store them
      create_embedding_collection(all_docs, collection_name, connection_string)
      print("Processing embeddings...")
      # Wait for 2mn before next run
      time.sleep(120)
 

# can make flask route to retrieve answers best answers from questions, it returns a dictionary with the question and the answer, which could be used as jinja context for html display
# text_query = "What is the the most populated city in Asia?"
# answer_retriever(text_query, collection_name, connection_string, embeddings)

if __name__ == "__main__":
    speak("I am ready to chat.")
    # run in the background for periodic embeddings
    embeddings_thread = threading.Thread(target=process_embeddings_periodically, daemon=True)
    embeddings_thread.start()
    # run as main thread in front which is the app llm vocal chat
    continuous_listen()

    




