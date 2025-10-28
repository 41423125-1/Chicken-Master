# server_ipv6.py
import asyncio, ssl, json, websockets

# ------------------------------------------------------------------
# 1. SSL context (self-signed is fine for local testing)
# ------------------------------------------------------------------
ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_ctx.load_cert_chain("cert.pem", "key.pem")   # <-- make sure these files exist

# ------------------------------------------------------------------
# 2. WebSocket handler
# ------------------------------------------------------------------
async def handler(ws):
    print("Client connected")
    try:
        async for msg in ws:
            data = json.loads(msg)
            cmd  = data.get("command", "")
            print(f"Received: {cmd}")
            await ws.send(json.dumps({"command": cmd}))
    except websockets.ConnectionClosed:
        print("Client disconnected")

# ------------------------------------------------------------------
# 3. Main – start the server *inside* an async function
# ------------------------------------------------------------------
async def main():
    host = "[2001:b011:d006:1349:c956:1cec:b46b:8ad1]"   # **no brackets**
    async with websockets.serve(handler, host=host, port=8765, ssl=ssl_ctx) as server:
        print(f"Server listening on wss://[{host}]:8765")
        await asyncio.Future()   # run forever

if __name__ == "__main__":
    asyncio.run(main())