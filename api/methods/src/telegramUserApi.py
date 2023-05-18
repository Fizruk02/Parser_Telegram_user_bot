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
	                app.add_contact(int(data['chat_id']), app.get_users(int(data['chat_id'])).first_name)
	                message = app.send_message(int(data['chat_id']), str(data['text']), reply_to_message_id=int(data['replay_id']))
	                answer.put(self.status(200, {"message": {"id": message.id}}))
	            elif(method == "sendMessage"):
	                app.add_contact(int(data['chat_id']), app.get_users(int(data['chat_id'])).first_name)
	                message = app.send_message(int(data['chat_id']), str(data['text']))
	                answer.put(self.status(200, {"message": {"id": message.id}}))
	            elif(method == "sendDocument"):
	                app.add_contact(int(data['chat_id']), app.get_users(int(data['chat_id'])).first_name)
	                message = app.send_document(int(data['chat_id']), str(data['path_to_file']), caption=str(data['caption']))
	                answer.put(self.status(200, {"message": {"id": message.id}}))
	            elif(method == "sendPhoto"):
	                app.add_contact(int(data['chat_id']), app.get_users(int(data['chat_id'])).first_name)
	                message = app.send_document(int(data['chat_id']), str(data['path_to_file']), caption=str(data['caption']))
	                answer.put(self.status(200, {"message": {"id": message.id}}))
	            elif(method == "sendReaction"):
	                app.add_contact(int(data['chat_id']), app.get_users(int(data['chat_id'])).first_name)
	                reaction = app.send_reaction(int(data['chat_id']), int(data['message_id']), str(data['emoji']))
	                answer.put(self.status(200, {"reaction": reaction}))
	            elif(method == "editProfile"):
	                profile = app.update_profile(first_name=data['first_name'], last_name=data['last_name'], bio=data['bio'])
	                answer.put(self.status(200, {"updateProfile": profile}))
	            elif(method == "editUsername"):
	                username = app.set_username(data['username'])
	                answer.put(self.status(200, {"updateUsername": username}))
	            elif(method == "editPhoto"):
	                photo = app.set_profile_photo(photo=data['photo'])
	                answer.put(self.status(200, {"updatePhoto": photo}))
        except Exception as error:
            if str(error) == "database is locked":
                answer.put(self.status(300, {'wait': 'This process is busy, try again in a few seconds'}))
            else:
                answer.put(self.status(400, {'error': str(error)}))

    def status(self, code, data):
        if code == 200:
            return {'status': True, 'code': code, 'data': data}
        return {'status': False, 'code': code, 'data': data}