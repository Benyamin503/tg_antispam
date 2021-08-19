from pyrogram import Client, filters
import pyrogram
import re

api_id = 3507193
api_hash = 'f939bf5eedbe7fa3d9b21fce69101848'

app = Client('antispam', api_id, api_hash)

antispam = True
exempt_users = []

@app.on_message((filters.me & filters.text))
def bot_command(client, message):
	splited = message.text.split()
	if len(splited) == 2:
		
		if (splited[0] == 'bot' or splited[0] == 'Bot'):
			
			global antispam
			if (splited[1] == 'on' or splited[1] == 'On'):
				if antispam:
					message.reply_text('**anti attack is activated!**')
				else:
					antispam = True
					message.reply_text('**anti attack was activated!**')
			
			
			elif (splited[1] == 'off' or splited[1] == 'Off'):
				if antispam:
					antispam = False
					message.reply_text('**anti attack was disabled!**')
				else:
					message.reply_text('**anti attack is disabled!**')
					
					
			elif (splited[1] == 'status' or splited[1] == 'Status'):
				if antispam:
					message.reply_text('**anti attack is ```activated```**')
					
				else:
					message.reply_text('**anti attack is ```disabled```**')
		
		
		elif (splited[0] == '!add' or splited[0] == '!Add'):
			try:
				user = app.get_users(splited[1]).id
				first_name = app.get_users(splited[1]).first_name
				
				if user not in exempt_users:
					exempt_users.append(user)
					message.reply_text(f'{first_name} (```{user}```) **added to exempt user!**')
					
				else:
					message.reply_text(f'{first_name} (```{user}```) **was in exempt user!**')
				
						
			except pyrogram.errors.exceptions.bad_request_400.UsernameNotOccupied:
				message.reply_text('**This user name does not exist in telegram!**')
				
			except:
				message.reply_text('**something went wrong!**')



	elif (message.text == '!help' or message.text == '!Help'):
		help_text = '''آن کردن بات👇
Bot on
_________
آف کردن بات 👇
Bot off
_________
دیدن وضعیت بات 👇
Bot status
_________
معاف کردن کاربری از بلاک شدن (ایدی عددی یا یوزرنیم وارد شود) 👇
!add @username'''

		message.reply_text(help_text, disable_web_page_preview=True)
				
				
					
		




blocked_text = r'join|@|پروپلیر|پرو پلیر|ولف|لفت|اتک|ننت|کص|کیر|گاییدم'

blocked_type = r'mention|hashtag|bot_command|text_link|text_mention'

text_dict = {}

@app.on_message((filters.private & filters.incoming) & (~filters.me))
def spam_detector(client, message):
	from_user = message.from_user
	global antispam
	if antispam:
		
		if not from_user.is_contact:
			common_chat = app.get_common_chats(user_id=from_user.id)
			
			if len(common_chat) == 0:
				
				his_count = app.get_history_count(chat_id=from_user.id)
				if his_count < 2: #optional number
					if from_user.id not in exempt_users:
						if message.entities:
							msg_types_list = []
							entities = message.entities
							for entity in entities:
								msg_types_list.append(entity.type)
							msg_types = ' '.join(msg_types_list)
							
							if re.search(blocked_type, msg_types):
								message.reply_text('**شما توسط ضد لینک من بلاک شدید😔**')
								app.block_user(from_user.id)
								peer = app.resolve_peer(from_user.id)
								app.send(pyrogram.raw.functions.messages.DeleteHistory(peer=peer, just_clear=False, revoke=False, max_id=0))
								
						
						
						elif message.text:
							text = message.text
							if re.search(blocked_text, text):
								message.reply_text('**شما توسط ضد لینک من بلاک شدید😔**')
								app.block_user(from_user.id)
								peer = app.resolve_peer(from_user.id)
								app.send(pyrogram.raw.functions.messages.DeleteHistory(peer=peer, just_clear=False, revoke=False, max_id=0))
								
								
							elif text in text_dict:
								if (text_dict[text][0] > 1 and text != '.' and text != 'سلام' and text!= 'خوبی'): 										#optional_number
									text_dict[text][0] += 1
									if from_user.id not in text_dict[text]:
										text_dict[text].append(from_user.id)
										
									message.reply_text('**شما توسط ضد لینک من بلاک شدید😔**')	
									app.block_user(from_user.id)
									peer = app.resolve_peer(from_user.id)
									app.send(pyrogram.raw.functions.messages.DeleteHistory(peer=peer, just_clear=False, revoke=False, max_id=0))
									
									
									for user in text_dict[text]:
										if not (len(str(user)) < 4):
											if user != from_user.id:
												try:
													app.send_message(chat_id=user, text='**شما توسط ضد لینک من بلاک شدید😔**')
													app.block_user(user)
													peer = app.resolve_peer(user)
													app.send(pyrogram.raw.functions.messages.DeleteHistory(peer=peer, just_clear=False, revoke=False, max_id=0))
												except Exception as e:
													print(e)
											
									
									
									
								else:
									text_dict[text][0] += 1
									if from_user.id not in text_dict[text]:
										text_dict[text].append(from_user.id)
								
							
							else:
								text_dict[text] = []
								text_dict[text].append(1)
								text_dict[text].append(from_user.id)
							
								
								

						elif message.media:
							message.reply_text('**شما توسط ضد لینک من بلاک شدید😔**')	
							app.block_user(from_user.id)
							peer = app.resolve_peer(from_user.id)
							app.send(pyrogram.raw.functions.messages.DeleteHistory(peer=peer, just_clear=False, revoke=False, max_id=0))




				
app.run()
