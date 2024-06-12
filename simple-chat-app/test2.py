import grpc
import user_pb2
import user_pb2_grpc
import chat_pb2
import chat_pb2_grpc

def register_user(stub, username, password):
    response = stub.RegisterUser(user_pb2.UserRequest(username=username, password=password))
    if response.success:
        print(f"User {username} registered successfully.")
    else:
        print(f"Failed to register user {username}.")
    return response

def authenticate_user(stub, username, password):
    response = stub.AuthenticateUser(user_pb2.AuthRequest(username=username, password=password))
    print(response)
    if response.success:
        print(f"User {username} authenticated successfully.")
    else:
        print(f"Failed to authenticate user {username}.")
    return response

def create_chat(stub, chat_id, users):
    print(chat_id, users)
    response = stub.CreateChat(chat_pb2.ChatRequest(chat_id=chat_id, users=users))
    # if response.success:
    print(f"Chat {chat_id} created successfully.")
    # else:
    #     print(f"Failed to create chat {chat_id}.")
    return response

def send_message(stub, chat_id, user_id, message):
    response = stub.SendMessage(chat_pb2.MessageRequest(chat_id=chat_id, user_id=user_id, message=message))
    if response.success:
        print("Message sent successfully.")
    else:
        print("Failed to send message.")
    return response

def receive_messages(stub, chat_id, user_id):
    response = stub.ReceiveMessages(chat_pb2.ChatRequest(chat_id=chat_id, user_id=user_id))
    if response.messages:
        print("Messages received:")
        for message in response.messages:
            print(f"{message.timestamp} - {message.user_id}: {message.message}")
    else:
        print("No messages received.")
    return response

def main():
    user_channel = grpc.insecure_channel('localhost:50051')
    chat_channel = grpc.insecure_channel('localhost:50052')

    user_stub = user_pb2_grpc.UserServiceStub(user_channel)
    chat_stub = chat_pb2_grpc.ChatServiceStub(chat_channel)

    # Register and authenticate users
    username1 = input("Enter username for user1: ")
    password1 = input("Enter password for user1: ")
    user1 = register_user(user_stub, username1, password1)

    username2 = input("Enter username for user2: ")
    password2 = input("Enter password for user2: ")
    user2 = register_user(user_stub, username2, password2)

    auth_user1 = authenticate_user(user_stub, user1.username, password1)
    auth_user2 = authenticate_user(user_stub, user2.username, password2)

    # Create chat
    chat_id = input("Enter chat ID: ")
    create_chat(chat_stub, chat_id, [user1.user_id, user2.user_id])

    # Send and receive messages
    while True:
        user_input = input("Enter message in format 'user_id-message' or type 'exit' to quit: ")
        if user_input.lower() == 'exit':
            break

        try:
            user_id, message = user_input.split('- ', 1)
            send_message(chat_stub, chat_id, user_id, message)
        except ValueError:
            print("Invalid message format. Please use 'user_id-message'.")

    receive_messages(chat_stub, chat_id, user1.user_id)

if __name__ == "__main__":
    main()
