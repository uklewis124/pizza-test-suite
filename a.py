import asyncio
from playwright.async_api import async_playwright

URL = "https://kanbanpizza.onrender.com"  # Change to your target URL
ROOM_NAME = "not-a-ddos"  # Base room name
CLIENT_COUNT = 100


async def simulate_client(client_id):
    room_number = client_id // 5
    print(f"Client {client_id}: Allocated to room number {room_number}")

    async with async_playwright() as p:
        print("Booting browser for client ", client_id)
        browser = await p.chromium.launch(channel="msedge", headless=True)
        print(f"Client {client_id}: Loaded Microsoft Edge")
        page = await browser.new_page()
        print(f"Client {client_id}: Opened New Page")

        try:
            await page.goto(URL)
            print(f"Client {client_id}: Loaded page")

            await page.fill("#room-input", f"{ROOM_NAME} - {room_number}")
            print(f"Client {client_id}: Entered Room Information")
            await page.press("#room-input", "Enter")

            if client_id % 3 == 0:
                await page.screenshot(path=f"screenshots-for-adam/before-button/{client_id}.png")

            try:
                await page.click("#start-round")
            except:
                print(f"Client {client_id}: Start Round button not Found")

            print(f"Client {client_id}: Submitted room name")

            if client_id % 3 == 0:            
                await page.screenshot(path=f"screenshots-for-adam/after-button/{client_id}.png", full_page=True)

            await asyncio.sleep(180)  # THIS ONE RUNS FOR (x) SECONDS
            #await asyncio.Event().wait() # THIS ONE RUNS FOREVER
        except Exception as e:
            print(f"Client {client_id} error: {e}")

        finally:
            print(f"Client {client_id}: Closing Connection")
            await browser.close()

async def main():
    print("Collecting clients")
    clients = [simulate_client(i) for i in range(CLIENT_COUNT)]
    await asyncio.gather(*clients)

if __name__ == "__main__":
    asyncio.run(main())