# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\"C\n\x0eMessageRequest\x12\x0f\n\x07\x63hat_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"\"\n\x0fMessageResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"-\n\x0b\x43hatRequest\x12\x0f\n\x07\x63hat_id\x18\x01 \x01(\t\x12\r\n\x05users\x18\x02 \x03(\t\"\x1f\n\x0c\x43hatResponse\x12\x0f\n\x07\x63hat_id\x18\x01 \x01(\t\"O\n\x07Message\x12\x0f\n\x07\x63hat_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\t\")\n\x0bMessageList\x12\x1a\n\x08messages\x18\x01 \x03(\x0b\x32\x08.Message2\x99\x01\n\x0b\x43hatService\x12\x30\n\x0bSendMessage\x12\x0f.MessageRequest\x1a\x10.MessageResponse\x12-\n\x0fReceiveMessages\x12\x0c.ChatRequest\x1a\x0c.MessageList\x12)\n\nCreateChat\x12\x0c.ChatRequest\x1a\r.ChatResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MESSAGEREQUEST']._serialized_start=14
  _globals['_MESSAGEREQUEST']._serialized_end=81
  _globals['_MESSAGERESPONSE']._serialized_start=83
  _globals['_MESSAGERESPONSE']._serialized_end=117
  _globals['_CHATREQUEST']._serialized_start=119
  _globals['_CHATREQUEST']._serialized_end=164
  _globals['_CHATRESPONSE']._serialized_start=166
  _globals['_CHATRESPONSE']._serialized_end=197
  _globals['_MESSAGE']._serialized_start=199
  _globals['_MESSAGE']._serialized_end=278
  _globals['_MESSAGELIST']._serialized_start=280
  _globals['_MESSAGELIST']._serialized_end=321
  _globals['_CHATSERVICE']._serialized_start=324
  _globals['_CHATSERVICE']._serialized_end=477
# @@protoc_insertion_point(module_scope)