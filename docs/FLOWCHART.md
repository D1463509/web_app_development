# 流程圖文件 (Flowchart)

本文件根據產品需求文件 (PRD) 與系統架構文件 (ARCHITECTURE)，定義「食譜收藏夾」系統的使用者操作路徑與系統資料流動方式。

## 1. 使用者流程圖 (User Flow)

此流程圖描述使用者在系統中可能進行的各種操作路徑，涵蓋食譜的瀏覽、新增、編輯、刪除以及搜尋。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 食譜列表]
    
    Home --> Action{要執行什麼操作？}
    
    %% 瀏覽與搜尋
    Action -->|搜尋關鍵字| Search[過濾出符合條件的食譜] --> Home
    Action -->|點擊特定食譜| Detail[食譜詳細內容頁面]
    
    %% 新增食譜
    Action -->|點擊新增食譜| CreateForm[填寫新增食譜表單]
    CreateForm -->|送出表單| SaveNew[儲存資料] --> Home
    
    %% 編輯與刪除食譜
    Detail --> DetailAction{對此食譜的操作}
    DetailAction -->|點擊編輯| EditForm[填寫編輯食譜表單]
    EditForm -->|送出更新| SaveEdit[更新資料] --> Detail
    
    DetailAction -->|點擊刪除| ConfirmDelete[確認刪除]
    ConfirmDelete -->|確定| DeleteData[刪除資料] --> Home
    
    %% 列出材料 (包含在詳細內容頁面)
    DetailAction -->|瀏覽內容| ViewIngredients[查看材料清單與作法]
```

## 2. 系統序列圖 (Sequence Diagram)

以下以「新增食譜」功能為例，展示從使用者填寫表單到資料庫寫入完成的完整系統互動過程：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route (Controller)
    participant Model as SQLAlchemy (Model)
    participant DB as SQLite 資料庫

    User->>Browser: 在「新增食譜」頁面填寫標題、材料與作法並點擊送出
    Browser->>Flask: 發送 POST 請求 (/recipe/new) 包含表單資料
    
    activate Flask
    Flask->>Model: 驗證資料並建立 Recipe 物件
    activate Model
    Model->>DB: 執行 INSERT INTO recipes ...
    activate DB
    DB-->>Model: 回傳寫入成功與新記錄 ID
    deactivate DB
    Model-->>Flask: 回傳 Recipe 物件
    deactivate Model
    
    Flask-->>Browser: 回傳 HTTP 302 Redirect (導向至首頁或詳細頁)
    deactivate Flask
    
    Browser->>Flask: 發送 GET 請求 (重新載入首頁)
    Flask->>Model: 查詢最新食譜列表
    Model->>DB: SELECT * FROM recipes
    DB-->>Model: 回傳資料表紀錄
    Model-->>Flask: 回傳列表物件
    Flask-->>Browser: 渲染並回傳首頁 HTML
```

## 3. 功能清單對照表

下表列出系統中的主要功能、對應的 URL 路徑規劃以及 HTTP 方法，為後續實作 API 設計與 Flask 路由的基礎。

| 功能名稱 | URL 路徑規劃 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **首頁 (食譜列表)** | `/` | GET | 顯示所有已收藏的食譜列表，若有加上 `?q=keyword` 則顯示搜尋結果。 |
| **新增食譜 (表單)** | `/recipe/new` | GET | 渲染新增食譜的 HTML 表單頁面。 |
| **新增食譜 (送出)** | `/recipe/new` | POST | 接收新增食譜的表單資料並存入資料庫。 |
| **食譜詳細資訊** | `/recipe/<id>` | GET | 顯示特定食譜的完整材料清單與作法。 |
| **編輯食譜 (表單)** | `/recipe/<id>/edit` | GET | 渲染編輯食譜的 HTML 表單頁面，並預填原有資料。 |
| **編輯食譜 (送出)** | `/recipe/<id>/edit` | POST | 接收編輯食譜的表單資料並更新至資料庫。 |
| **刪除食譜** | `/recipe/<id>/delete` | POST | 將特定食譜從資料庫中刪除 (通常透過表單送出 POST 請求)。 |
