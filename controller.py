# This is the program that will handle the controller input
import RPi.GPIO as GPIO
import pygame as pg
from threading import Thread
from time import sleep

class Controller():
    def __init__(self):
        self.buttons = [17, 18]

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buttons, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        listener = Thread(target=self.listen)
        listener.start()

    def listen(self):
        #BUTTON_DOWN = pg.event.custom_type() 

        while True:
            for i in range(len(self.buttons)):
                if GPIO.input(self.buttons[i]) == True:
                    print("PRESSED")
                    #match self.buttons[i]:             # upgrade python installation on pi
                        #case 17:                       # bc this is faster
                    if self.buttons[i] == 17:
                        pg.event.post(pg.event.Event(pg.KEYDOWN, {'key': pg.K_LEFT}))
                        sleep(0.1)  # avoid event flooding
                    if self.buttons[i] == 18:
                        pg.event.post(pg.event.Event(pg.KEYDOWN, {'key': pg.K_RIGHT}))
                        sleep(0.1)
                

def main():
    c = Controller()
    pg.init()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            else:
                print(event)
    exit()


if __name__ == "__main__":
    main()