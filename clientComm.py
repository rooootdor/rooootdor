import pickle
import socket
import struct
import threading
import wave
import DH_exchange_keys
import AES
import protocol_client


class ClientComm:
    """
        class to represent client (communication)
    """

    def __init__(self, server_ip, port, msg_q):
        """
            init the object
            :param server_ip: server ip
            :param port: port of communication
            :param msg_q: collects all reiceving messages
        """
        self.socket = None
        self.server_ip = server_ip
        self.port = port
        self.msg_q = msg_q
        self.connected = False
        self.thread = threading.Thread(target=self._main_loop, daemon=True)
        self.AES = AES.AESCipher()
        self.clientKey = None
        self.thread.start()

    def _main_loop(self):
        """
            connects to server
        :return:
        """

        self.socket = socket.socket()
        try:
            self.socket.connect((self.server_ip, self.port))
        except Exception as e:
            print("clientComm - _main_loop", str(e))
            self.connected = None
            exit()
        else:
            # change keys
            print("in change keys")
            encryption1 = DH_exchange_keys.Delphi_Helman()
            key_to_send1 = encryption1.create_key()
            try:
                key_len = int(self.socket.recv(2).decode())
                key = int(self.socket.recv(key_len).decode())
                self.socket.send(str(len(str(key_to_send1))).zfill(2).encode())
                self.socket.send(str(key_to_send1).encode())

            except Exception as e:
                print("in change keys ", str(e))
                self.connected = None
                exit()
            self.clientKey = encryption1.set_key(key)
            print("done with keys ", self.clientKey)
            self.connected = True
            while self.connected:
                try:
                    data_len = self.socket.recv(2).decode()
                    data = self.socket.recv(int(data_len))
                    decData = self.AES.decrypt(data, self.clientKey)

                    self.msg_q.put(decData)
                except Exception as e:
                    self.connected = None
                    print("clientComm - _main_loop", str(e))
                    exit()

    # def p2p_connection(self):

    def send(self, msg):
        """
            send message
            :param msg: message to send
        """
        print("in send ", self.clientKey)
        msg2send = self.AES.encrypt(msg, self.clientKey)
        msg_len = str(len(msg2send)).zfill(2).encode()
        try:
            self.socket.send(msg_len)
            self.socket.send(msg2send)
        except Exception as e:
            self.connected = None
            print("clientComm - send", str(e))
            exit()

    def receive_song(self, song_name, song_len):
        data = bytearray()
        while len(data) < int(song_len):
            slice = int(song_len) - len(data)
            if slice > 1024:
                data.extend(self.socket.recv(1024))
            else:
                data.extend(self.socket.recv(slice))
                break

        file_name = f"songPath_Listen_Together\\{song_name}"
        with open (file_name, 'wb') as f:
            f.write(data)
        self.msg_q.put(file_name)


    def close_client(self):
        self.connected = False
        #self.socket.close()


    def comm_is_ready(self):
        return self.connected


