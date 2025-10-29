import asyncio
import websockets
import ssl

async def echo(websocket):
    async for message in websocket:
        await websocket.send(f"收到以下訊息: {message}")

async def main():
    # SSL 設定
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    # 綁定到 [::] 表示同時支援 IPv6 和 IPv4（雙棧）
    # 也可以用 host="::" 或 host="0.0.0.0"（僅 IPv4）
    async with websockets.serve(
        echo,
        host="::",          # 關鍵：IPv6 雙棧監聽
        port=8765,
        ssl=ssl_context,    # 啟用 wss
        family=socket.AF_INET6  # 強制使用 IPv6 地址族（可選）
    ):
        print("WebSocket 伺服器啟動，監聽在 wss://[::1]:8765")
        print("也支援 wss://127.0.0.1:8765 (IPv4 映射)")
        await asyncio.Future()

if __name__ == "__main__":
    import socket  # 確保 socket 被 import
    asyncio.run(main())