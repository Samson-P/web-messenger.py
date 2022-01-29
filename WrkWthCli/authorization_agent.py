from jose import jws, jwe
import yaml, hashlib, base64
from datetime import datetime
import os, base64, M2Crypto, db
#from M2Crypto import EVP


def web_messenger_crypt_email(email):
	user_id, err = search_client_id(email)
	secret_str = user_id + str(datetime.now())
	access = hashlib.sha256(secret_str.encode('utf-8')).hexdigest()
	secret_str = user_id + str(datetime.now()) + "GosKojnoaDoogwJw"
	refresh = hashlib.sha256(secret_str.encode('utf-8')).hexdigest()
	db.set_session(access, refresh, user_id)
	return access, refresh


def web_messenger_crypt_id(user_id):
	secret_str = user_id + str(datetime.now())
	access = hashlib.sha256(secret_str.encode('utf-8')).hexdigest()
	secret_str = user_id + str(datetime.now()) + "GosKojnoaDoogwJw"
	refresh = hashlib.sha256(secret_str.encode('utf-8')).hexdigest()
	db.set_session(access, refresh, user_id)
	return access, refresh


def search_client_id(email):
	user_id, err = db.search_param_from_db('id', email)
	if err != None:
		return None, err
	return user_id, None


def search_client_token(user_id):
	access, err = db.search_param_from_db('access', user_id)
	if err != None:
		return None, err
	return access, None


def authorization(JWTJWS):
	payload = yaml.load(JWTJWS,  Loader=yaml.BaseLoader)
	if payload['type'] in ["signin", "sendverify"]:
		return payload, None
	
	
	
	payload = yaml.load(base64.b64decode(JWTJWS.split('.')[1]), Loader=yaml.BaseLoader)
	
	if 'user_id' in payload:
		user_id = payload['user_id']
		access_token, err = search_client_token(payload['user_id'])
	else:
		try:
			user_id, err = search_client_id(payload['email'])
			access_token, err = search_client_token(user_id)
		except:
			return None, f"User with such mail ({payload['email']}) was not foundd"
	
	try:
		print(access_token)
		print(JWTJWS)
		msg = jws.verify(JWTJWS, access_token, algorithms=['HS256']).decode("utf-8")
	except:
		print("Signature verification failed ;)")
		password, err = db.search_param_from_db('passwd', user_id)
		access, refresh = web_messenger_crypt_id(user_id)
		if payload['password'] == password:
			client_refresh = {
				'type': "refresh", 'user_id': user_id, 'access': access, 'refresh': refresh }
			return client_refresh, None
		else:
			return None, "Signature verification failed"
	print(f"<<< {msg}")
	response = yaml.load(msg, Loader=yaml.BaseLoader)
	return response, None

