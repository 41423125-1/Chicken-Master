import tkinter as tk
import os
import random
import json

# 全域常數
CELL_SIZE = 40
WALL_THICKNESS = 6

# 指定的世界設定，以 JSON 格式直接嵌入在程式碼中
# This is the world configuration provided by the user.
DEFAULT_SCENE = {
    "robots": [{
        "x": 5,
        "y": 1,
        "orientation": 1,
        "objects": {
            "carrot": "infinite"
        }
    }],
    "walls": {
        "10,1": ["east"],
        "10,2": ["east"],
        "10,3": ["east"],
        "10,4": ["east"],
        "10,5": ["east"],
        "10,6": ["east"],
        "10,7": ["east"],
        "10,8": ["east"],
        "10,9": ["east"],
        "10,10": ["east", "north"],
        "9,10": ["north"],
        "8,10": ["north"],
        "7,10": ["north"],
        "6,10": ["north"],
        "5,10": ["north"],
        "4,10": ["north"],
        "3,10": ["north"],
        "2,10": ["north"],
        "1,10": ["north"]
    },
    "goal": {
        "objects": {}
    },
    "objects": {
        "5,3": {
            "carrot": 5
        },
        "5,4": {
            "carrot": 1
        },
        "5,5": {
            "carrot": 4
        },
        "5,6": {
            "carrot": 3
        },
        "5,7": {
            "carrot": 2
        },
        "5,8": {
            "carrot": 1
        },
        "4,8": {
            "carrot": 1
        },
        "4,7": {
            "carrot": 1
        },
        "4,6": {
            "carrot": 1
        },
        "4,5": {
            "carrot": 1
        },
        "4,4": {
            "carrot": 1
        },
        "4,3": {
            "carrot": 1
        },
        "6,8": {
            "carrot": 1
        },
        "6,7": {
            "carrot": 1
        },
        "6,6": {
            "carrot": 1
        },
        "6,5": {
            "carrot": 1
        },
        "6,4": {
            "carrot": 1
        },
        "6,3": {
            "carrot": 1
        },
        "7,8": {
            "carrot": 1
        },
        "7,7": {
            "carrot": 1
        },
        "7,6": {
            "carrot": 1
        },
        "7,5": {
            "carrot": 1
        },
        "7,4": {
            "carrot": 1
        },
        "8,7": {
            "carrot": 1
        },
        "8,6": {
            "carrot": 1
        },
        "8,5": {
            "carrot": 1
        },
        "3,8": {
            "carrot": 1
        },
        "3,7": {
            "carrot": 1
        },
        "3,6": {
            "carrot": 1
        },
        "3,5": {
            "carrot": 1
        },
        "3,4": {
            "carrot": 1
        },
        "8,8": {
            "carrot": 1
        },
        "8,4": {
            "carrot": 1
        },
        "7,3": {
            "carrot": 1
        },
        "3,3": {
            "carrot": 1
        },
        "8,3": {
            "carrot": 1
        }
    }
}

# 請將此路徑更改為您的圖片檔案位置
# 預設使用相對於執行腳本的 images/ 目錄
IMG_DIR = os.path.join(os.path.dirname(__file__), 'images')

class World:
    """
    這個類別負責建立和管理 Tkinter 視窗及畫布，模擬 Reeborg 的世界。
    """
    def __init__(self, width, height, scene_data):
        self.width = width
        self.height = height
        self.scene_data = scene_data
        self.root = tk.Tk()
        self.root.title("Tkinter Reeborg Patrol")
        
        # 建立一個單一畫布
        self.canvas = tk.Canvas(
            self.root,
            width=self.width * CELL_SIZE,
            height=self.height * CELL_SIZE,
            bg="#f0f0f0"
        )
        self.canvas.pack()
        
        self.robot_image_cache = {}
        self.wall_image_cache = {}
        self.carrot_image_cache = None
        self.carrot_count_image_cache = {}
        self.objects = {}
        self.walls = {}
        
        self._load_images()
        self._parse_scene_data()
        self._draw_grid()
        self._draw_walls()
        self.draw_objects()
        
        robot_start_x = self.scene_data["robots"][0]["x"]
        robot_start_y = self.scene_data["robots"][0]["y"]
        robot_start_orientation = self.scene_data["robots"][0]["orientation"]
        self.robot = SmartRobot(self, robot_start_x, robot_start_y, robot_start_orientation)
        
        # 建立控制按鈕
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        move_button = tk.Button(button_frame, text="前進 (I)", command=lambda: self.robot.move(1))
        move_button.pack(side=tk.LEFT, padx=5)
        
        backward_button = tk.Button(button_frame, text="後退 (M)", command=lambda: self.robot.backward())
        backward_button.pack(side=tk.LEFT, padx=5)
        
        turn_left_button = tk.Button(button_frame, text="左轉 (J)", command=lambda: self.robot.turn_left())
        turn_left_button.pack(side=tk.LEFT, padx=5)
        
        turn_right_button = tk.Button(button_frame, text="右轉 (K)", command=lambda: self.robot.turn_right())
        turn_right_button.pack(side=tk.LEFT, padx=5)
        
        pick_button = tk.Button(button_frame, text="採集 (P)", command=lambda: self.robot.pick_carrot())
        pick_button.pack(side=tk.LEFT, padx=5)

        # 綁定鍵盤事件
        self.root.bind('<Key>', self._on_key_press)
        
    def _on_key_press(self, event):
        """根據按下的按鍵控制機器人。"""
        key = event.char.lower()
        if key == 'i':
            self.robot.move(1)
        elif key == 'm':
            self.robot.backward()
        elif key == 'j':
            self.robot.turn_left()
        elif key == 'k':
            self.robot.turn_right()
        elif key == 'p':
            self.robot.pick_carrot()
    
    def _parse_scene_data(self):
        """解析 JSON 數據並填充世界物件。"""
        self.objects = { (int(x), int(y)): data for key, data in self.scene_data.get("objects", {}).items() for x, y in [key.split(',')] }
        self.walls = self.scene_data.get("walls", {})

    def _load_images(self):
        """同步載入所有需要的圖片，並將其存入快取。"""
        try:
            # 機器人圖片
            for direction in ["e", "n", "w", "s"]:
                img_path = os.path.join(IMG_DIR, f"blue_robot_{direction}.png")
                self.robot_image_cache[direction.upper()] = tk.PhotoImage(file=img_path)
            
            # 牆壁圖片
            self.wall_image_cache["north"] = tk.PhotoImage(file=os.path.join(IMG_DIR, "north.png"))
            self.wall_image_cache["east"] = tk.PhotoImage(file=os.path.join(IMG_DIR, "east.png"))
            
            # 胡蘿蔔圖片
            self.carrot_image_cache = tk.PhotoImage(file=os.path.join(IMG_DIR, "carrot.png"))
            
            # 胡蘿蔔計數圖片
            for i in range(1, 6):
                img_path = os.path.join(IMG_DIR, f"{i}_t.png")
                self.carrot_count_image_cache[i] = tk.PhotoImage(file=img_path)

        except tk.TclError as e:
            print(f"🚨 無法載入圖片。請檢查 '{IMG_DIR}' 目錄中是否有所有必要的 .png 檔案。")
            print(f"詳細錯誤: {e}")
            self.root.destroy()
            return
            
    def _draw_grid(self):
        """繪製世界上的網格線。"""
        for i in range(self.width + 1):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, self.height * CELL_SIZE, fill="#cccccc")
        for j in range(self.height + 1):
            self.canvas.create_line(0, j * CELL_SIZE, self.width * CELL_SIZE, j * CELL_SIZE, fill="#cccccc")

    def _draw_image(self, image, x, y, offset_x=0, offset_y=0, tag=None):
        """
        在畫布上繪製圖片。
        x, y 是網格座標，繪製時需要轉換為像素座標。
        """
        # 將 Brython 的座標系 (左下角為 0,0) 轉換為 Tkinter 的座標系 (左上角為 0,0)
        px = x * CELL_SIZE + offset_x
        py = (self.height - 1 - y) * CELL_SIZE + offset_y
        
        return self.canvas.create_image(px, py, anchor=tk.NW, image=image, tags=tag)

    def _draw_walls(self):
        """繪製世界的邊界牆。"""
        north_img = self.wall_image_cache["north"]
        east_img = self.wall_image_cache["east"]
        
        # 繪製 JSON 中指定的牆
        for key, directions in self.walls.items():
            x, y = map(int, key.split(','))
            for direction in directions:
                if direction == "north":
                    self._draw_image(north_img, x - 1, y - 1, offset_y=0)
                elif direction == "east":
                    self._draw_image(east_img, x - 1, y - 1, offset_x=CELL_SIZE - WALL_THICKNESS)
    
    def draw_objects(self):
        """繪製世界中的所有物件，如胡蘿蔔。"""
        self.canvas.delete("objects") # 清除舊物件
        for (x, y), data in self.objects.items():
            if "carrot" in data and data["carrot"] > 0:
                # 在網格中心繪製胡蘿蔔
                self._draw_image(self.carrot_image_cache, x - 1, y - 1, tag="objects")
                
                # 繪製胡蘿蔔數量
                if isinstance(data["carrot"], int):
                    num_to_draw = min(data["carrot"], 5)
                    count_img = self.carrot_count_image_cache.get(num_to_draw)
                    if count_img:
                        self._draw_image(count_img, x - 1, y - 1, 
                                         offset_x=CELL_SIZE - 20, offset_y=CELL_SIZE - 35,
                                         tag="objects")
                
