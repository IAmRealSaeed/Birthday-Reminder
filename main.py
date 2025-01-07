import asyncio
from pyrogram import Client, filters
import jdatetime
import pytz

# Specify your time zone
timezone = pytz.timezone('Asia/Tehran')

# Bot credentials
API_ID = "123456789"  # Replace with your API ID
API_HASH = "123qwer123qwer"  # Replace with your API hash
PHONE_NUMBER = '+1234567890'  # Replace with your Phone Number

# Initialize the bot
app = Client("group_name_bot", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

groups_to_update = []  # Add group IDs here

target_time = jdatetime.datetime(1403, 10, 18, 0, 0, 0, tzinfo=timezone)


async def update_group_names():
    """Periodically updates the group names."""
    while True:
        current_persian_datetime = jdatetime.datetime.now(timezone)
        target_persian_datetime = target_time
        time_delta = target_persian_datetime - current_persian_datetime
        remaining_seconds = time_delta.total_seconds()
        rem = round(remaining_seconds / (3600 * 24), 3)

        for group_id in groups_to_update:
            try:
                if rem <= 0:
                    group_name = "Happy Birthday!"
                else:
                    group_name = f"{rem} Day's until your birthday!"
                await app.set_chat_title(group_id, group_name)
                async for message in app.get_chat_history(group_id, limit=3):
                    # Delete the system notification
                    if message.service:
                        s = await app.delete_messages(group_id, message.id)
                print(f"Group name set to: {group_name}")
            except Exception as e:
                print(f"Failed to update group {group_id}: {e}")

        # Wait to not get flooded
        await asyncio.sleep(620)


@app.on_message(filters.command("ping") & filters.group)
async def ping(client, message):
    await message.reply('bot is running.')


@app.on_message(filters.command("start") & filters.group)
async def startup(client, message):
    await message.reply("Automatic group name updates started!")
    asyncio.create_task(update_group_names())


@app.on_message(filters.command("stop") & filters.group)
async def stop_auto_update(client, message):
    """Command to stop automatic group name updates."""
    chat_id = message.chat.id
    if chat_id in groups_to_update:
        groups_to_update.remove(chat_id)
        await message.reply("Automatic group name updates stopped!")
    else:
        await message.reply("Automatic updates are not running for this group.")


if __name__ == "__main__":
    print("Bot is running...")
    app.run()
