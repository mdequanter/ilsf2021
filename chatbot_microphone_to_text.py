"""Dialogflow API streams user input through the microphone and
speaks voice responses through the speaker.
Examples:
  python mic_stream_audio_response.py
  python mic_stream_audio_response.py--project-id PROJECT_ID
"""
from google.cloud import dialogflow_v2 as dialogflow
import pyaudio
import simpleaudio as sa
import argparse
import uuid
import paho.mqtt.client as mqttclient
import time
import re

selectedLang = "NL"
maxTime = 90
askedToLeave = False
endTalk = False

timer = time.time()



def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass


# Audio recording parameters
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)
PROJECT_ID = "chatbot-ilsf"
SESSION_ID = "123456789"

broker = "localhost"

client1 = mqttclient.Client("Nao1")
client1.on_publish = on_publish
client1.connect(broker)
client1.loop_start() #start the loop

import paho.mqtt.client as mqttclient


lastMessage =  ""

input_stream = ""


def publishTask(topic,message):
    global lastMessage,input_stream

    if (message!=lastMessage) :
        ret = client1.publish(topic, message)
        lastMessage = message


def grab_intent(projectId, sessionId, languageCode):
    """Start stream from microphone input to dialogflow API"""
    global selectedLang, endTalk,askedToLeave
    selectedLang = languageCode

    session_client = dialogflow.SessionsClient()
    # Audio output stream

    final_request_received = False

    def __request_generator():
        global input_stream, selectedLang, endTalk,maxTime

        if (endTalk == False) :

            input_stream = pyaudio.PyAudio().open(channels=1,
                                                  rate=SAMPLE_RATE, format=pyaudio.paInt16, input=True)

            session_path = session_client.session_path(projectId, sessionId)
            print('Session path: {}\n'.format(session_path))
            input_audio_config = dialogflow.types.InputAudioConfig(audio_encoding=1,
                                                                   language_code=languageCode,
                                                                   sample_rate_hertz=SAMPLE_RATE)
            print("========+=====")
            #print ("sleeping 3 seconds")
            #time.sleep(3)

            query_input = dialogflow.types.QueryInput(
                audio_config=input_audio_config)

            # The first request contains the configuration.
            yield dialogflow.types.StreamingDetectIntentRequest(
                session=session_path, query_input=query_input)

            while (endTalk == False):
                if final_request_received is True:
                    print("received final request")
                    print("closed stream")
                    return
                if input_stream.is_active():
                    content = input_stream.read(
                        CHUNK_SIZE, exception_on_overflow=False)
                    yield dialogflow.types.StreamingDetectIntentRequest(input_audio=content)

    while True:
        requests = __request_generator()
        responses = session_client.streaming_detect_intent(requests)

        if ((time.time() - timer) > maxTime):
            if (askedToLeave == False) :
                if (selectedLang == "FR"):
                    publishTask("EARLEDS", "OFF")
                    publishTask("SAY",
                                "Je vais devoir te dire au revoir, car mon collegue vous attend.  Pouvez-vous passer à l'un de mes collegues ?")
                    publishTask("MOTION", "REST")
                    final_request_received = True
                    endTalk = True
                    time.sleep(20)
                    exit()

                if (selectedLang == "NL"):
                    publishTask("EARLEDS", "OFF")
                    publishTask("SAY",
                                "Ik zal je moeten laten,  want mijn collega is aan het wachten op jou.  Kan je doorlopen naar één van mijn collega's?")
                    final_request_received = True
                    publishTask("MOTION", "REST")
                    endTalk = True
                    time.sleep(20)
                    exit()
                askedToLeave = True

        for response in responses:
            print(
                f'Intermediate transcription result: {response.recognition_result.transcript}')
            if response.recognition_result.is_final:
                final_request_received = True
            if response.query_result.query_text:
                fulfillment_text = response.query_result.fulfillment_text
                print(
                    f'Response: {response.query_result.fulfillment_text}')
                publishTask("EARLEDS", "OFF")
                publishTask("SAY", response.query_result.fulfillment_text)
                charsCount = len(response.query_result.fulfillment_text)
                print ("charakters: " + str(charsCount))
                timeWait = charsCount / 15
                time.sleep(timeWait)
                if re.search(r"\b(tot ziens|veel plezier|Veel plezier|mijn collega|Salut|Au revoir)\b", response.query_result.fulfillment_text, re.I):
                    print ("veel plezier detected")
                    publishTask("EARLEDS", "OFF")
                    time.sleep(1)
                    publishTask("MOTION", "REST")
                    time.sleep(1)
                    publishTask("ENDED", "1")
                    exit()

                publishTask("EARLEDS","ON")
                final_request_received = False

def play_audio(audio):
    audio_obj = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
    audio_obj.wait_done()


Listening  = False

def main():
    global endTalk
    publishTask("POSTURE", "Stand")
    while(endTalk == False):
        response = grab_intent(
            PROJECT_ID, SESSION_ID, args.language_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--language-code',
        help='Language code of the query. Defaults to "fr".',
        default='fr')

    args = parser.parse_args()
    publishTask("EARLEDS", "OFF")
    publishTask("LANGUAGE",args.language_code)
    if (args.language_code=="NL") :
        publishTask("SAY",
                    "Hallo, welkom.  Van zodra mijn ogen oplichten, mag je me alles vragen over onze activiteiten.  Wat wil je weten?")
    if (args.language_code=="FR") :
        publishTask("SAY",
                    "Bonjour, bienvenue.  Dès que mes yeux s'allument, tu peux me demander n'importe quoi sur nos activités.  Que veux-tu savoir ?")
    time.sleep(10)
    publishTask("EARLEDS", "ON")
    main()
