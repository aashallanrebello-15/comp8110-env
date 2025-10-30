import socket

def main():
    HOST = "127.0.0.1"
    PORT = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    f = s.makefile("r")

    def send(msg):
        s.sendall(msg.encode())
        return f.readline().strip()

    # handshake
    send("HELO\n")
    send("AUTH aashallanrebello\n")

    while True:
        msg = send("REDY\n")
        if not msg or msg.startswith("NONE"):
            break

        if msg.startswith("JOBN"):
            parts = msg.strip().split()
            job_id = parts[2]
            cores = parts[4]
            mem = parts[5]
            disk = parts[6]

            hdr = send(f"GETS Capable {cores} {mem} {disk}\n")
            n = int(hdr.split()[1])
            send("OK\n")

            servers = []
            for _ in range(n):
                servers.append(f.readline().strip())
            send("OK\n")
            f.readline()  # consume '.'

            stype, sid = servers[0].split()[:2]
            send(f"SCHD {job_id} {stype} {sid}\n")

    send("QUIT\n")
    s.close()

if __name__ == "__main__":
    main()
