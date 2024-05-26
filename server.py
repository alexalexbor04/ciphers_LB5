import pickle
import socket

from algoritmizator import DiffHel, Coder

IP = '127.0.0.1'
PORT = 12345
ALLOWED_KEYS_FILE = "allowed_keys.txt"
b = 123

def load_allowed_keys():
    with open(ALLOWED_KEYS_FILE, "r") as file:
        return [int(line.strip()) for line in file]

def main():
    try:
        sock = socket.socket()
        sock.bind((IP, PORT))
        sock.listen(1)

        coder = None
        allowed_keys = load_allowed_keys()
        conn, addr = sock.accept()

        while True:
            msg = conn.recv(4096)
            data = pickle.loads(msg)

            if type(data) == tuple:
                p, g, A = data

                if A not in allowed_keys:
                    print("Незнакомый клиент. Подключение разорвано.")
                    conn.close()
                    continue

                diff_hel = DiffHel(ab=b, p=p, g=g)
                B = diff_hel.calculate_key
                K = diff_hel.calculate_k(A)
                coder = Coder(K)
                conn.send(pickle.dumps(B))

            else:
                decrypted_message = coder.decode(data.decode())
                print("Полученное сообщение = ", decrypted_message)

                encrypted_answer = coder.code(decrypted_message)
                conn.send(encrypted_answer.encode())
    except EOFError:
        sock.close()

if __name__ == "__main__":
    main()
