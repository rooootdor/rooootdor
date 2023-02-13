import os
import time
import queue
import threading
import protocol_client
from uuid import getnode
from clientComm import ClientComm
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import serverComm


# NEEDED FUNCTIONS
# ----------------->

def monitor_path():
    # songfile is saved like the following --> "song name_artist.wav"
    # create hidden song file if doesnt exist:
    if not os.path.exists("songPath_Listen_Together"):
        os.makedirs("songPath_Listen_Together")

    # def needed vars \ patterns -
    patterns = ["*"]        #
    ignore_patterns = None  #
    ignore_directories = False  #
    case_sensitive = True       #
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted

    path = "songPath_Listen_Together"
    go_recursively = True       #
    my_observer = Observer()    #
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)  #

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


def on_created(event):
    # return creation status, file_name.
    params = event.src_path.split("\\")
    print("update - created",params)
    # client_comm.send(protocol_client.pack_dynamic_update("00", song_file_name, artist))


def on_deleted(event):
    # return deletion status, file_name.
    params = event.src_path.split("\\")
    print("update - del ", params)
    # client_comm.send(protocol_client.pack_dynamic_update("01", song_file_name, artist))

# =======>


def get_macAddress():
    """ returns  mac address"""
    return ':'.join(['{:02x}'.format((getnode() >> i) & 0xff) for i in range(0, 8 * 6, 8)][::-1])


def register(params):
    """
    :return:
    """
    print("signup status is - ", params)


def login(params):
    """
    :return:
    """
    print("login status is - ", params)


def handle_download_song(ip,song_name):
    song_q = queue.Queue()
    song_client = ClientComm(ip, 2000, song_q)
    while not song_client.comm_is_ready():
        pass
    ask2song = protocol_client.pack_p2p_ask_download(song_name)
    song_client.send(ask2song)
    while True:
        data = song_q.get()
        print("in handle songs", data)
        if not data.startswith("songPath_Listen_Together"):
            opcode, data = protocol_client.unpack_msg(data)
            song_client.receive_song(song_name,int(data[1]))
        else:
            print("check song arrive")
            song_client.close_client()
            break


def download_song(params):
    """
    :return:
    """
    status = params[0]
    print(params)
    # if can download song - >
    if status == "00":
        ip_of_sharer = params[1]
        song_name = "lana.mp3"
        print("ip of sharer - ", ip_of_sharer)
        # create p2p connection
        threading.Thread(target = handle_download_song,args=(ip_of_sharer,song_name,)).start()

    else:
        # print according msg ("sorry, song unavailable.
        pass
    print("can download song status is - ", params)


def ask_for_song(params):
    pass


def upload_song(params):
    """
    :return:
    """
    print("upload status is - ", params)


def p2p_request_download():
    """
    :return:
    """


def like_dislike_song(params):
    """
    :return:
    """
    print("like/dislike status is - ", params)


def lookup_song():
    """
    :return:
    """
    # todo: lookup song in clients playlist
    # return true + info \ false + sorry msg


def play_song():
    """
    :return: play song
    """


def dynamic_update_ans(params):
    """
    :return:
    """


def handle_exit(params):
    """
    :return: take user to first scrn
    """


def handle_income_songs(songs_q):
    while True:
        ip, data = songs_q.get()
        op_code, song_name = protocol_client.unpack_msg(data)
        if op_code == "04":
            server_song_comm.send_song(song_name, ip)



def handle_income_msgs(msg_q):
    while True:
        data = msg_q.get()
        op_code, data = protocol_client.unpack_msg(data)
        if op_code in op_codes.keys():
            op_codes[op_code](data)


op_codes = {"00": register,
            "01": login,
            "02": upload_song,
            "03": download_song,
            "05": like_dislike_song,
            "06": dynamic_update_ans,
            "99": handle_exit}

if __name__ == '__main__':

    # create msg q, connection -
    msg_q = queue.Queue()
    songs_q = queue.Queue()
    client_comm = ClientComm("192.168.4.95", 1000, msg_q)

    server_song_comm = serverComm.ServerComm(2000, msg_q)


    flag = client_comm.connected

    # wait until connected
    while not flag:
        flag = client_comm.connected

    flag = False

    # create thread to handle incoming msgs from clients:
    thread_recv_msg = threading.Thread(target=handle_income_msgs, args=(msg_q,)).start()

    # create thread to handle incoming songs from clients:
    thread_recv_song= threading.Thread(target=handle_income_songs, args=(songs_q,)).start()

    # thread to monitor files :
    thread_send_update = threading.Thread(target=monitor_path).start()

    # things that work:
    # ------------------->

    # USER-DATA:
    client_comm.send(protocol_client.pack_signUp("guy", "123456", get_macAddress()))
    client_comm.send(protocol_client.pack_login("guy", "123456", get_macAddress()))

    # SONG-DATA:
    # client_comm.send(protocol_client.pack_uploadSong("lana", "lana", "reut"))
    # client_comm.send(protocol_client.pack_addOrRem_like("black hole sun", "reut"))  # add like
    # client_comm.send(protocol_client.pack_addOrRem_like("black hole sun", "reut"))  # rem like
    # client_comm.send(protocol_client.pack_downloadSong("black hole sun"))

    # ------------------->
    client_comm.send(protocol_client.pack_downloadSong("lana"))
    # ------------------->
