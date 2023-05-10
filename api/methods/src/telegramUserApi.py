from pyrogram import Client
import os

class TelegramUserAPI:
    def __init__(self, bot_id):
        self.bot_id = str(bot_id)

    def routeApi(self, method, data, answer):
        try:
            with Client("../include/sessions/user/"+self.bot_id) as app:
	            if(method == "joinChat"):
	                chat = app.join_chat(str(data['channel_link']))
	                answer.put(self.status(200, {"chat": {"id": chat.id, "title": chat.title}}))
	            elif(method == "replyToMessage"):
	                message = app.send_message(int(data['chat_id']), str(data['text']), reply_to_message_id=int(data['replay_id']))
	                answer.put(self.status(200, {"message": {"id": message.id}}))
	            elif(method == "sendMessage"):
	                message = app.send_message(int(data['chat_id']), str(data['text']))
	                answer.put(self.status(200, {"message": {"id": message.id}}))
	            elif(method == "sendDocument"):
	                message = app.send_document(int(data['chat_id']), str(data['path_to_file']), caption=str(data['caption']))
	                answer.put(self.status(200, {"message": {"id": message.id}}))
	            elif(method == "sendPhoto"):
	                message = app.send_document(int(data['chat_id']), str(data['path_to_file']), caption=str(data['caption']))
	                answer.put(self.status(200, {"message": {"id": message.id}}))
	            elif(method == "sendReaction"):
	                reaction = app.send_reaction(int(data['chat_id']), int(data['message_id']), str(data['emoji']))
	                answer.put(self.status(200, {"reaction": reaction}))
        except Exception as error:
            if str(error) == "database is locked":
                answer.put(self.status(300, {'wait': 'This process is busy, try again in a few seconds'}))
            else:
                answer.put(self.status(400, {'error': str(error)}))

    def status(self, code, data):
        if code == 200:
            return {'status': True, 'code': code, 'data': data}
        return {'status': False, 'code': code, 'data': data}