import hashlib
from serverComm import ServerComm
import queue

to_find = "EC9C0F7EDCC18A98B1F31853B1813301"  # string to find

# Create a line of messages:
msg_q = queue.Queue()
# make server connection
server_comm = ServerComm(8080, msg_q)
to_send_q = queue.Queue()

curr_index_to_give = 0
sock_to_range = {}
failed_indexes_to_give = []
banned_sockets = []


import queue

from clientComm import ClientComm
import socket

# connect to the main server:
msg_q = queue.Queue()
client_comm = ClientComm("127.0.0.1", 8080, msg_q)
flag = client_comm.connected

while not flag:
    flag = client_comm.connected

flag = False

# NEEDED FUNCTIONS -->
# -------------------------->



def register():
    """
    :return:
    """

def login():
    """
    :return:
    """

def download_song():
    """
    :return:
    """

def like_song():
    """
    :return:
    """

def remove_like():
    """
    :return:
    """

def receive_song_updates():
    """
    :return:
    """

def handle_income_msgs(msg_q):
    """
    :return:
    """

def main():
    """
    :return:
    """



running = True
while running:

    while not msg_q.empty():
        # sending messages:
        msg = msg_q.get()
        print(msg)

        # if process found key:
        if msg[0] == "K":

        # if a process needs a range
        if msg[0] == "A":
            try:


