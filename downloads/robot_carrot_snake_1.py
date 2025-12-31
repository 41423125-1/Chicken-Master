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
    while True:
        x = randint(0, world.width - 1)
        y = randint(0, world.height - 1)
        # 檢查新座標是否與機器人或身體重疊
        if (x, y) != (robot.x, robot.y) and (x, y) not in body and (x, y) not in carrots:
            carrots.append((x, y))
            ctx = world.layers["objects"].getContext("2d")
            world._draw_image(ctx, IMG_PATH + "carrot.png", x, y, CELL_SIZE, CELL_SIZE)
            break

def draw_all():
    """重新繪製所有物件，包括蘿蔔和機器人身體"""
    ctx = world.layers["objects"].getContext("2d")
    ctx.clearRect(0, 0, world.width * CELL_SIZE, world.height * CELL_SIZE)

    for x, y in carrots:
        world._draw_image(ctx, IMG_PATH + "carrot.png", x, y, CELL_SIZE, CELL_SIZE)
    
    # 畫出機器人身體
    for (x, y) in body:
        world._draw_image(ctx, IMG_PATH + "carrot.png", x, y, CELL_SIZE, CELL_SIZE)

def get_path_to_target(target):
    """計算從機器人目前位置到目標的路徑（只走直線），並返回一個包含方向的列表"""
    path = []
    tx, ty = target
    
    # 先在 x 軸上移動
    if robot.x != tx:
        dx = tx - robot.x
        direction = "E" if dx > 0 else "W"
        for _ in range(abs(dx)):
            path.append(direction)
    
    # 再在 y 軸上移動
    if robot.y != ty:
        dy = ty - robot.y
        direction = "N" if dy > 0 else "S"
        for _ in range(abs(dy)):
            path.append(direction)
            
    return path

def move_path():
    """依序執行路徑中的每一個移動步驟"""
    global is_moving, train_length

    if not current_path:
        # 路徑已走完，抵達目標
        is_moving = False
        
        # 採集蘿蔔，更新身體長度
        if (robot.x, robot.y) in carrots:
            carrots.remove((robot.x, robot.y))
            train_length += 1
        
        draw_all()
        place_carrot()
        timer.set_timeout(seek_and_collect, 500)
        return

    # 取得下一個方向
    next_direction = current_path.pop(0)

    # 定義轉向和移動的串聯動作
    def move_and_update():
        def on_move_complete():
            # 更新身體節點
            body.insert(0, (robot.x, robot.y))
            if len(body) > train_length:
                body.pop()
            draw_all()
            # 延遲後繼續下一個步驟
            timer.set_timeout(move_path, 200)

        # 確保機器人轉向正確
        if robot.facing != next_direction:
            robot.turn_left()
            timer.set_timeout(move_and_update, 300) # 轉向需要時間
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

    # 如果沒有蘿蔔，就生成一個並等待
    if not carrots:
        place_carrot()
        timer.set_timeout(seek_and_collect, 500)
        return

    # 找到離機器人最近的蘿蔔
    min_dist = float('inf')
    target = None
    for c in carrots:
        dist = abs(c[0] - robot.x) + abs(c[1] - robot.y)
        if dist < min_dist:
            min_dist = dist
            target = c
    
    if target:
        current_path = get_path_to_target(target)
        is_moving = True
        move_path()
    else:
        timer.set_timeout(seek_and_collect, 500)

# 啟動
place_carrot()
timer.set_timeout(seek_and_collect, 500)