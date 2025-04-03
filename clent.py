import socket
import threading

def receive_messages(client_socket):
    """接收服务器发送的消息"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\n服务器: {message}")
                print("请输入消息: ", end='', flush=True)  # 保持输入提示
            else:
                print("\n连接已关闭")
                client_socket.close()
                break
        except Exception as e:
            print(f"\n连接错误: {str(e)}")
            client_socket.close()
            break

def start_client():
    """启动客户端连接服务器"""
    host = '192.168.10.56'  # 服务器地址
    port = 12345        # 服务器端口

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print(f"已连接到服务器 {host}:{port}")
    except Exception as e:
        print(f"连接失败: {str(e)}")
        return

    # 启动接收消息线程
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
    receive_thread.start()

    try:
        while True:
            message = input("请输入消息: ")
            if message.lower() == 'exit':
                client_socket.send(message.encode('utf-8'))
                print("关闭连接...")
                break
            client_socket.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("\n主动终止连接")
        client_socket.send('exit'.encode('utf-8'))
    except Exception as e:
        print(f"发送错误: {str(e)}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()