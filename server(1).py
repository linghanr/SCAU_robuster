import socket
import threading

def receive_messages(client_socket):
    """接收客户端发送的消息"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"客户端: {message}")
            else:
                print("客户端已断开连接")
                client_socket.close()
                break
        except:
            print("客户端已断开连接")
            client_socket.close()
            break

def start_server():
    """启动服务器，监听客户端连接"""
    host = '0.0.0.0'  # 监听所有可用的网络接口
    port = 12345      # 选择一个端口号

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # 最大等待连接数为1

    print(f"服务器已启动，在端口 {port} 监听...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"客户端 {client_address} 已连接")

        # 创建一个线程来处理客户端的消息接收
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        # 在主线程中等待用户输入消息并发送给客户端
        while True:
            message = input("请输入要发送的消息: ")
            if message.lower() == 'exit':
                client_socket.send(message.encode('utf-8'))
                client_socket.close()
                break
            client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    start_server()