import asyncio
import websockets
import ssl
import json
import keyboard
import socket
import sys # 引入 sys 模組用於 sys.exit

connected_clients = set()
# 用於接收到 'q' 鍵時發出停止訊號
stop_event = asyncio.Event() 

# 必須接收 websocket, path
async def handler(websocket, path):
    # websockets 函式庫已處理 WebSocket 握手，
    # handler 函式只有在握手成功後才會被呼叫。
    # 因此，不需要手動檢查 Upgrade 頭部來拒絕非 WebSocket 請求。

    print(f"WebSocket 客戶端連線請求來自: {websocket.remote_address}")
    connected_clients.add(websocket)
    print(f"WebSocket 客戶端已連線: {websocket.remote_address}，目前連線數: {len(connected_clients)}")

    try:
        async for message in websocket:
            print(f"收到來自 {websocket.remote_address} 的訊息: {message}")
            # 你可以在這裡處理收到的訊息，例如解析 JSON 並執行相應動作
            # try:
            #     data = json.loads(message)
            #     print(f"解析後資料: {data}")
            #     # 根據 data 執行機器人操作
            #     # 範例：如果客戶端發送 "status_request"，你可以回傳當前狀態
            #     if data.get("type") == "status_request":
            #         await websocket.send(json.dumps({"status": "ready", "clients_online": len(connected_clients)}))
            # except json.JSONDecodeError:
            #     print(f"收到非 JSON 格式訊息: {message}")
            # except Exception as e:
            #     print(f"處理訊息時發生錯誤: {e}")

    except websockets.exceptions.ConnectionClosedOK:
        print(f"客戶端正常斷線: {websocket.remote_address}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"客戶端非正常斷線: {websocket.remote_address}, 錯誤: {e}")
    except Exception as e:
        print(f"連線錯誤: {websocket.remote_address} - {e}")
    finally:
        # 確保在任何情況下都將客戶端從集合中移除
        if websocket in connected_clients:
            connected_clients.discard(websocket)
            print(f"客戶端已移除: {websocket.remote_address}，目前連線數: {len(connected_clients)}")


async def send_command(cmd):
    if not connected_clients:
        print("無客戶端連線，無法發送指令")
        return

    message = json.dumps({"cmd": cmd})
    
    # 建立一個靜態的客戶端列表，以便在發送期間對其進行迭代
    # 這可以避免在 asyncio.gather 執行期間，connected_clients 集合發生變化導致的問題
    clients_to_send_to = list(connected_clients) 
    
    # 使用 asyncio.gather 同步發送給所有客戶端，並處理可能發生的錯誤
    results = await asyncio.gather(
        *(client.send(message) for client in clients_to_send_to),
        return_exceptions=True  # 即使部分發送失敗，也不會中斷 gather
    )

    sent_count = 0
    failed_clients_info = []
    clients_to_remove = []

    # 遍歷結果，處理成功和失敗的情況
    for client, res in zip(clients_to_send_to, results):
        if isinstance(res, Exception):
            # 發送失敗，記錄錯誤訊息並標記客戶端可能需要移除
            failed_clients_info.append(f"{client.remote_address} - {res}")
            # 如果是連線關閉的錯誤，則將其標記為待移除
            if isinstance(res, (websockets.exceptions.ConnectionClosedOK, websockets.exceptions.ConnectionClosedError)):
                clients_to_remove.append(client)
        else:
            sent_count += 1
            
    # 從 connected_clients 集合中移除已斷線的客戶端
    for client in clients_to_remove:
        if client in connected_clients:
            connected_clients.discard(client)
            print(f"已從連線列表中移除斷線客戶端: {client.remote_address}")

    print(f"已發送指令 '{cmd}' 給 {sent_count} 個客戶端。")
    if failed_clients_info:
        print(f"其中 {len(failed_clients_info)} 個客戶端發送失敗，詳情如下：")
        for info in failed_clients_info:
            print(f"  - {info}")
        print(f"目前連線數: {len(connected_clients)}")


async def keyboard_listener():
    print("\n=== 控制說明 ===")
    print("按 j 前進（留軌跡）")
    print("按 k 前進（無軌跡）")
    print("按 i 左轉")
    print("按 q 退出程式")
    print("==============\n")
    
    # 持續監聽，直到停止事件被設定
    while not stop_event.is_set():
        if keyboard.is_pressed('j'):
            await send_command("move")
            await asyncio.sleep(0.3) # 簡短的延遲以避免重複發送
        elif keyboard.is_pressed('k'):
            await send_command("move2")
            await asyncio.sleep(0.3)
        elif keyboard.is_pressed('i'):
            await send_command("turn_left")
            await asyncio.sleep(0.3)
        elif keyboard.is_pressed('q'):
            print("\n收到退出指令 'q'。正在準備關閉程式...")
            stop_event.set() # 設定停止事件，通知其他任務關閉
            break # 退出鍵盤監聽迴圈
        
        # 讓出控制權，避免佔用 CPU 過多。
        # 這裡的 keyboard.is_pressed() 是同步的，頻繁調用可能會消耗 CPU。
        # asyncio.sleep 允許事件迴圈處理其他任務。
        await asyncio.sleep(0.05) 
    print("鍵盤監聽器已停止。")


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 連接到外部伺服器以獲取本地 IP
        s.connect(("8.8.8.8", 80)) 
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1" # 如果無法連接外部網路，則使用本地回環地址
    finally:
        s.close()
    return ip


async def main():
    server = None # 初始化 server 變數
    listener_task = None # 初始化 listener_task 變數
    ssl_context = None # 初始化 ssl_context 變數
    use_ssl = False # 標誌是否使用 SSL

    try:
        # SSL 設定
        # 建立 SSL context
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # 載入您的 SSL 憑證和私鑰檔案
        # 請確保 'server.crt' 和 'server.key' 檔案存在於相同目錄
        # 或者提供完整的路徑
        try:
            ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")
            print("SSL 憑證載入成功。伺服器將使用 WSS (安全 WebSocket) 運行。")
            use_ssl = True
        except FileNotFoundError:
            print("警告：找不到 server.crt 或 server.key 檔案。伺服器將不使用 SSL，以 WS (非安全 WebSocket) 模式運行。")
        except Exception as e:
            print(f"警告：載入 SSL 憑證時發生錯誤: {e}。伺服器將不使用 SSL，以 WS (非安全 WebSocket) 模式運行。")

        local_ip = get_local_ip()
        port = 8765
        
        # 根據 use_ssl 決定是否傳遞 ssl 參數
        start_server = websockets.serve(
            handler,
            local_ip,
            port,
            ssl=ssl_context if use_ssl else None # 條件式傳遞 ssl_context)
     