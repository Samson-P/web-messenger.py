import websockets, asyncio, yaml, hashlib
import db, jwt


clients = {
	'samson': {'id': '0001', 'password': '34802315', 'time': '2021-12-26 23:31:15'},
	'andrew': {'id': '0002', 'password': '34238015', 'time': '2021-10-23 24:45:00'},
}

#jwt.encode({"some": "payload"}, "secret", algorithm="HS256", headers={"kid": "230498151c214b788dd97f22b85410a5"},)

async def connect(client, message):
	await client.send(message)


async def new_client_connected(client_socket: websockets.WebSocketClientProtocol, path: str):
	print("New client connected!")
	
	while True:
		msg = await client_socket.recv()
		print(msg)
		
		response = yaml.load(msg, Loader=yaml.BaseLoader)
		
		if "signin" == response['type']:
			if response['login'] in clients:
				if clients[response['login']]['password'] == response['password']:
					await connect(client_socket, message=hashlib.md5(b'0001samson348023152021-12-2623:31:15').hexdigest())
		
		if "logout" == response['type']:
			print("Client went offline")
			client_socket.close()
		
		if "sendmessage" == response['type']:
			print("Client send: {}".format(response['message']))


async def test_auth_token(token):
	header="Authorization: BEARER " + str(token)
	conn = create_connection("ws://192.168.0.14:1080"+ '/'+ "api.token", header)
	result = conn.recv()
	await assert result is not None


async def start_server():
	await websockets.serve(new_client_connected, "192.168.0.14", 1080)


if __name__ == '__main__':
	event_loop = asyncio.get_event_loop()
	event_loop.run_until_complete(test_auth_token()) # start_server
	event_loop.run_forever()
