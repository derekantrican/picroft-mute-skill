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