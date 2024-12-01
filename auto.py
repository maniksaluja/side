import asyncio
from telethon import TelegramClient, errors

# Bot API credentials
api_id = '27566180'
api_hash = '22ff768b386252d2c7a8867361fa9941'
bot_token = '7823661833:AAH7DsVQv2F2fw1E3dWhEzqorYGcNynSfyY'
channel_id = -1002210532935  # Replace with your private channel ID

# Initialize Telegram client
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# Flood control settings
REQUEST_LIMIT = 10  # Number of approvals per minute
DELAY_BETWEEN_REQUESTS = 3  # Delay between each approval


async def approve_join_requests():
    print("Approving pending join requests...")
    approved_count = 0

    try:
        async for request in client.get_chat_join_requests(channel_id):
            if approved_count >= REQUEST_LIMIT:
                print("Flood control: Waiting to avoid rate limits...")
                await asyncio.sleep(60)  # Respect Telegram's rate limits
                approved_count = 0  # Reset the counter

            try:
                print(f"Approving request from: {request.user_id}")
                await client.approve_chat_join_request(channel_id, request.user_id)
                approved_count += 1
                await asyncio.sleep(DELAY_BETWEEN_REQUESTS)  # Delay to prevent spam
            except errors.FloodWaitError as e:
                print(f"Flood control triggered! Waiting for {e.seconds} seconds...")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"Error while approving request: {e}")

    except Exception as e:
        print(f"Failed to fetch or approve requests: {e}")


async def main():
    print("Bot started!")
    await approve_join_requests()


if __name__ == "__main__":
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
