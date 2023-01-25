import pickle
import socket
import struct
import threading
import wave

import pyaudio


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
            self.connected = True
            while True:
                try:
                    data_len = self.socket.recv(2).decode()
                    data = self.socket.recv(int(data_len))
                    self.msg_q.put(data.decode())
                except Exception as e:
                    self.connected = None
                    print("clientComm - _main_loop", str(e))
                    exit()

    def send(self, msg):
        """
            send message
            :param msg: message to send
        """
        msg_len = str(len(msg)).zfill(2).encode()
        if type(msg) == str:
            msg = msg.encode()
        try:
            self.socket.send(msg_len)
            self.socket.send(msg)
        except Exception as e:
            self.connected = None
            print("clientComm - send", str(e))
            exit()

    def send_song(self, file_path):
        CHUNK_TO_SEND = 1024
        wf = wave.open(file_path+".wav", 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        input=True,
                        frames_per_buffer=CHUNK_TO_SEND)
        while True:
            data = wf.readframes(CHUNK_TO_SEND)
            a = pickle.dumps(data)
            message = struct.pack("Q", len(a)) + a
            self.socket.sendall(message)

    def receive_song(self):
        p = pyaudio.PyAudio()
        CHUNK_TO_SEND = 1024
        stream = p.open(format=p.get_format_from_width(2),
                        channels=2,
                        rate=44100,
                        output=True,
                        frames_per_buffer=CHUNK_TO_SEND)

        data = b""
        payload_size = struct.calcsize("Q")
        while True:
            try:
                while len(data) < payload_size:
                    packet = self.socket.recv(4 * 1024)  # 4K
                    if not packet:
                        break
                    data += packet

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += self.socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                stream.write(frame)
            except Exception as e:
                print(e, "in receive_song")
                break




