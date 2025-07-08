import asyncio
import json
import websockets
from dotenv import load_dotenv
import os

load_dotenv()

INFURA_WSS = os.getenv("INFURA_WSS")

# Souscription aux transactions en attente
SUB_PENDING_TXS = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "eth_subscribe",
    "params": ["newPendingTransactions"],
}

# Souscription aux événements logs de contrats
SUB_SWAP_LOGS = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "eth_subscribe",
    "params": [
        "logs",
        {
            "address": [
                "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",  # Uniswap V2 Factory
                "0xE592427A0AEce92De3Edee1F18E0157C05861564",  # Uniswap V3 Router
            ],
        },
    ],
}


async def listen():
    async with websockets.connect(INFURA_WSS) as ws:
        await ws.send(json.dumps(SUB_PENDING_TXS))
        await ws.send(json.dumps(SUB_SWAP_LOGS))

        print("[📡] Subscribed to mempool and logs.")

        while True:
            msg = await ws.recv()
            print("[🧾] Raw message:", msg)
            data = json.loads(msg)

            if "params" in data and "result" in data["params"]:
                result = data["params"]["result"]
                if "transactionHash" in result:
                    print(f"[⏱] Pending tx: {result['transactionHash']}")
                elif "data" in result:
                    print(f"[🧩] Log event: {result}")
            asyncio.sleep(0.01)  # Yield control to the event loop


if __name__ == "__main__":
    try:
        asyncio.run(listen())
    except KeyboardInterrupt:
        print("\n[❌] Stopping the listener.")
