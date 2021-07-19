import asyncio
from bleak import BleakClient

address = "7c:9e:bd:ee:7a:82"
MODEL_NBR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"#"00002a24-0000-1000-8000-00805f9b34fb"
#UUID_NORDIC_TX = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
# async def run(address):
#     async with BleakClient(address) as client:
#         model_number = await client.read_gatt_char(MODEL_NBR_UUID)
#         print("Model Number: {0}".format("".join(map(chr, model_number))))
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(run(address))

#await client.write_gatt_char(UUID_NORDIC_TX, bytearray(user_command[0:20]), True)



async def main(address, loop):
    while True:  # Loop to allow reconnection
        try: # Attempt to connect to ESP32
            print("Connecting\n")
            async with BleakClient(address, loop=loop) as client:
                print("Connected!\n")
                while True: # Main loop, user selects test case
                    print("Trying to get model number")
                    model_number = await client.read_gatt_char(MODEL_NBR_UUID)
                    print("Model Number: {0}".format("".join(map(chr, model_number))))
                break
        except Exception as e: # Catch connection exceptions, usually "device not found," then try to reconnect
            print(e)
            print('Trying to reconnect...')
            continue

if __name__ == "__main__":
    # Create an event loop to run the main coroutine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(address, loop))
