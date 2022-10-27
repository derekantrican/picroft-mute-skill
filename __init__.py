from mycroft import MycroftSkill, intent_file_handler


class PicroftMute(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('mute.picroft.intent')
    def handle_mute_picroft(self, message):
        self.speak_dialog('mute.picroft')


def create_skill():
    return PicroftMute()

