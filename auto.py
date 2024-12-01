from telethon import TelegramClient, errors
import asyncio

# API credentials
api_id = '26422364'
api_hash = '06fb2da75e57d0c2027cafefdacdfd70'
phone_number = '+959783844005'
channel_id = -1002210532935  # Use as integer to avoid conversion issues

# Initialize Telegram client
client = TelegramClient('manik', api_id, api_hash)

# Flood control variables
REQUEST_LIMIT = 10  # Number of requests allowed per window
TIME_WINDOW = 60  # Time window in seconds (1 minute)
DELAY_BETWEEN_REQUESTS = 3  # Delay between approvals in seconds


async def approve_requests():
    async with client:
        approved_count = 0  # Track approved requests in the current window

        try:
            async for request in client.iter_participants(
                channel_id, filter=client.types.ChannelParticipantsBanned
            ):
                if approved_count >= REQUEST_LIMIT:
                    print(f"Flood control: Pausing for {TIME_WINDOW} seconds...")
                    await asyncio.sleep(TIME_WINDOW)
                    approved_count = 0  # Reset counter after time window

                print(f"Approving request from user ID: {request.id}")
                try:
                    await client.edit_admin(
                        channel_id,
                        request.id,
                        is_admin=False,
                        change_info=False,
                    )
                    approved_count += 1
                    await asyncio.sleep(DELAY_BETWEEN_REQUESTS)  # Respect API limits
                except errors.FloodWaitError as e:
                    print(f"Flood control triggered! Waiting for {e.seconds} seconds...")
                    await asyncio.sleep(e.seconds)  # Wait for flood timeout
                except Exception as e:
                    print(f"Error approving request: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")


async def main():
    await client.start(phone=phone_number)
    print("Client started. Approving requests...")
    await approve_requests()


if __name__ == "__main__":
    client.loop.run_until_complete(main())
