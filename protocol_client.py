# protocol NEEDED functions ->


def unpack_msg(msg_packed):
    # todo: call decryption
    data = msg_packed.split(",")
    return data[0], data[1:]


def pack_signUp(username, password, mac):
    return f"00,{username},{password},{mac}"


def pack_login(user_name, hushed_password, mac):
    return f"01,{user_name},{hushed_password},{mac}"


def pack_uploadSong(song_name, artist_name, username):
    return f"02,{song_name},{artist_name},{username}"


def pack_downloadSong(song_name):
    # ask from server
    return f"03,{song_name}"


def pack_p2p_ask_download(song_name):
    # ask of other client
    return f"04,{song_name}"


def pack_p2p_send(song_name, song_len):
    return f"04,{song_name},{song_len}"


def pack_addOrRem_like(song_name, username):
    return f"05,{song_name},{username}"


def pack_dynamic_update(update, song_name, artist):
    return f"06,{update},{song_name},{artist}"


def pack_exit_prog():
    return "99"


