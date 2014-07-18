__author__ = 'SolarLune'

import os
import random

import aud
from bge import logic


class CAudioDevice():
    def __init__(self, sound_folder='//assets/snd/'):

        self.device = aud.device()

        if not sound_folder.endswith("/"):
            sound_folder += "/"  # Make sure there's a trailing slash for sound files to go

        self.sound_folder = logic.expandPath(sound_folder)

        self.sounds = {}

        for snd_info in os.walk(self.sound_folder):

            for f in snd_info[2]:
                filename = os.path.splitext(f)[0]

                self.sounds[filename] = aud.Factory(self.sound_folder + f)

        self.current_bgm_handle = None
        self.current_bgm = None

    def play_bgm(self, bgm, loop=1):

        if bgm != self.current_bgm:
            self.current_bgm = bgm
            self.current_bgm_handle = self.device.play(self.sounds[bgm])
            self.current_bgm_handle.loop_count = -1
            self.current_bgm_handle.volume = logic.settings['bgm_vol']
            return self.current_bgm_handle

        return None

    def stop_bgm(self):

        if self.current_bgm is not None:
            self.current_bgm = None
            self.current_bgm_handle.stop()

    def play_sound(self, sound, volume_var=0.1, pitch_var=.1):
        handle = self.device.play(self.sounds[sound])
        handle.volume += random.uniform(-volume_var, volume_var)
        handle.volume *= logic.settings['sound_vol']
        handle.pitch += random.uniform(-pitch_var, pitch_var)
        return handle

    def get_bgm_handle(self):

        return self.current_bgm_handle


device = CAudioDevice()