# remote_client_local.py （測試用）
import asyncio, websockets, json, keyboard, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

async def send(cmd):
    uri = "wss://127.0.0.1:8765"  # 改用 localhost
    print(f"正在連線到 {uri}...")
    try:
        async with websockets.connect(uri, ssl=ssl_ctx) as ws:
            await ws.send(json.dumps({"command": cmd}))
            print(f"Sent: {cmd}")
    except Exception as e:
        print(f"連線失敗: {e}")

async def main():
    print("j=move, i=turn_left, q=quit")
    while True:
        if keyboard.is_pressed('q'): break
        if keyboard.is_pressed('j'):
            await send("move")
            await asyncio.sleep(0.3)
        if keyboard.is_pressed('i'):
            await send("turn_left")
            await asyncio.sleep(0.3)
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    asyncio.run(main())