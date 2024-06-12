from flask import Flask, request, jsonify
from pymongo import MongoClient
import grpc
import user_pb2
import user_pb2_grpc
import chat_pb2
import chat_pb2_grpc

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.chat_app

user_channel = grpc.insecure_channel('localhost:50051')
chat_channel = grpc.insecure_channel('localhost:50052')

user_stub = user_pb2_grpc.UserServiceStub(user_channel)
chat_stub = chat_pb2_grpc.ChatServiceStub(chat_channel)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    response = user_stub.RegisterUser(user_pb2.UserRequest(username=data['username'], password=data['password']))
    if response.success:
        db.users.insert_one({'user_id': response.user_id, 'username': data['username'], 'password': data['password']})
        return jsonify({"message": "User registered successfully."}), 200
    else:
        return jsonify({"message": "Failed to register user."}), 400

@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.json
    response = user_stub.AuthenticateUser(user_pb2.AuthRequest(username=data['username'], password=data['password']))
    if response.success:
        return jsonify({"message": "User authenticated successfully."}), 200
    else:
        return jsonify({"message": "Failed to authenticate user."}), 400

@app.route('/create_chat', methods=['POST'])
def create_chat():
    data = request.json
    response = chat_stub.CreateChat(chat_pb2.ChatRequest(chat_id=data['chat_id'], users=data['users']))
    if response.success:
        db.chats.insert_one({'chat_id': data['chat_id'], 'users': data['users']})
        return jsonify({"message": f"Chat {data['chat_id']} created successfully."}), 200
    else:
        return jsonify({"message": f"Failed to create chat {data['chat_id']}."}), 400

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    response = chat_stub.SendMessage(chat_pb2.MessageRequest(chat_id=data['chat_id'], user_id=data['user_id'], message=data['message']))
    if response.success:
        db.messages.insert_one({'chat_id': data['chat_id'], 'user_id': data['user_id'], 'message': data['message']})
        return jsonify({"message": "Message sent successfully."}), 200
    else:
        return jsonify({"message": "Failed to send message."}), 400

@app.route('/receive_messages', methods=['POST'])
def receive_messages():
    data = request.json
    response = chat_stub.ReceiveMessages(chat_pb2.ChatRequest(chat_id=data['chat_id'], users=data['users']))
    if response.messages:
        messages = [{"timestamp": msg.timestamp, "user_id": msg.user_id, "message": msg.message} for msg in response.messages]
        return jsonify({"messages": messages}), 200
    else:
        return jsonify({"message": "No messages received."}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
