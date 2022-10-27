from mycroft import MycroftSkill, intent_file_handler
from mycroft.audio import wait_while_speaking
from mycroft.messagebus.message import Message
import RPi.GPIO as GPIO

class PicroftMuteSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT) # set up LED pin # TODO: allow this pin # to be customized
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # set up button event handler # TODO: allow this pin # to be customized
        GPIO.add_event_detect(10, GPIO.BOTH, self.handle_button_press)

    def shutdown(self):
        self.log.info("Performing shutdown....")
        GPIO.remove_event_detect(10) # remove button event handler
        GPIO.cleanup() # TODO: currently I don't think this is cleaning up previous event handlers

    muted = False

    @intent_file_handler('mute.intent')
    def handle_mute_picroft(self, message):
        if not self.muted:
            # NOTE: for a toggle button, using the "mute.intent" voice command means that the button will have to be pressed twice to unmute
            # (once to "align" the button state with the mute state, then again to change the mute state)
            self.muted = True
            self.handle_mute()

    def handle_mute(self):
        GPIO.output(12, GPIO.HIGH) # Turn on LED
        self.speak_dialog("muted")
        wait_while_speaking()
        self.bus.emit(Message('mycroft.volume.mute', data={"speak_message": False})) # This has to come after the speak_dialog line for the speak_dialog to be heard

    def handle_unmute(self):
        GPIO.output(12, GPIO.LOW) # Turn off LED
        self.speak_dialog("unmuted")
        self.bus.emit(Message('mycroft.volume.unmute', data={"speak_message": False}))

    def handle_button_press(self, channel):
        self.log.info(f"handling button press (pin {channel}: {GPIO.input(channel)}). muted: {self.muted}")
        # NOTE: this code assumes a "toggle button" right now and should be changed to also be compatible with a push button
        if GPIO.input(channel) == GPIO.HIGH and not self.muted:
            self.muted = True
            self.handle_mute()
        elif GPIO.input(channel) == GPIO.LOW and self.muted:
            self.muted = False
            self.handle_unmute()

def create_skill():
    return PicroftMuteSkill()

# import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
# import subprocess
# import os
# import time

# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
# GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

# def runAndPrint(command):
#     print(command)
#     p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#     (stdout, stderr) = p.communicate()

#     exitcode = p.wait()

#     if stdout != None:
#         stdout = stdout.decode()
    
#     if stderr != None:
#         stderr = stderr.decode()

#     return stdout, stderr, exitcode

# def runRecordLoop():
#     runAndPrint('espeak "Record what you want to say"')
#     stdout, stderr, exitcode = runAndPrint('arecord -D hw:2,0 -d 3 -f cd test.wav -c 1')

#     if 'Invalid value for card' in stderr:
#         runAndPrint('espeak "there was an error recording"')
#         return

#     runAndPrint('aplay test.wav')

#     if os.path.exists('test.wav'):
#         os.remove('test.wav')

# runAndPrint('espeak "I am ready"')
# button_state = GPIO.input(10) == GPIO.HIGH
# while True:
#     if GPIO.input(10) == GPIO.HIGH and not button_state:
#         runAndPrint('espeak "Button was pushed!"')
#         runAndPrint('sudo uhubctl -a on -p 1 -l 1-1')
#         time.sleep(10) # Allow mic time to "boot back up" (avoid "device or resource busy" issues)
#         runRecordLoop()
#         button_state = True
#     elif GPIO.input(10) == GPIO.LOW and button_state:
#         runAndPrint('espeak "Button was unpushed!"')
#         runAndPrint('sudo uhubctl -a off -p 1 -l 1-1')
#         runRecordLoop()
#         button_state = False
