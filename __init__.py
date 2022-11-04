from mycroft import MycroftSkill, intent_file_handler
from mycroft.audio import wait_while_speaking
from mycroft.messagebus.message import Message
import RPi.GPIO as GPIO

class PicroftMuteSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    muted = False

    def initialize(self):
        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed(False)

    def shutdown(self):
        self.log.info("Performing shutdown....")
        self.bus.emit(Message('mycroft.volume.unmute', data={"speak_message": False})) # Turn the volume back on if shutdown
        self.cleanupGPIO()

    def on_settings_changed(self, doCleanup = True):
        self.log.info(f"Settings changed! \n\t{self.settings}")

        self.led_pin = self.settings.get('led_pin')
        self.button_pin = self.settings.get('button_pin')

        if doCleanup:
            self.cleanupGPIO()

        self.initGPIO()

        self.led_mute_behavior = self.settings.get('led_mute_behavior')
        self.set_led_state()

    def initGPIO(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.led_pin, GPIO.OUT) # set up LED pin
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # set up button event handler
        GPIO.add_event_detect(self.button_pin, GPIO.BOTH, self.handle_button_press)

    def cleanupGPIO(self):
        GPIO.remove_event_detect(self.button_pin) # remove button event handler
        GPIO.cleanup()

    @intent_file_handler('mute.intent')
    def handle_mute_picroft(self, message):
        if not self.muted:
            # NOTE: for a toggle button, using the "mute.intent" voice command means that the button will have to be pressed twice to unmute
            # (once to "align" the button state with the mute state, then again to change the mute state)
            self.muted = True
            self.handle_mute()

    def handle_mute(self):
        self.set_led_state()            
        self.speak_dialog("muted")
        wait_while_speaking()
        self.bus.emit(Message('mycroft.volume.mute', data={"speak_message": False})) # This has to come after the speak_dialog line for the speak_dialog to be heard

    def handle_unmute(self):
        self.set_led_state()
        self.speak_dialog("unmuted")
        self.bus.emit(Message('mycroft.volume.unmute', data={"speak_message": False}))

    def set_led_state(self):
        if ((self.muted and self.led_mute_behavior == 'muted') or
           (not self.muted and self.led_mute_behavior == 'unmuted')):
            GPIO.output(self.led_pin, GPIO.HIGH) # Turn on LED
        else:
            GPIO.output(self.led_pin, GPIO.LOW) # Turn off LED

    def handle_button_press(self, channel):
        self.log.info(f"handling button press (pin {channel}: {GPIO.input(channel)}). muted: {self.muted}")
        # TODO: this code assumes a "toggle button" right now and should be changed to also be compatible with a push button
        if GPIO.input(channel) == GPIO.HIGH and not self.muted:
            self.muted = True
            self.handle_mute()
        elif GPIO.input(channel) == GPIO.LOW and self.muted:
            self.muted = False
            self.handle_unmute()

def create_skill():
    return PicroftMuteSkill()