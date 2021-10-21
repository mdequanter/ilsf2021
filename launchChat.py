import time
import os
import pygame
import paho.mqtt.client as mqttclient

pygame.init()
gameDisplay = pygame.display.set_mode((1280,400))
pygame.display.set_caption('Naov6 Control')
clock = pygame.time.Clock()

lastMessage =  ""

black = (0,0,0)
white = (255,255,255)

dutch = pygame.image.load('button1.png')
french = pygame.image.load('button2.png')
nao = pygame.image.load('nao.png')

running = False

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_message(clientScreen, userdata, message):
    global running
    content = message.payload
    topic =  message.topic
    print("message topic=",topic)
    print("message received ", content)

    if (topic == "ENDED") :
        running = False




broker = "localhost"


clientScreen=mqttclient.Client("ClientScreen")
clientScreen.on_publish = on_publish
clientScreen.connect(broker)
clientScreen.on_message=on_message #attach function to callback
clientScreen.subscribe("ENDED")
clientScreen.loop_start() #start the loop
crashed = False

def publishTask(topic,message):
    global lastMessage,input_stream

    if (message!=lastMessage) :
        ret = clientScreen.publish(topic, message)
        lastMessage = message



while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        posDutch = 50
        posFrench = 50

        #print(event)

        gameDisplay.fill(white)

        if event.type == pygame.FINGERDOWN:
            if (event.x < 0.3) :
                if (running == False) :
                    print ("Start NL")
                    posDutch = 55
                    pygame.display.update()
                    os.system("python chatbot_microphone_to_text.py --language-code NL")
                    running = True
            if (event.x > 0.3 and event.x < 0.6) :
                if (running == False) :
                    print ("Start FR")
                    posFrench = 55
                    pygame.display.update()
                    os.system("python chatbot_microphone_to_text.py --language-code FR")
                    running = True
            if (event.x > 0.6 ):
                print("Rest")
                publishTask("MOTION", "REST")
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = event.pos[0]
            if (position < 350) :
                if (running == False) :
                    print ("Start NL")
                    posDutch = 55
                    pygame.display.update()
                    os.system("python chatbot_microphone_to_text.py --language-code NL")
                    running = True
            if (position > 400 and  position < 800) :
                if (running == False) :
                    print ("Start FR")
                    posFrench = 55
                    pygame.display.update()
                    os.system("python chatbot_microphone_to_text.py --language-code FR")
                    running = True

            if (position > 800) :
                print ("Rest")
                publishTask("MOTION", "REST")
                running = False
                pygame.display.update()



        gameDisplay.blit(dutch, (50, posDutch))
        gameDisplay.blit(french, (400, posFrench))
        gameDisplay.blit(nao, (800, 0))


    pygame.display.update()
