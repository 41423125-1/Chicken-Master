import asyncio
import websockets

async def echo(websocket):  # 只用 websocket
    async for message in websocket:
        await websocket.send(f"收到以下訊息: {message}")

async def main():
    # 使用 handler=echo 並忽略 path
    async with websockets.serve(echo, "localhost", 8765):
        print("WebSocket 伺服器啟動，監聽在 ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())