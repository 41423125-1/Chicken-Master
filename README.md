# Chicken-Master

<img width="1233" height="898" alt="image" src="https://github.com/user-attachments/assets/b4014d9f-020f-4c54-9a7e-988a34c73cce" />

 ##  點擊 [此處打開Chicken-Master](https://41423125-1.github.io/Chicken-Master/)
 大吉大利，今晚吃雞　一天一烤雞，校長遠離我

 # Principle
 

本系統的核心原理是利用 Brython（Browser Python）將 Python 程式直接在瀏覽器端執行，藉由操作 HTML DOM 元素，實現互動式舒肥烹飪計算面板。整體邏輯如下：

### I.Brython 執行層

Brython 將 <script type="text/python"> 內的 Python 程式碼轉譯成 JavaScript，於瀏覽器內執行

透過 from browser import document, timer, window 操作 DOM、定時器與本地儲存

實現完整的 Python 數學計算與邏輯處理能力

### II. 熱力學計算層
系統基於食品科學的熱傳導原理進行精準計算：

核心計算公式：

厚度估算：厚度(cm) = (重量(g) / 密度(1.06g/cm³))^(1/3) × 形狀係數(0.6)

熱傳導時間：t = (厚度/2)² / (π² × 熱擴散係數(1.4e-7 m²/s)) × 保守係數(2.5)

保溫時間：根據目標溫度採用 Douglas Baldwin 的 pasteurization 表進行等效滅菌時間估算

### III. 智慧調整系統
根據使用者選擇的烹飪條件（去骨、切丁、有皮）動態調整厚度與時間估算

醃料用量根據表面積變化自動調整比例

### IV. 即時展示層
計算結果（時間、溫度、醃料比例）即時更新至 HTML 介面

利用 document.createElement 動態生成醃料項目的顯示方格

響應式設計確保在不同設備上的最佳顯示效果

# Functions
模組	功能說明
重量輸入區	使用者輸入雞肉重量 (1-5000g)，作為所有計算的基礎依據
配方選擇區	四種醃料風味：經典原味、香辣風味、香草蒜香、蜜汁甜味，單選切換
溫度設定區	預設熟度選項(60°C-74°C) + 自訂溫度輸入，含安全提醒
烹飪條件備註	多選項：去骨、切丁、有皮，影響時間與醃料計算
計算按鈕	按下後執行熱力學計算，輸出加熱時間、保溫時間與總時間
結果顯示區	顯示詳細的烹飪參數、厚度估算與調整因素說明
醃料建議面板	顯示當前配方的詳細材料用量，根據重量與條件自動調整
# Architecture
整體採用三層架構設計：

### 1. 前端視覺層（HTML + CSS）
HTML 結構劃分：

.card: 主容器，包含所有功能模組

輸入控制區：重量、配方、溫度、備註

結果顯示區：烹飪參數與醃料建議

安全提醒區：USDA 建議與注意事項

CSS 設計特色：

現代化簡潔設計，採用系統字體與自定義色彩變數

響應式網格佈局，適應手機與桌面設備

互動狀態視覺回饋（hover、active、focus）

加載動畫與狀態指示器

### 2. 邏輯運算層（Brython Python）
主要 Python 函數：

函數名稱	功能
estimate_thickness_cm_from_weight_g(w_g)	根據重量估算雞肉厚度
adjust_thickness_based_on_notes(base_thickness)	根據備註條件調整厚度估算
estimate_time_to_reach_core_minutes(thickness_cm)	計算到達核心溫度時間
adjust_time_based_on_notes(base_time)	根據備註條件調整加熱時間
recommend_hold_minutes(temp_c)	推薦保溫滅菌時間
calculate_marinade(weight, recipe_type)	計算醃料各材料用量
create_marinade_details(marinade_data)	動態生成醃料顯示表格
set_active_recipe() / toggle_note()	管理使用者選擇狀態
### 3. 事件處理層
Brython 事件綁定：

配方按鈕點擊事件：單選切換

備註按鈕點擊事件：多選切換

溫度選擇變化事件：顯示/隱藏自訂溫度輸入

計算按鈕點擊事件：觸發完整計算流程

非同步處理：

使用 timer.set_timeout 模擬計算延遲，提供更好的使用者體驗

加載狀態顯示與隱藏

科學基礎
本工具基於以下食品科學原理：

傅立葉熱傳導定律：用於估算熱量從表面傳導至核心的時間

等效滅菌原理：低溫長時間與高溫短時間的滅菌等效性

表面積體積比：影響醃料滲透與熱傳導效率

熱擴散係數：雞肉組織的熱物理特性參數

系統將複雜的食品科學計算封裝成簡單易用的介面，讓使用者能夠精準控制舒肥烹飪過程，同時確保食品安全。
