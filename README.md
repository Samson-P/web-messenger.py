# web-messenger.py
Simple web-messenger with python websockets


pip install websockets
pip install python-jose
pip install pyjwt
apt-get install build-essential libssl-dev swig python3-dev
pip install M2Crypto
pip install js2py
pip install selenium
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
export PATH=$PATH:/path-to-extracted-file/.

SQLite3
ALTER TABLE table_name
ADD COLUMN column_definition;


<script type=”text/javascript” src=”https://cdn.jsdelivr.net/npm/brython@3.8.9/brython.min.js"></script>
=======


WebSocket — протокол связи поверх TCP-соединения, предназначенный для обмена сообщениями между браузером и веб-сервером в режиме реального времени. — Википедия

Настраиваем свой веб-сокет с библиотекой WebSockets API, которая делает возможным двусторонний интерактивный сеанс связи между клиентом и сервером. С веб-сокетами вы можете отправлять и получать сообщения в режиме отслеживания событий без необходимости все время запрашивать данные у сервера, что уменьшает накладные расходы и позволяет передавать данные с сервера и на сервер в режиме реального времени. Это как нельзя лучше подходит для создания месенджера.

1. Я написал простенькую верстку без даже стилей. Блок для сообщений, input text для ввода сообщения, кнопку для отправки сообщения.
2. Создал на JS пару функций для обработки подключения клиента, нажатия кнопок, отправления сообщения на сервер по нажатию, а так же отправления сервером сообщения другому клиету, добавление его в div class="messages".
3. Сервер, как я говорил, написан на питоне, это короткий ассинхронный скрипт всего на пару функций, использующий библиотеки websockets и asyncio, который обслуживает всех клиентов на порту IP:1090 моей локальной сети.
4. Для подключения клиентов используется веб-сервер apache, с затычкой, которая состоит из пп. 1-2.
