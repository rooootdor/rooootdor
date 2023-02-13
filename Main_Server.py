import hashlib
from serverComm import ServerComm
import queue
from serverComm import ServerComm
import protocol_server
import DB_listenTgthr
import threading


# NEEDED FUNCTIONS -->
# -------------------------->

def register(params, DB):
    """
    :return: return packed msg with status of could\n't register to system
    """

    username = params[0]
    password = params[1]
    mac_addr = params[2]

    # enter user to database:
    added_to_db = DB.enter_client(username, mac_addr, password)

    return protocol_server.pack_signUp(added_to_db)


def login(params, DB):
    """
    :return: return packed msg with status of could\n't login to system
    """

    username = params[0]
    password = params[1]
    mac = params[2]
    ip = params[3]

    # check if can get logged in:
    can_log_in = DB.verify_login(username, password)



    # if can login -
    # 1) want to get MAC to put in mac -> ip dict (for p2p connection)
    print("mac - ", mac)
    server_comm.ip_of_mac[mac] = ip
    return protocol_server.pack_login(can_log_in)


# todo later
def download_song(song_name, DB):
    """
    :return: return packed msg with status of could\n't download song
    """
    # get mac of sharing users if there are
    song_name = song_name[0]
    can_download = DB.give_mac_of_shares(song_name)
    print("sharers of song - ", can_download)
    print("all macs given - ", server_comm.ip_of_mac)
    ip = []

    if len(can_download) > 0:
        # go over all MAC sharers, try to find one that is connected to server: (tup(0) = mac)
        for tup in can_download:
            print("going thru all macs - ", tup[0])
            temp = server_comm.get_ip_by_mac(tup[0])
            if temp:
                ip.append(temp)
                break

    ans = protocol_server.pack_downloadSong(ip)
    return ans


def upload_song(params, DB):
    """
    :return: return packed msg with status of could\n't update song to system
    """
    song_name = params[0]
    artist_name = params[1]
    username = params[2]
    mac_addr = DB.get_mac_of_user(username)[0][0]


    # can the song be uploaded?
    song_added = DB.add_song(song_name, artist_name, mac_addr)

    return protocol_server.pack_uploadSong(song_added)


def add_remove_like(params,DB):
    """
    :return: return packed msg with status of could\n't dislike/like song
    """
    song_name = params[0]
    user_name = params[1]

    could_add_rem = DB.add_like_or_rem(song_name, user_name)

    return protocol_server.pack_addOrRem_like(could_add_rem)


def receive_song_updates(params, DB):
    """
    :return: return packed msg with status of could\n't receive update
    """
    # check in db for song
    # check type of update:
    event = params[0]  # 01 - deleted
    song_name = params[1]
    artist = params[2]
    ip_of_user = params[3]

    # get mac of user:
    mac_of_user = server_comm.ip_of_mac[ip_of_user]


    if event == "00":
        # song added  - new sharer of EXISTING song:
        # add to sharing table (user, mac)

        DB.add_song(song_name,artist,mac_of_user)


    elif event == "01": # song deleted
        # delete share song from user:
        # todo - figure out - do we take into consideration deletion?
        pass

    return protocol_server.pack_dynamic_update("00")


def handle_exit(username,DB):
    """
    :return: delete user from all tables in db.
    """

    DB.remove_client(username)

    return protocol_server.pack_exit_prog()


def handle_income_msgs(msg_q, comm):
    """
    :return:
    """

    DB = DB_listenTgthr.DB("DB_listenTgthr")

    while True:
        data, ip = msg_q.get()
        print("data is - ", data)
        op_code, data = protocol_server.unpack_msg(data)

        # if logging in \ receiving song update  -> need to transfer ip as well.
        if op_code == "01" or "06":
            data.append(ip)

        #print("in income", data)
        #print("opcode is - ", op_code)

        if op_code in op_codes.keys():
            msg = op_codes[op_code](data,DB)
            comm.send_one(msg, ip)


op_codes = {"00": register,
            "01": login,
            "02": upload_song,
            "03": download_song,
            "05": add_remove_like,
            "06": receive_song_updates,
            "99": handle_exit}

if __name__ == '__main__':
    # make table -
    # create msg q, connection -
    msg_q = queue.Queue()
    server_comm = ServerComm(1000, msg_q)

    # create thread to handle incoming msgs from clients:
    thread_recv_msg = threading.Thread(target=handle_income_msgs, args=(msg_q, server_comm)).start()
