document.addEventListener('DOMContentLoaded', function(){

	const signinButton = document.querySelector("[name=signin]");
	const logoutButton = document.querySelector("[name=logout]");
	const sendButton = document.querySelector("[name=send]");
	const tokenContainer = document.querySelector("[name=client-identification]");

	let websocketClient = new WebSocket("ws://localhost:8765");
	
	function CookiesDelete() {
		var cookies = document.cookie.split(";");
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i];
			var eqPos = cookie.indexOf("=");
			var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
			document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;";
			document.cookie = name + '=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
		}
	};
	
	function getCookie(name) {
		let matches = document.cookie.match(new RegExp(
			"(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
		));
		return matches ? decodeURIComponent(matches[1]) : undefined;
	};
	
	function JWTstring(content) {
		var header = {
			"alg": "HS256",
			"typ": "JWT"
		};
		sHeader = JSON.stringify(header);
		sPayload = JSON.stringify(content);
		secret = getCookie("access");
		unsignedToken = btoa(sHeader) + "." + btoa(unescape(encodeURIComponent(sPayload)));
		unsignedToken = unsignedToken.split('=').join('');
		return KJUR.jws.JWS.sign(header.alg, sHeader, sPayload, secret);
	};
	
	function JWTpasswd(content) {
		var header = {
			alg: "HS256",
			typ: "JWT"
		};
		var dict_content = {
			value: content
		};
		sHeader = JSON.stringify(header);
		sPayload = JSON.stringify(dict_content);
		secret = document.querySelector("[name=password]").value; //password
		//unsignedToken = btoa(sHeader) + "." + btoa(unescape(encodeURIComponent(sPayload)));
		//alert(unsignedToken);
		//unsignedToken = unsignedToken.split('=').join('');
		return KJUR.jws.JWS.sign(header.alg, sHeader, sPayload, secret);
	};
	
	websocketClient.onopen = () => {
		console.log("Client connected!");
		
		signinButton.onclick = () => {
			var content = {
				type: "signin",
				email: document.querySelector("[name=email]").value,
				//password: document.querySelector("[name=password]").value,
			};
			//websocketClient.send(JWTstring(content));
			websocketClient.send(JSON.stringify(content));
		};
		logoutButton.onclick = () => {
			var content = {
				type: "logout",
				user_id: getCookie("id"),
				token: document.querySelector("[name=client-token]").value,
			};
			websocketClient.send(JWTstring(content));
			CookiesDelete();
		};
		sendButton.onclick = () => {
			var content = {
				type: "sendmessage",
				user_id: getCookie("id"),
				message: document.querySelector("[name=message]").value,
			};
			websocketClient.send(JWTstring(content));
			//websocketClient.send(JSON.stringify(content));
		};
	};

	websocketClient.onmessage = (message) => {
		comand = JSON.parse(message.data);
		if(comand['type'] == "err") {
			alert(comand["err"]); };
		if(comand['type'] == "refresh") {
			document.cookie = "access=" + comand['access'];
			document.cookie = "refresh=" + comand['refresh'];
			document.cookie = "id=" + comand['user_id'];
		};
		if(comand['type'] == "signin") {
			var content = {
				type: "sendverify",
				email: document.querySelector("[name=email]").value,
				salt: JWTpasswd(comand["sha1_salt"])
			};
			websocketClient.send(JSON.stringify(content));
			password = document.querySelector("[name=password]").value; //password
			RND_stat = KJUR.jws.JWS.verify(JWTpasswd(comand["sha1_salt"]), password, ['HS256']);
			//RND_stat = KJUR.jws.JWS.verify(JWTpasswd(comand["sha1_salt"]), {utf8: password}, ['HS256']);
			//RND = KJUR.crypto.Cipher.decrypt(comand["password"], password);
			alert(RND_stat);
		};
		if(comand['type'] == "ok") {
			alert(comand['message']);
		};
		
	};
	
	

}, false);
