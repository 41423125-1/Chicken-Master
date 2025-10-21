# Chicken-Master

<img width="1233" height="898" alt="image" src="https://github.com/user-attachments/assets/b4014d9f-020f-4c54-9a7e-988a34c73cce" />

 ##  點擊 [此處打開Chicken-Master](https://41423125-1.github.io/Chicken-Master/)
 大吉大利，今晚吃雞　一天一烤雞，校長遠離我

 # Principle
 

本系統的核心原理是利用 Brython（Browser Python） 將 Python 程式直接在瀏覽器端執行，藉由操作 HTML DOM 元素，實現互動式控制面板
整體邏輯如下：

### I.Brython 執行層

Brython 將 <script type="text/python"> 內的 Python 程式碼轉譯成 JavaScript，於瀏覽器內執行

透過 from browser import document, timer, window 操作 DOM、定時器與本地儲存

### II.資料運算層

使用者輸入雞的重量與選擇的腌料配方後，程式以 Python 計算所需：

各種調味料比例（依雞重量乘以比例係數）

烘烤溫度（根據重量分級）

烘烤時間（以每500克為25分鐘估算）

### III.資料展示層

計算結果（腌料比例、烘烤步驟）會即時更新至 HTML 介面中

利用 document.createElement 動態生成每個腌料項目的顯示方格

狀態儲存與歷史紀錄

每次的烘烤參數結果會保存到 window.localStorage

歷史紀錄可於右側面板查看，支援返回主頁

# Functions


模組	功能說明
1. 重量輸入區	使用者輸入雞重量 (500–5000g)，作為計算依據
2. 配方選擇區	四種腌料風味：Classic、Spicy、Herbal、Sweet，點選切換
3. 計算按鈕	按下後即時計算出腌料比例、烘烤溫度與時間
4. 結果顯示區	顯示腌料詳細表格與烘烤步驟說明
5. 歷史紀錄功能	顯示過去計算的烤雞紀錄，含時間、重量、溫度與配方摘要
6. 控制面板按鈕	模擬控制功能（Start、Temperature、Timer、Recipe）
7. 功能圖示面板	四大模式：Monitor、Recipe、History、Settings，可切換視圖
8. 即時時鐘	每分鐘更新一次當前時間顯示

# Architecture

整體採用三層架構設計：

### 1️.前端視覺層（HTML + CSS）

HTML 結構明確劃分：

.left-section: 控制與輸入功能

.right-section: 結果與歷史紀錄

CSS 採用 深色玻璃質感設計，搭配柔和的漸層與陰影效果，模擬高科技控制面板介面

### 2️. 邏輯運算層（Brython Python）

主要 Python 函數：

### 函數名稱	功能
calculate_marinade(weight, recipe_type)	根據重量與配方，計算各材料比例


calculate_roasting_temperature(weight)	決定烤箱溫度


calculate_roasting_time(weight)	計算烘烤時間


create_marinade_details(data)	動態生成腌料顯示表格


save_to_history() / load_from_history()	與 localStorage 交互，保存與載入紀錄


display_history()	動態生成歷史紀錄項目


set_active_recipe() / set_active_icon()	管理使用者選擇狀態


3️. 資料持久層（localStorage）

以 JSON 形式儲存使用者操作紀錄：自動於頁面載入時恢復歷史資料。

# 特色與延伸應用

1.完全以 Brython 實現 Python 前端互動，無需後端伺服器

2.支援 本地歷史記錄保存

3.架構清晰，可延伸為：智慧烤箱模擬控制系統；食譜管理面板；教學型程式實驗專案（Brython DOM 操作範例）
