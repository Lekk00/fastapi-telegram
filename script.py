from telethon.sync import TelegramClient

API_ID = "13676960"
API_HASH = "e7711d9390f24907101c4018011e2da7"
PHONE_NUMBER = "+905550564025"

client = TelegramClient("session_name", API_ID, API_HASH)

async def main():
    await client.start(PHONE_NUMBER)
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        print(f"ID: {dialog.id} | Name: {dialog.title}")

with client:
    client.loop.run_until_complete(main())