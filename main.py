import websockets
import asyncio


all_clients = []


async def send_message(message: str):
	for client in all_clients:
		await client.send(message)


async def new_client_connected(client_socket: websockets.WebSocketClientProtocol, path: str):
	print("New client connected!")
	all_clients.append(client_socket)
	
	while True:
		new_message = await client_socket.recv()
		print("New message from a client: ", new_message)
		await send_message(message=new_message)


async def start_server():
	await websockets.serve(new_client_connected, "localhost", 1090)


if __name__ == '__main__':
	event_loop = asyncio.get_event_loop()
	event_loop.run_until_complete(start_server())
	event_loop.run_forever()
