import socket
import threading

from AsymmetricEncryption import AsymmetricEncryption
from SymmetricEncryption import SymmetricEncryption


def receive_messages(client_socket, symmetric, asymmetric):
    while True:
        try:
            received_message = client_socket.recv(4096)
            if not received_message:
                print("Client disconnected.")
                break

            if received_message.startswith(b"AES"):
                encrypted_data = received_message[3:]
                print("\nencrypted_data [Client (AES)]: \n", encrypted_data)
                decrypted_message = symmetric.decrypt(encrypted_data)
                print(f"[Client (AES)]: {decrypted_message}")

            elif received_message.startswith(b"RSA"):
                encrypted_data = received_message[3:]
                print("\nEncrypted data [Client (RSA)]:\n", encrypted_data)
                decrypted_message = asymmetric.decrypt(encrypted_data)
                print(f"[Client (RSA)]: {decrypted_message}")

            else:
                print(f"[Client]: {received_message.decode()}")

        except Exception as e:
            print(f"Error while receiving: {e}")
            break


def send_messages(client_socket, symmetric, asymmetric, client_public_key):
    while True:
        try:
            print("Choose encryption method:")
            print("1. Plain (no encryption)")
            print("2. AES encryption")
            print("3. RSA encryption")

            encryption_choice = input("Enter your choice: ")
            message = input("Enter the message to send: ")

            if encryption_choice == "1":
                client_socket.send(message.encode())

            elif encryption_choice == "2":
                encrypted_msg = symmetric.encrypt(message)
                client_socket.send(b"AES" + encrypted_msg)

            elif encryption_choice == "3":
                encrypted_msg = asymmetric.encrypt(message, client_public_key)
                client_socket.send(b"RSA" + encrypted_msg)

            else:
                print("Invalid choice. Sending plain message.")
                client_socket.send(message.encode())

        except Exception as e:
            print(f"Error while sending: {e}")
            break


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(1)
    print("Server is running on 127.0.0.1:12345")

    client_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    # توليد المفاتيح العامة والخاصة
    asymmetric = AsymmetricEncryption()

    # إرسال المفتاح العام للخادم إلى العميل
    client_socket.send(asymmetric.serialize_public_key())

    # استقبال المفتاح العام للعميل
    client_public_key_data = client_socket.recv(4096)
    client_public_key = asymmetric.deserialize_public_key(client_public_key_data)

    aes_key = b'mysecurekey12345'  # Fixed AES key
    symmetric = SymmetricEncryption(key=aes_key)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, symmetric, asymmetric))
    send_thread = threading.Thread(target=send_messages, args=(client_socket, symmetric, asymmetric, client_public_key))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()
    client_socket.close()


if __name__ == "__main__":
    run_server()
