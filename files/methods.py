import asyncio
import random
import re
import sqlite3

from twilio.rest import Client

from data.config import ACCOUNT_SID, AUTH_TOKEN, DATABASE_PATH, MY_NUMBER

client = Client(ACCOUNT_SID, AUTH_TOKEN)


async def send_sms(number, text):
    message = client.messages.create(body=text, from_=MY_NUMBER, to=number)
    await asyncio.sleep(3)
    return message.status


def generate_otp():
    otp = random.randint(101010, 909090)
    return str(otp)


def is_e164_format(number):
    pattern = r"^\+(?:[0-9]●?){6,14}[0-9]$"
    match = re.match(pattern, number)
    if match:
        return True
    else:
        return False


def create_table():
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.execute(
            f"CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, number TEXT, otp TEXT, limited INTEGER, verify INTEGER)"
        )


def create_user(discord_id: int, number: str, otp: str):
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.execute(
            f"INSERT OR REPLACE INTO users (id,number,otp,limited,verify) VALUES (?,?,?,?,?)",
            (discord_id, number, otp, 1, 0),
        )


def update_number(discord_id: int, number: str):
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.execute(f"UPDATE users SET number = {number} WHERE id = {discord_id}")


def update_otp(discord_id: int, otp: str):
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.execute(f"UPDATE users SET otp = {otp} WHERE id = {discord_id}")


def update_verify(discord_id: int, verify: int):
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.execute(f"UPDATE users SET verify = {verify} WHERE id = {discord_id}")


def get_user(discord_id: int):
    with sqlite3.connect(DATABASE_PATH) as conn:
        result = conn.execute(f"SELECT * FROM users WHERE id = {discord_id}")
    return result.fetchone()


def delete_user(discord_id: int):
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.execute(f"DELETE FROM users WHERE id = {discord_id}")
