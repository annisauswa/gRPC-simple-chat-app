import grpc
from concurrent import futures
import redis
import hashlib
import user_pb2
import user_pb2_grpc

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def RegisterUser(self, request, context):
        user_id = f"user:{request.username}"
        if self.redis_client.exists(user_id):
            return user_pb2.UserResponse(user_id="", username="", success=False)
        
        user_data = {
            'user_id': user_id,
            'username': request.username,
            'password': self.hash_password(request.password)
        }
        self.redis_client.hmset(user_id, user_data)
        return user_pb2.UserResponse(user_id=user_id, username=request.username, success=True)
    
    def AuthenticateUser(self, request, context):
        user_id = f"user:{request.username}"
        if not self.redis_client.exists(user_id):
            return user_pb2.AuthResponse(user_id="", token="", success=False)
        
        user_data = self.redis_client.hgetall(user_id)
        if self.hash_password(request.password) != user_data[b'password'].decode():
            return user_pb2.AuthResponse(user_id="", token="", success=False)
        
        token = hashlib.sha256(f"{request.username}{request.password}".encode()).hexdigest()
        self.redis_client.setex(f"session:{token}", 3600, user_id)  # Session valid for 1 hour
        return user_pb2.AuthResponse(user_id=user_id, token=token, success=True)
    
    def GetUser(self, request, context):
        user_data = self.redis_client.hgetall(request.user_id)
        if not user_data:
            return user_pb2.UserResponse(user_id="", username="", success=False)
        return user_pb2.UserResponse(
            user_id=user_data[b'user_id'].decode(),
            username=user_data[b'username'].decode(),
            success=True
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
