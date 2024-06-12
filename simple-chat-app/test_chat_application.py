import grpc
import user_pb2
import user_pb2_grpc
import chat_pb2
import chat_pb2_grpc

def register_user(stub, username, password):
    response = stub.RegisterUser(user_pb2.UserRequest(username=username, password=password))
    print(f"Register User: {response.username} - {'Success' if response.success else 'Failure'}")
    return response

def authenticate_user(stub, username, password):
    response = stub.AuthenticateUser(user_pb2.AuthRequest(username=username, password=password))
    print(f"Authenticate User: {username} - {'Success' if response.success else 'Failure'}")
    return response

def create_chat(stub, chat_id, users):
    response = stub.CreateChat(chat_pb2.ChatRequest(chat_id=chat_id, users=users))
    print(f"Create Chat: {response.chat_id}")
    return response

def send_message(stub, chat_id, user_id, message):
    response = stub.SendMessage(chat_pb2.MessageRequest(chat_id=chat_id, user_id=user_id, message=message))
    print(f"Send Message: {'Success' if response.success else 'Failure'}")
    return response

def receive_messages(stub, chat_id, user_id):
    response = stub.ReceiveMessages(chat_pb2.ChatRequest(chat_id=chat_id, users=[user_id]))
    print(f"Messages for Chat {chat_id}:")
    for message in response.messages:
        print(f"{message.timestamp} - {message.user_id}: {message.message}")
    return response

def main():
    user_channel = grpc.insecure_channel('localhost:50051')
    chat_channel = grpc.insecure_channel('localhost:50052')

    user_stub = user_pb2_grpc.UserServiceStub(user_channel)
    chat_stub = chat_pb2_grpc.ChatServiceStub(chat_channel)

    # Register and authenticate users
    user1 = register_user(user_stub, 'user1', 'password1')
    user2 = register_user(user_stub, 'user2', 'password2')

    auth_user1 = authenticate_user(user_stub, 'user1', 'password1')
    auth_user2 = authenticate_user(user_stub, 'user2', 'password2')

    # Create chat
    create_chat(chat_stub, 'chat1', [user1.user_id, user2.user_id])

    # Send and receive messages
    send_message(chat_stub, 'chat1', user1.user_id, 'Hello from user1')
    send_message(chat_stub, 'chat1', user2.user_id, 'Hello from user2')
    receive_messages(chat_stub, 'chat1', user1.user_id)

if __name__ == '__main__':
    main()
