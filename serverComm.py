import socket
import threading
import select


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
            rlist, wlist, xlist = select.select([self.socket]+list(self.open_clients.keys()), list(self.open_clients.keys()), [])
            for current_socket in rlist:

                if current_socket is self.socket:
                    client, addr = self.socket.accept()
                    print(f"{addr[0]} - connected")
                    self.open_clients[client] = addr[0]
                    # todo - send index
                    # add sock and ind to soc list

                else:
                    try:
                        data_len = int(current_socket.recv(2).decode())
                        data = current_socket.recv(data_len).decode()
                        self.q.put((data, addr))
                    except Exception as e:
                        print("ServerComm - _1!!!main_loop", str(e))
                        self._disconnect_client(current_socket)
                    else:
                        # all possible cases: in main server
                        # suddenly disconnected
                        if data == "":
                            self._disconnect_client(current_socket)

    def send_one(self, data, ip):
        """
        send msg to all clients
        :param data: the message
        :param ip: the one to send to
        :return:
        """
        data_len = str(len(data)).zfill(2).encode()
        if type(data) == str:
            data = data.encode()
        for soc in self.open_clients.keys():
            if self.open_clients[soc] == ip:
                try:
                    soc.send(data_len)
                    soc.send(data)
                except Exception as e:
                    print("ServerComm - send_all", str(e))
                    self._disconnect_client(soc)

    def _disconnect_client(self, socket):
        """
        disconnect client
        :param socket: the client socket
        :return:
        """
        # todo - add range to need to do, delete soc from working list
        if socket in self.open_clients.keys():
            print(f"{self.open_clients[socket]} - disconnected")
            del self.open_clients[socket]
            socket.close()
