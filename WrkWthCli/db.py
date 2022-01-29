import sqlite3
import os
from datetime import datetime
import time


filename = "users.sqlite3"
DB_NAME = "users"
param = ["email", "passwd", "id", "username", "first_name", "second_name", "access", "refresh"]


def check_db():
    return os.path.exists(filename)


def get_database_connection():
	if not check_db():
		return None, 'Missing {} database local'.format(filename)
	
	con = sqlite3.connect(filename)

	return con, None


def search_param_from_db(comand, user): #search_param_from_db('access', 'id')
	"""
	Return param by prod names from database.
	"""
	if comand == "id":
		sql_query = ''' SELECT {} FROM {} WHERE email = '{}'; '''.format(comand, DB_NAME, user)
	elif comand == "access":
		sql_query = ''' SELECT {} FROM {} WHERE id = '{}'; '''.format(comand, DB_NAME, user)
	elif comand == "passwd":
		sql_query = ''' SELECT {} FROM {} WHERE id = '{}'; '''.format(comand, DB_NAME, user)

	con, err = get_database_connection()
	
	if err != None:
		return None, err
	
	cur = con.cursor()

	cur.execute(sql_query)
	result = cur.fetchall()
	value = str(result[0][0])
	
	cur.close()
	con.close()  

	return value, None


def authorization_assistant(comand, username):
	"""
	Return param by prod names from database.
	"""

	sql_query = ''' SELECT {} FROM {} WHERE username = '{}'; '''.format(comand, 'users', username)

	con, err = get_database_connection()
	
	if err != None:
		return None, err
	
	cur = con.cursor()

	cur.execute(sql_query)
	result = cur.fetchall()
	value = str(result[0][0])
	
	cur.close()
	con.close()
	
	if comand == "signin" and value == "Yes":
		return True
	elif comand == "signin" and value == "No":
		return False
	if comand == "start_time" and value != "-":
		return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
	if comand == "start_time" and value == "-":
		return None
	if comand == "passwd":
		return value
	
	return value, None


def set_session(access, refresh, user_id):
	
	
	sql_query = """ update {} set access = '{}', refresh = '{}' where id = '{}'; """.format('users', access, refresh, user_id)
	
	con, err = get_database_connection()
	
	if err != None:
		con.close()
		return err
	
	con.execute(sql_query)
	con.commit()
	con.close()  

	return None


def salt_user(salt, user_id):
	sql_query = """ update {} set salt = '{}' where id = '{}'; """.format('users', salt, user_id)
	con, err = get_database_connection()
	
	if err != None:
		con.close()
		return err
	
	con.execute(sql_query)
	con.commit()
	con.close()  

	return None

