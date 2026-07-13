import asyncio
import time

async def fetch_data(url):
    print(f"Fetching data from {url}...")
    await asyncio.sleep(2) # Simulate a network request
    print(f"Finished fetching data from {url}.")
    return "Data from " + url

async def main():
    start_time = time.time()

    tasks = [
        fetch_data("website A"),
        fetch_data("website B"),
        fetch_data("website C")
    ]

    await asyncio.gather(*tasks) # Run tasks concurrently

    print(f"All data fetched in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())