from browser import document, html, timer
from random import randint
from brython_robot import World, AnimatedRobot, CELL_SIZE, IMG_PATH

# 初始化世界與機器人
world = World(10, 10)
robot = AnimatedRobot(world, 1, 1)

carrots = []        # 所有 carrot 的座標
body = []           # 車廂節點的座標
train_length = 0    # 車廂長度（收過幾個 carrot）
current_path = []   # 機器人預計要走的路線
is_moving = False   # 標誌，用來避免重複啟動移動

def place_carrot():
    """隨機放一顆 carrot 在空地上，並確保不會與機器人或身體重疊"""
    # 這裡不再使用 while True，改用非同步的 set_timeout 來尋找位置
    def find_empty_spot():
        x = randint(0, world.width - 1)
        y = randint(0, world.height - 1)
        
        # 檢查新座標是否與機器人或身體重疊
        if (x, y) != (robot.x, robot.y) and (x, y) not in body and (x, y) not in carrots:
            carrots.append((x, y))
            ctx = world.layers["objects"].getContext("2d")
            world._draw_image(ctx, IMG_PATH + "carrot.png", x, y, CELL_SIZE, CELL_SIZE)
        else:
            # 如果不符合條件，稍後再試，將控制權交還給瀏覽器
            timer.set_timeout(find_empty_spot, 10)
    
    find_empty_spot()

def draw_all():
    """重新繪製所有物件，包括蘿蔔和機器人身體"""
    ctx = world.layers["objects"].getContext("2d")
    ctx.clearRect(0, 0, world.width * CELL_SIZE, world.height * CELL_SIZE)

    for x, y in carrots:
        world._draw_image(ctx, IMG_PATH + "carrot.png", x, y, CELL_SIZE, CELL_SIZE)

    for (x, y) in body:
        world._draw_image(ctx, IMG_PATH + "carrot.png", x, y, CELL_SIZE, CELL_SIZE)
        
def bfs_path(start, goal, obstacles, callback):
    """使用非同步 BFS 尋找路徑"""
    from collections import deque
    
    queue = deque()
    queue.append((start, []))
    visited = set()
    visited.add(start)

    directions = {
        "E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1)
    }

    def process_queue():
        # 每個幀只處理一定數量的節點，避免阻塞
        nodes_to_process = 50 
        for _ in range(nodes_to_process):
            if not queue:
                # 找不到路徑，回傳空列表
                callback([])
                return
            
            (x, y), path = queue.popleft()
            if (x, y) == goal:
                callback(path)
                return

            for dir, (dx, dy) in directions.items():
                nx, ny = x + dx, y + dy
                if 0 <= nx < world.width and 0 <= ny < world.height:
                    if (nx, ny) not in visited and (nx, ny) not in obstacles:
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [dir]))
        
        # 處理完當前幀的節點後，將控制權交還，並排程下一個處理
        timer.set_timeout(process_queue, 10)

    # 開始執行非同步 BFS
    process_queue()

def get_path_to_target(target, callback):
    """取得從機器人到目標的安全路徑，避開身體"""
    head = (robot.x, robot.y)
    obstacles = set(body)
    bfs_path(head, target, obstacles, callback)

def move_path():
    """依序執行路徑中的每一個移動步驟"""
    global is_moving, train_length

    if not current_path:
        is_moving = False
        if (robot.x, robot.y) in carrots:
            carrots.remove((robot.x, robot.y))
            train_length += 1
        draw_all()
        place_carrot()
        timer.set_timeout(seek_and_collect, 500)
        return

    next_direction = current_path.pop(0)

    def move_and_update():
        def on_move_complete():
            body.insert(0, (robot.x, robot.y))
            if len(body) > train_length:
                body.pop()
            draw_all()
            timer.set_timeout(move_path, 200)

        if robot.facing != next_direction:
            robot.turn_left()
            timer.set_timeout(move_and_update, 300)
        else:
            robot.move(1)
            robot.queue.append(lambda done: on_move_complete() or done())
            robot._run_queue()

    move_and_update()

def seek_and_collect():
    """尋找最近的 carrot 並開始移動"""
    global current_path, is_moving

    if is_moving:
        return

    if not carrots:
        place_carrot()
        timer.set_timeout(seek_and_collect, 500)
        return

    min_dist = float('inf')
    target = None
    for c in carrots:
        dist = abs(c[0] - robot.x) + abs(c[1] - robot.y)
        if dist < min_dist:
            min_dist = dist
            target = c
    
    if target:
        # 這裡改用回調函式來處理非同步的 BFS 結果
        def on_path_found(path):
            if not path:
                print("⚠️ 無法到達 carrot，跳過此回合")
                timer.set_timeout(seek_and_collect, 500)
                return
            
            global current_path, is_moving
            current_path = path
            is_moving = True
            move_path()

        get_path_to_target(target, on_path_found)
    else:
        timer.set_timeout(seek_and_collect, 500)

# 啟動
place_carrot()
timer.set_timeout(seek_and_collect, 500)