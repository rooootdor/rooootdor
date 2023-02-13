# protocol NEEDED functions ->


def unpack_msg(msg_packed):
    # todo: call decryption
    data = msg_packed.split(",")
    return data[0], data[1:]


def pack_signUp(singup_status):
    flag = "01"
    if singup_status:
        flag = "00"

    return f"00,{flag}"


def pack_login(login_status):
    flag = "01"
    if login_status:
        flag = "00"
    return f"01,{flag}"


def pack_uploadSong(upload_status):
    flag = "01"
    if upload_status:
        flag = "00"
    return f"02,{flag}"


def pack_downloadSong(ip_of_share):
    flag = "01"
    if len(ip_of_share) > 0:
        ips = ",".join(x for x in ip_of_share)
        flag = f"00,{ips}"
    return f"03,{flag}"


def pack_addOrRem_like(like_status):
    flag = "01"
    if like_status:
        flag = "00"
    return f"05,{flag}"


def pack_dynamic_update(update_status):
    return f"06,{update_status}"


def pack_exit_prog():
    return {2, "99"}