class BaseRobot:
    """
    此類別負責管理機器人的狀態、動作佇列及動畫。
    """
    def __init__(self, world, x, y, orientation):
        self.world = world
        self.x = x - 1
        self.y = y - 1
        self.facing_order = ["E", "N", "W", "S"]
        self.facing = self.facing_order[orientation]
        self.robot_id = None
        self.queue = []
        self.running = False

    def _draw_robot(self):
        """清除舊機器人圖片並在新的位置和方向繪製它。"""
        self.world.canvas.delete("robot") # 清除所有帶有"robot"標籤的物件
        
        img = self.world.robot_image_cache[self.facing]
        self.robot_id = self.world._draw_image(img, self.x, self.y, tag="robot")
    
    def _draw_trace(self, from_x, from_y, to_x, to_y):
        """繪製從舊位置到新位置的追蹤線。"""
        # 轉換座標系
        fx = from_x * CELL_SIZE + CELL_SIZE / 2
        fy = (self.world.height - 1 - from_y) * CELL_SIZE + CELL_SIZE / 2
        tx = to_x * CELL_SIZE + CELL_SIZE / 2
        ty = (self.world.height - 1 - to_y) * CELL_SIZE + CELL_SIZE / 2
        
        self.world.canvas.create_line(fx, fy, tx, ty, fill="#d33", width=2)
    
    def move(self, steps, on_complete):
        """將移動動作加入佇列。"""
        def action(next_done):
            def step():
                nonlocal steps
                if steps == 0:
                    next_done()
                    return
                
                from_x, from_y = self.x, self.y
                dx, dy = 0, 0
                if self.facing == "E": dx = 1
                elif self.facing == "W": dx = -1
                elif self.facing == "N": dy = 1
                elif self.facing == "S": dy = -1
                
                next_x, next_y = self.x + dx, self.y + dy
                
                # 邊界檢查
                if 0 <= next_x < self.world.width and 0 <= next_y < self.world.height:
                    self.x, self.y = next_x, next_y
                    self._draw_trace(from_x, from_y, self.x, self.y)
                    self._draw_robot()
                    steps -= 1
                    self.world.canvas.after(200, step)
                else:
                    print("🚨 已經撞牆，停止移動！")
                    next_done()
                    
            step()
        
        self.queue.append(action)
        self._run_queue(on_complete)
    
    def backward(self, on_complete):
        """將後退動作加入佇列。"""
        def action(next_done):
            from_x, from_y = self.x, self.y
            dx, dy = 0, 0
            if self.facing == "E": dx = -1
            elif self.facing == "W": dx = 1
            elif self.facing == "N": dy = -1
            elif self.facing == "S": dy = 1
            
            next_x, next_y = self.x + dx, self.y + dy
            
            if 0 <= next_x < self.world.width and 0 <= next_y < self.world.height:
                self.x, self.y = next_x, next_y
                self._draw_trace(from_x, from_y, self.x, self.y)
                self._draw_robot()
                self.world.canvas.after(200, next_done)
            else:
                print("🚨 已經撞牆，停止移動！")
                next_done()
        
        self.queue.append(action)
        self._run_queue(on_complete)
    
    def turn_left(self, on_complete):
        """將向左轉動作加入佇列。"""
        def action(done):
            idx = self.facing_order.index(self.facing)
            self.facing = self.facing_order[(idx + 1) % 4]
            self._draw_robot()
            self.world.canvas.after(300, done)
        
        self.queue.append(action)
        self._run_queue(on_complete)

    def turn_right(self, on_complete):
        """將向右轉動作加入佇列。"""
        def action(done):
            idx = self.facing_order.index(self.facing)
            self.facing = self.facing_order[(idx - 1) % 4]
            self._draw_robot()
            self.world.canvas.after(300, done)
        
        self.queue.append(action)
        self._run_queue(on_complete)

    def _run_queue(self, on_complete):
        """執行佇列中的下一個動作。"""
        if self.running or not self.queue:
            if on_complete:
                on_complete()
            return
        
        self.running = True
        action = self.queue.pop(0)
        action(lambda: self._done(on_complete))

    def _done(self, on_complete):
        """標記動作完成，並嘗試執行佇列中的下一個動作。"""
        self.running = False
        self._run_queue(on_complete)

