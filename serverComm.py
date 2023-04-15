import socket
import threading
import select
import DH_exchange_keys
import AES
import protocol_client


class ServerComm:
    """
    class to represent client  (communication)
    """

    def __init__(self, port, msg_q):
        """
        init the object
        :param port: port of communication
        :param msg_q:
        """
        self.socket = None
        self.port = port
        self.q = msg_q
        self.open_clients = {}
        self.ip_of_mac = {}
        self.AES = AES.AESCipher()
        threading.Thread(target=self._main_loop).start()

    def _main_loop(self):
        """
        connect to server
        :return:
        """
        self.socket = socket.socket()
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(8)

        while True:
            rlist, wlist, xlist = select.select([self.socket]+list(self.open_clients.keys()), list(self.open_clients.keys()), [], 0.3)
            for current_socket in rlist:

                if current_socket is self.socket:
                    client, addr = self.socket.accept()
                    print(f"{addr[0]} - connected")
                    threading.Thread(target=self._change_key, args=(client, addr[0])).start()
                    # todo - send index
                    # add sock and ind to soc list

                else:
                    try:
                        data_len = int(current_socket.recv(2).decode())
                        data = current_socket.recv(data_len)
                        decData = self.AES.decrypt(data, self._get_key_by_socket(current_socket))
                        print("server get ", decData)
                        self.q.put((decData, self._find_ip_by_socket(current_socket)))
                    except Exception as e:
                        print("ServerComm - _1!!!main_loop", str(e))
                        self._disconnect_client(current_socket)
                    else:
                        # all possible cases: in main server
                        # suddenly disconnected
                        if data == "":
                            self._disconnect_client(current_socket)

    def _get_key_by_socket(self, soc):
        key = None
        if soc in self.open_clients.keys():
            key = self.open_clients[soc][1]
        return key

    def _find_ip_by_socket(self, soc):
        '''

        :param soc:
        :return:
        '''
        find_ip = None
        if soc in self.open_clients.keys():
            find_ip = self.open_clients[soc][0]
        return find_ip

    def _find_socket_by_ip(self, ip):
        '''

        :param ip:
        :return:
        '''
        find_soc = None
        for soc in self.open_clients.keys():
            if self.open_clients[soc][0] == ip:
                find_soc = soc
                break
        return find_soc

    def send_one(self, data, ip):
        """
        send msg to all clients
        :param data: the message
        :param ip: the one to send to
        :return:
        """
        soc = self._find_socket_by_ip(ip)
        if soc:
            encData = self.AES.encrypt(data, self._get_key_by_socket(soc))
            data_len = str(len(encData)).zfill(2).encode()
            try:
                soc.send(data_len)
                soc.send(encData)
            except Exception as e:
                print("ServerComm - send_all", str(e))
                self._disconnect_client(soc)

    def send_all(self, data):
        """
        :param data: data wanted to send
        :return: send data to all connected clients
        """
        for client in self.open_clients.keys():
            self.send_one(data, self._find_ip_by_socket(client))

    def _disconnect_client(self, socket):
        """
        disconnect client
        :param socket: the client socket
        :return:
        """
        # del from ip_of_mac dict
        ip_to_del = self._find_ip_by_socket(socket)
        for mac, ip in self.ip_of_mac.items():
            if ip == ip_to_del:
                del self.ip_of_mac[mac]
                break

        if socket in self.open_clients.keys():
            print(f"{self._find_ip_by_socket(socket)} port {self.port} - disconnected")
            del self.open_clients[socket]
            socket.close()

    def _change_key(self, client, ip):
        '''
        :param client:
        :param ip:
        :return:
        '''

        # for client
        encryption1 = DH_exchange_keys.Delphi_Helman()
        key_to_send1 = encryption1.create_key()
        try:
            client.send(str(len(str(key_to_send1))).zfill(2).encode())
            client.send(str(key_to_send1).encode())
            key_len = int(client.recv(2).decode())
            key = int(client.recv(key_len).decode())
        except Exception as e:
            print("in change keys ", str(e))
            client.close()
        else:
            clientKey = encryption1.set_key(key)
            self.open_clients[client] = [ip, clientKey]

    def send_song(self, song_path, ip):
        print("song_path =", song_path)
        with open(song_path, 'rb') as f:
            data = f.read()

        song_name = song_path[song_path.rfind("\\")+1:]
        msg2send = protocol_client.pack_p2p_send(song_name, len(data))
        self.send_one(msg2send, ip)
        soc = self._find_socket_by_ip(ip)
        soc.send(data)

    def get_ip_by_mac(self, mac):
        print("all macs are - ", self.ip_of_mac)
        ip = None
        if mac in self.ip_of_mac.keys():
            print("mac is - ", mac)
            ip = self.ip_of_mac[mac]

        return ip

    def set_ip_mac(self, mac, ip):
        if self._find_socket_by_ip(ip):
            self.ip_of_mac[mac] = ip


