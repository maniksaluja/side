from telethon import TelegramClient, events, errors
import asyncio
import time

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone_number = 'YOUR_PHONE_NUMBER'
channel_id = 'YOUR_CHANNEL_ID'

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Flood control variables
request_limit = 10  # Number of requests to approve per minute
time_limit = 60  # Time window in seconds
pending_approvals = []

async def approve_requests():
    async with client:
        try:
            async for request in client.get_participants(channel_id, filter=telethon.tl.types.ChannelParticipantsBanned):
                if len(pending_approvals) >= request_limit:
                    print('Flood control: waiting before approving more requests')
                    await asyncio.sleep(time_limit)
                    pending_approvals.clear()

                print(f'Approving {request.id}')
                await client.edit_admin(channel_id, request.id, is_admin=False, change_info=False)
                pending_approvals.append(request.id)
                time.sleep(3)  # Adding delay to avoid being flagged for spam

        except errors.FloodWaitError as e:
            print(f'Flood control triggered. Waiting for {e.seconds} seconds.')
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f'An error occurred: {e}')

async def main():
    await client.start(phone=phone_number)
    await approve_requests()

client.loop.run_until_complete(main())
