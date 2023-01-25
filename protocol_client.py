# protocol NEEDED functions ->


def unpack_msg(msg_packed):
    # todo: call decryption
    # 3 first bites are the length of the msg
    op_code = msg_packed[4:6]
    data = msg_packed[7:]

    return [op_code, data]


def pack_signUp(username, password):
    len_of_msg = 2 + len(username) + len(password)
    return [len_of_msg, "00", username, password]


def pack_login(user_name, hushed_password):
    len_of_msg = 2 + len(user_name) + len(hushed_password)
    return [len_of_msg, "01", user_name, hushed_password]


def pack_uploadSong(song_name, artist_name):
    len_of_msg = 2 + len(song_name) + len(artist_name)
    return [len_of_msg, "02", song_name, artist_name]


def pack_downloadSong(song_name):
    len_of_msg = 2 + len(song_name)
    return [len_of_msg, "03", song_name]


def pack_p2p_ask_download(song_name):
    len_of_msg = 2 + len(song_name)
    return [len_of_msg, "04", song_name]


def pack_p2p_send(song_name, filepath):
    len_of_msg = 2 + len(song_name) + len(filepath)
    return [len_of_msg, "04", song_name, filepath]


def pack_addOrRem_like(like_status):
    len_of_msg = 2 + len(like_status)
    return [len_of_msg, "05", like_status]


def pack_dynamic_update(update_to_send):
    len_of_msg = 2 + len(update_to_send)
    return [len_of_msg, "06", update_to_send]


def pack_exit_prog():
    return [2, "99"]


