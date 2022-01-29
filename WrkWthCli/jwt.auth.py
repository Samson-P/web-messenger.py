import websockets, asyncio, yaml, hashlib, base64
import db, jwt, random
from jose import jws, jwe
from authorization_agent import *
import pathlib
import ssl
import logging



logging.basicConfig(filename = "proxy.log", level = logging.DEBUG, format = "%(asctime)s - %(message)s")
#from websocket import create_connection
# 


#ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
#ssl_context.load_cert_chain(localhost_pem)


async def send(client, message):
	print(f"<<< {message}")
	await client.send(message)


async def hello(websocket):
	logging.info(">>> New client connected!");
	while True:
		JWTJWS = await websocket.recv()
		print(f">>> {JWTJWS}")
		response, err = authorization(JWTJWS)
		
		if err != None:
			print(err)
			await send(websocket, message='err')
		
		if "refresh" == response['type']:
			await send(websocket, message=str(response).replace("'", '"'))
		
		if "sendverify" == response['type']:
			user_id, err = search_client_id(response['email'])
			password, err = db.search_param_from_db('passwd', user_id)
			try:
				print('salt site', response['salt'])
				print(password)
				#jws.verify(response['salt'], password, algorithms=['HS256']).decode("utf-8")
				jws.verify(response['salt'], password, algorithms=['HS256'])
				
				content = {
					'type': "ok", 'message': "Signature verification succsess!!" }
			except:
				print("Signature verification failed")
				content = {
					'type': "err", 'err': "Signature verification failed" }
			
			
			await send(websocket, message=str(content).replace("'", '"'))
		
		if "signin" == response['type']:
			user_id, err = search_client_id(response['email'])
			password, err = db.search_param_from_db('passwd', user_id)
			RND = str(random.getrandbits(128))
			hash_object = hashlib.sha1(RND.encode('utf-8')) 
			pbHash = hash_object.hexdigest()
			print(pbHash)
			#db.salt_user(pbHash, user_id)
			content = {
				'type': "signin", 'user_id': user_id, 'sha1_salt': pbHash }
			signed = jws.sign({ 'value': pbHash }, password, algorithm='HS256')
			
			await send(websocket, message=str(content).replace("'", '"'))
		
		if "logout" == response['type']:
			print("Client went offline")
			websocket.close()
		
		if "sendmessage" == response['type']:
			print("Client send: {}".format(response['user_id'], response['message']))


async def main():
	async with websockets.serve(hello, "localhost", 8765): #ssl=ssl_context
		await asyncio.Future()  # run forever


if __name__ == "__main__":
	asyncio.run(main())
