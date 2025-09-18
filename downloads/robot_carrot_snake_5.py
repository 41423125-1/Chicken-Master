from browser import document, html, timer
from random import randint
from brython_robot import World, AnimatedRobot, CELL_SIZE, IMG_PATH
from collections import deque

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
    def find_empty_spot():
        x = randint(0, world.width - 1)
        y = randint(0, world.height - 1)
        
        if (x, y) != (robot.x, robot.y) and (x, y) not in body and (x, y) not in carrots:
            carrots.append((x, y))
            ctx = world.layers["objects"].getContext("2d")
            world._draw_image(ctx, IMG_PATH + "carrot.png", x, y, CELL_SIZE, CELL_SIZE)
        else:
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
        
def bfs_path(start, goal, obstacles):
    """使用 BFS 尋找從 start 到 goal 的路徑，避開 obstacles"""
    queue = deque()
    queue.append((start, []))  # (位置, 路徑)
    visited = set()
    visited.add(start)

    directions = [("E", (1, 0)), ("W", (-1, 0)), ("N", (0, 1)), ("S", (0, -1))]

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path  # 回傳方向序列

        for dir, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < world.width and 0 <= ny < world.height:
                if (nx, ny) not in visited and (nx, ny) not in obstacles:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [dir]))

    return []  # 找不到路徑

def get_path_to_target(target):
    """取得從機器人到目標的安全路徑，避開身體"""
    head = (robot.x, robot.y)
    obstacles = set(body)
    return bfs_path(head, target, obstacles)

def find_safe_move():
    """尋找一個不撞到自己身體的移動方向"""
    directions = [("E", (1, 0)), ("W", (-1, 0)), ("N", (0, 1)), ("S", (0, -1))]
    head = (robot.x, robot.y)
    obstacles = set(body)
    
    # 優先選擇最短的自由路徑
    safe_paths = []
    for dir, (dx, dy) in directions:
        next_pos = (head[0] + dx, head[1] + dy)
        if 0 <= next_pos[0] < world.width and 0 <= next_pos[1] < world.height and next_pos not in obstacles:
            # 找到一條通往地圖邊緣的安全路徑
            path_to_wall = bfs_path(next_pos, (dx + (world.width-1), dy + (world.height-1)), obstacles)
            if path_to_wall:
                safe_paths.append((len(path_to_wall), dir))

    if safe_paths:
        safe_paths.sort()
        return [safe_paths[0][1]]
        
    # 如果找不到通往地圖邊緣的路徑，就尋找任何一個不撞到自己的方向
    for dir, (dx, dy) in directions:
        next_pos = (head[0] + dx, head[1] + dy)
        if 0 <= next_pos[0] < world.width and 0 <= next_pos[1] < world.height and next_pos not in obstacles:
            return [dir]
    
    return []

def move_path():
    """依序執行路徑中的每一個移動步驟"""
    global is_moving, train_length, carrots
    
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

    # 找到離機器人最近且可到達的蘿蔔
    min_dist = float('inf')
    target = None
    best_path = []
    
    for c in carrots:
        path = get_path_to_target(c)
        if path:
            dist = len(path)
            if dist < min_dist:
                min_dist = dist
                target = c
                best_path = path

    if best_path:
        current_path = best_path
        is_moving = True
        move_path()
    else:
        # 如果所有蘿蔔都無法到達，尋找一條安全路徑來移動
        print("⚠️ 無法找到可到達的 carrot，尋找安全路徑來移動。")
        current_path = find_safe_move()
        if current_path:
            is_moving = True
            move_path()
        else:
            # 如果連安全路徑都找不到，這意味著機器人被完全堵死
            print("❌ 無法找到任何安全路徑，機器人被困住了！")
            is_moving = False

# 啟動
place_carrot()
timer.set_timeout(seek_and_collect, 500)