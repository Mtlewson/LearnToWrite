import asyncio
from bleak import BleakClient

address = "7c:9e:bd:ee:7a:82"
MODEL_NBR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"#"00002a24-0000-1000-8000-00805f9b34fb"
UUID_NORDIC_TX = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
async def run(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
