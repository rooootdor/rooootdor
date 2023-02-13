import random
import AES



class Delphi_Helman:
    """
    class to represent encryption methods
    """
    def __init__(self):
        self.p = 23197     # primary number
        self.g = 22964     # primitive root of p
        self.a = None
        self.final_key = None
        self.key_received = False

    def create_key(self):
        """
        create key to send to server
        :return: the key to send to the server
        """
        # the random number
        self.a = random.randint(0, 999999)
        key_to_send = (self.g ** self.a) % self.p
        return key_to_send

    def set_key(self, key_from_server):
        """
        get the final key
        :param key_from_server: the key the server made
        :return: the final key
        """
        final_key = str((int(key_from_server) ** self.a) % self.p)
        self.final_key = final_key
        return final_key


if __name__ == '__main__':
    # for client
    encryption1 = Delphi_Helman()
    key_to_send1 = encryption1.create_key()
    print("client key: ",key_to_send1)

    # for sever
    encryption2 = Delphi_Helman()
    key_to_send2 = encryption2.create_key()
    print("server key: ",key_to_send2)


    clientKey = encryption1.set_key(key_to_send2)
    serverKey = encryption2.set_key(key_to_send1)

    myAES = AES.AESCipher()

    text = "Hello my names is Reut Dor!!!"
    print("1: ", text)
    text2server = myAES.encrypt(text, clientKey)
    print("2: ", text2server)

    text2 = myAES.decrypt(text2server,serverKey)
    print("3: ",text2)