class SmartRobot:
    """
    此類別擴充了基礎機器人，增加了狀態管理和新功能。
    """
    def __init__(self, world, x, y, orientation):
        self.world = world
        self.base = BaseRobot(world, x, y, orientation)
        self.carrots_collected = 0
        self._draw_robot()

    def _draw_robot(self):
        """同步狀態並重新繪製機器人及胡蘿蔔計數。"""
        self.base._draw_robot()
        
        if self.carrots_collected > 0:
            num = min(self.carrots_collected, 5)
            img = self.world.carrot_count_image_cache.get(num)
            if img:
                self.world._draw_image(img, self.base.x, self.base.y, 
                                        offset_x=CELL_SIZE - 20, offset_y=CELL_SIZE - 35,
                                        tag="robot")

    def move(self, steps=1):
        self.base.move(steps, self._draw_robot)

    def backward(self):
        self.base.backward(self._draw_robot)

    def turn_left(self):
        self.base.turn_left(self._draw_robot)

    def turn_right(self):
        self.base.turn_right(self._draw_robot)

    def pick_carrot(self):
        """檢查機器人位置是否有胡蘿蔔，並進行採集。"""
        current_pos = (self.base.x + 1, self.base.y + 1)
        cell_data = self.world.scene_data["objects"].get(f"{current_pos[0]},{current_pos[1]}", {})
        
        if "carrot" in cell_data:
            carrot_count = cell_data["carrot"]
            
            if isinstance(carrot_count, int) and carrot_count > 0:
                self.carrots_collected += 1
                cell_data["carrot"] -= 1
                if cell_data["carrot"] == 0:
                    del self.world.scene_data["objects"][f"{current_pos[0]},{current_pos[1]}"]
                self.world.draw_objects()
                self._draw_robot()
                print(f"採收成功！目前總數: {self.carrots_collected}")
            elif carrot_count == "infinite":
                self.carrots_collected += 1
                self._draw_robot()
                print(f"採收成功！目前總數: {self.carrots_collected}")
        else:
            print("這裡沒有胡蘿蔔！")


# 主程式區塊
if __name__ == "__main__":
    world_width = 10
    world_height = 10
    
    w = World(world_width, world_height, DEFAULT_SCENE)
    
    # 啟動 Tkinter 主迴圈
    w.root.mainloop()
