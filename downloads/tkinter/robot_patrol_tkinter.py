import tkinter as tk
import os

# 全域常數
CELL_SIZE = 40
WALL_THICKNESS = 6

# 請將此路徑更改為您的圖片檔案位置
# 預設使用相對於執行腳本的 images/ 目錄
IMG_DIR = os.path.join(os.path.dirname(__file__), 'images')

# 如果您要使用絕對路徑，請取消註解並修改下一行
#IMG_DIR = r"Y:\tmp\images"

class World:
    """
    這個類別負責建立和管理 Tkinter 視窗及畫布，模擬 Reeborg 的世界。
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = tk.Tk()
        self.root.title("Tkinter Reeborg Patrol")
        
        # 建立一個單一畫布來取代多個 HTML canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.width * CELL_SIZE,
            height=self.height * CELL_SIZE,
            bg="#f0f0f0"
        )
        self.canvas.pack()
        
        self.robot_image_cache = {}
        self.wall_image_cache = {}
        
        self._load_images()
        self._draw_grid()
        self._draw_walls()
        
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
        
        # 使用 center 錨點讓圖片定位更精確
        return self.canvas.create_image(px, py, anchor=tk.NW, image=image, tags=tag)

    def _draw_walls(self):
        """繪製世界的邊界牆。"""
        north_img = self.wall_image_cache["north"]
        east_img = self.wall_image_cache["east"]
        
        for x in range(self.width):
            # 北牆 (最上方)
            self._draw_image(north_img, x, self.height - 1, offset_y=0)
            # 南牆 (最下方)
            self._draw_image(north_img, x, 0, offset_y=CELL_SIZE - WALL_THICKNESS)
        
        for y in range(self.height):
            # 西牆 (最左邊)
            self._draw_image(east_img, 0, y, offset_x=0)
            # 東牆 (最右邊)
            self._draw_image(east_img, self.width - 1, y, offset_x=CELL_SIZE - WALL_THICKNESS)
        
class AnimatedRobot:
    """
    此類別負責管理機器人的狀態、動作佇列及動畫。
    """
    def __init__(self, world, x, y):
        self.world = world
        self.x = x - 1
        self.y = y - 1
        self.facing = "E"
        self.facing_order = ["E", "N", "W", "S"]
        self.robot_id = None
        self.queue = []
        self.running = False
        self._draw_robot()

    def _draw_robot(self):
        """清除舊機器人圖片並在新的位置和方向繪製它。"""
        if self.robot_id:
            self.world.canvas.delete(self.robot_id)
        
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
    
    def move(self, steps):
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
                    # 使用 after 模擬非同步延遲
                    self.world.canvas.after(200, step)
                else:
                    print("🚨 已經撞牆，停止移動！")
                    next_done()
                    
            step() # 啟動第一個步驟
        
        self.queue.append(action)
        self._run_queue()
    
    def turn_left(self):
        """將向左轉動作加入佇列。"""
        def action(done):
            idx = self.facing_order.index(self.facing)
            self.facing = self.facing_order[(idx + 1) % 4]
            self._draw_robot()
            # 使用 after 模擬非同步延遲
            self.world.canvas.after(300, done)
        
        self.queue.append(action)
        self._run_queue()

    def _run_queue(self):
        """執行佇列中的下一個動作。"""
        if self.running or not self.queue:
            return
        
        self.running = True
        action = self.queue.pop(0)
        # 使用 lambda 函數作為回呼，在動作完成後啟動下一個動作
        action(lambda: self._done())

    def _done(self):
        """標記動作完成，並嘗試執行佇列中的下一個動作。"""
        self.running = False
        self._run_queue()

# 主程式區塊
if __name__ == "__main__":
    w = World(10, 10)
    
    r = AnimatedRobot(w, 1, 1)
    
    r.move(9)
    r.turn_left()
    r.move(9)
    r.turn_left()
    r.move(9)
    r.turn_left()
    r.move(9)
    
    # 啟動 Tkinter 事件迴圈，開始運行程式
    w.root.mainloop()
