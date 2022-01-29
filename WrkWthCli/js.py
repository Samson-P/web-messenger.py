from selenium import webdriver


html_content = """
<html>
<head>
	<title>web-messenger.py/verify</title>
	<meta charset="UTF-8">
	<script src="https://kjur.github.io/jsrsasign/jsrsasign-latest-all-min.js"></script>
	<script src="js/auth.js" type="application/javascript"></script>
</head>
</html>
"""


def execute_js(salt, secret):
	scrypt_string = f"KJUR.jws.JWS.verify({salt}, {secret}, ['HS256'])"
	driver = webdriver.Firefox()
	
	driver.get(f"data:text/html;charset=utf-8,{html_content}")
	return driver.execute_script(scrypt_string)


salt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2YWx1ZSI6ImNiZWUzNGM0OTYyZjA1MjEwYzNlZDRiMmQxNGNlYjRjMGJkZjRkNDMifQ.iS3FFjlzRMmqxaj1kFHnTgf2Wd2rQclKO_Dxc-mMRWI"
secret = "34802315"
execute_js(salt, secret)
