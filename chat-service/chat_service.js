const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const redis = require('redis');

const PROTO_PATH = './chat.proto';
const USER_PROTO_PATH = './user.proto';

const chats = {};
const chatUsers = {};

// Create Redis client
// const redisClient = redis.createClient();

// Load chat proto
const chatPackageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});
const chatProto = grpc.loadPackageDefinition(chatPackageDefinition).ChatService;

// Load user proto
const userPackageDefinition = protoLoader.loadSync(USER_PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});
const userProto = grpc.loadPackageDefinition(userPackageDefinition).UserService;

const userClient = new userProto('localhost:50051', grpc.credentials.createInsecure());

function sendMessage(call, callback) {
  // const message = {
  //   chat_id: call.request.chat_id,
  //   user_id: call.request.user_id,
  //   message: call.request.message,
  //   timestamp: new Date().toISOString()
  // };
  // const chatKey = `chat:${call.request.chat_id}`;
  // redisClient.rpush(chatKey, JSON.stringify(message), (err, res) => {
  //   if (err) {
  //     callback(err, null);
  //   } else {
  //     callback(null, { success: true });
  //   }
  // });

  const message = {
    chat_id: call.request.chat_id,
    user_id: call.request.user_id,
    message: call.request.message,
    timestamp: new Date().toISOString()
  };

  if (!chats[call.request.chat_id]) {
    chats[call.request.chat_id] = [];
  }

  chats[call.request.chat_id].push(message);
  callback(null, { success: true });
}

function receiveMessages(call, callback) {
  // const chatKey = `chat:${call.request.chat_id}`;
  // redisClient.lrange(chatKey, 0, -1, (err, messages) => {
  //   if (err) {
  //     callback(err, null);
  //   } else {
  //     const messageList = { messages: messages.map(message => JSON.parse(message)) };
  //     callback(null, messageList);
  //   }
  // });

  const messages = chats[call.request.chat_id] || [];
  callback(null, { messages });
}

function createChat(call, callback) {
  // const chatId = `chat:${call.request.chat_id}`;

  //   call.request.users.forEach(user => {
  //     redisClient.sadd(`chat_users:${chatId}`, user, (err, reply) => {
  //       if (err) {
  //         console.error('Error adding user to chat:', err);
  //       }
  //     });
  //   });
  //   callback(null, { chat_id: call.request.chat_id });

  const chatId = call.request.chat_id;
  chatUsers[chatId] = call.request.users;
  callback(null, { chat_id: chatId });

}

function main() {
  const server = new grpc.Server();
  server.addService(chatProto.service, {
    sendMessage: sendMessage,
    receiveMessages: receiveMessages,
    createChat: createChat,
  });
  server.bindAsync('0.0.0.0:50052', grpc.ServerCredentials.createInsecure(), () => {
    server.start();
    console.log('Chat Service started on port 50052');
  });
}

main();
