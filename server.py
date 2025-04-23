import socket
from http import HTTPStatus

HOST = "127.0.0.1"
PORT = 61432


def parse_request(data_request):
    lines = data_request.splitlines()
    method = lines[0].split()[0]
    url = lines[0].split()[1]
    try:
        status_code = int(url.split("status=")[1])
    except (ValueError, IndexError):
        status_code = 200
    status_message = HTTPStatus(status_code).phrase
    response_body = (
        f"Request Method: {method}\r\n"
        f"Request Source: {addr}\r\n"
        f"Response Status: {status_code} {status_message}\r\n"
    )
    for line in lines[1:]:
        response_body += f"{line}\r\n"
    response = (
        f"HTTP/1.1 {status_code} {status_message}\r\n"
        f"Content-Type: text/plain; charset=utf-8\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        f"\r\n"
        f"{response_body}"
    )
    return response.encode("utf-8")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
    serv.bind((HOST, PORT))
    serv.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")
    while True:
        conn, addr = serv.accept()
        with conn:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
            http_response = parse_request(data)
            conn.sendall(http_response)
