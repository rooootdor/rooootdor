# protocol NEEDED functions ->


def unpack_msg(msg_packed):
    # todo: call decryption
    # 3 first bites are the length of the msg
    op_code = msg_packed[4:6]
    data = msg_packed[7:]

    return [op_code, data]


def pack_signUp(singup_status):
    len_of_msg = 2 + len(singup_status)
    return [len_of_msg, "00", singup_status]


def pack_login(login_status):
    len_of_msg = 2 + len(login_status)
    return [len_of_msg, "01", login_status]


def pack_uploadSong(upload_status):
    len_of_msg = 2 + len(upload_status)
    return [len_of_msg, "02", upload_status]


def pack_downloadSong(download_status):
    len_of_msg = 2 + len(download_status)
    return [len_of_msg, "03", download_status]


def pack_addOrRem_like(like_status):
    len_of_msg = 2 + len(like_status)
    return [len_of_msg, "05", like_status]


def pack_dynamic_update(update_status):
    len_of_msg = 2 + len(update_status)
    return [len_of_msg, "06", update_status]


def pack_exit_prog():
    return [2, "99"]

