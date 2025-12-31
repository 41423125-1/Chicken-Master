# app.py （Windows 修正版）
import asyncio, ssl, json, threading
from flask import Flask, render_template
from flask_sockets import Sockets
import websockets

app = Flask(__name__)
sockets = Sockets(app)

# SSL Context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("cert.pem", "key.pem")

# WebSocket 處理器
async def ws_handler(ws):
    print("[WS 8765] 客戶端連入")
    try:
        async for msg in ws:
            data = json.loads(msg)
            cmd = data.get("command")
            print(f"[WS 8765] 收到: {cmd}")
            await ws.send(json.dumps({"action": cmd}))
    except websockets.ConnectionClosed:
        print("[WS 8765] 斷線")

# 啟動內部 WebSocket（給 Flask 代理）
async def start_inner_ws():
    await websockets.serve(
        ws_handler,
        host="127.0.0.1",
        port=8765,
        ssl=ssl_context
    )
    print("內部 WebSocket 127.0.0.1:8765 啟動")
    await asyncio.Future()

# 啟動公開 WebSocket（給遠端 client）
async def start_public_ws():
    # 同時監聽 IPv4 和 IPv6
    await websockets.serve(
        ws_handler,
        host="0.0.0.0",      # IPv4
        port=8765,
        ssl=ssl_context
    )
    await websockets.serve(
        ws_handler,
        host="::",           # IPv6
        port=8765,
        ssl=ssl  # 這是關鍵！
    )
    print("公開 WebSocket 0.0.0.0:8765 與 [::]:8765 啟動")
    await asyncio.Future()

# Flask 代理 /ws
@sockets.route('/ws')
def proxy_ws(ws):
    async def run():
        async with websockets.connect("wss://127.0.0.1:8765", ssl=ssl_context) as backend:
            async def c2s():
                while True:
                    m = await ws.receive()
                    if m is None: break
                    await backend.send(m)
            async def s2c():
                while True:
                    m = await backend.recv()
                    await ws.send(m)
            await asyncio.gather(c2s(), s2c())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())

# Brython 頁面
@app.route('/brython')
def brython_page():
    return render_template('brython.html')

# 啟動 WebSocket 伺服器
def start_ws_servers():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.gather(start_inner_ws(), start_public_ws())
    loop.run_forever()

threading.Thread(target=start_ws_servers, daemon=True).start()

# 主程式
if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(
        ('', 9442),  # 監聽所有介面
        app,
        handler_class=WebSocketHandler,
        ssl_context=ssl_context
    )
    print("Flask 啟動於 https://[你的IPv6]:9442/brython")
    print("遠端 client 連 wss://[你的IPv6]:8765")
    server.serve_forever()