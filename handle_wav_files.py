# this file is responsible for the following:
# 1) playing a song
# 2) converting a song from mp3 to wav


import os
import pickle
import socket

import pyaudio
import queue
import struct
import wave
from pydub import AudioSegment
from pydub.playback import play
from clientComm import ClientComm


def convert_to_wav(mp3_path, song_name, hidden_file_path):
    # files
    dst = f"{hidden_file_path}{song_name}.wav"
    can_covert = False
    if os.path.exists(mp3_path):
        # convert wav to mp3
        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(dst, format="wav")
        can_covert = True
    return can_covert


def play_song(song_file):
    sound = AudioSegment.from_wav(song_file)
    play(sound)


def audio_stream(song_path):
    msg_q = queue.Queue()
    client_com = ClientComm("127.0.0.1", 1000, msg_q)

    CHUNK = 1024
    wf = wave.open(song_path, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    data = None
    while True:
        data = wf.readframes(CHUNK)
        a = pickle.dumps(data)
        message = struct.pack("Q", len(a)) + a
        client_com.send(message)


def send_song_data(song_path):
    """
    :return:
    """
    (HOST, PORT) = ('localhost', 19123)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.connect((HOST, PORT))

    with open(song_path, 'rb') as f:
        for l in f: s.sendall(l)
    s.close()


if __name__ == '__main__':

    song_name = "Lana"
    hidden_file_path = os.getcwd() + "\\songPath_Listen_Together\\"
    path_song_folder = os.getcwd() + "\\songPath_Listen_Together\\" + song_name + ".mp3"

    # convert_to_wav(path_song_folder, song_name, hidden_file_path)
    song_path = os.getcwd() + "\\song_trasfered" + ".wav"
    play_song(song_path)
    # send_song_data(song_path)
