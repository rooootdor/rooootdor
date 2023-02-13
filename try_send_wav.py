import socket
import wave

(HOST,PORT) = ('localhost',19123)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)); s.listen(1); conn, addr = s.accept()

with open('song_trasfered.wav','wb') as f:
  while True:
    l = conn.recv(1024)
    if not l: break
    f.write(l)
s.close()