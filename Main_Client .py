import queue
from pydub import AudioSegment
from pydub.playback import play
from clientComm import ClientComm
import socket

# connect to the main server:
# msg_q = queue.Queue()
# client_comm = ClientComm("127.0.0.1", 8080, msg_q)
# flag = client_comm.connected
#
# while not flag:
#     flag = client_comm.connected
#
# flag = False


# NEEDED FUNCTIONS
# ----------------->
# -------------------------->


def register(password, username):
    """
    :return:
    """
    pass


def login(password, username):
    """
    :return:
    """
    pass


def download_song(song_name):
    """
    :return:
    """


def p2p_Request_download(peer_ip, file_name):
    """
    :return:
    """


def Monitor_path(file_path):
    """
    :return:
    """
    pass


def like_dislike_song(song_name):
    """
    :return:
    """


def lookup_song(song_artist_name):
    """
    :return:
    """
    pass


def play_song(song_name):
    """
    :return: play song
    """
    song = AudioSegment.from_wav(song_name+".wav")
    play(song)
    pass


def handle_income_msgs(msg_q):
    """
    :return:
    """
    pass


def main():
    """
    :return:
    """
    play_song(r"C:\Users\97254\Downloads\Lana.mp3")

