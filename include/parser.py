from dotenv import load_dotenv, find_dotenv
from pyrogram.handlers import MessageHandler
from pyrogram import Client, idle
import requests
import pymysql
import json
import os

load_dotenv(find_dotenv())

URL_TO_WEBHOOK = os.getenv("URL_TO_WEBHOOK")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_TABLE = os.getenv("DB_TABLE")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")

active_bots = []

conn = pymysql.connect(
    host="localhost",
    port=3306,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    cursorclass=pymysql.cursors.DictCursor
)

with conn.cursor() as cursor:
    query = "SELECT `api_key` FROM `"+DB_TABLE+"` WHERE `status` = 1"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        bot_id = row['api_key']
        active_bots.append(bot_id)

conn.close()