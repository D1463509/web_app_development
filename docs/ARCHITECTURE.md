# 系統架構文件 (Architecture)

本文件根據產品需求文件 (PRD) 規劃「食譜收藏夾」的系統架構，採用 Python + Flask 開發，並搭配 SQLite 作為輕量級資料庫。

## 1. 技術架構說明

本專案採用典型的 MVC (Model-View-Controller) 架構模式來組織程式碼：

- **選用技術與原因**：
  - **後端框架：Flask (Python)**
    - 輕量、易學且靈活，非常適合個人使用的小型 Web 專案。
  - **資料庫：SQLite + SQLAlchemy (ORM)**
    - SQLite：單檔資料庫，無需額外安裝或設定資料庫伺服器，適合本機單人使用。
    - SQLAlchemy：提供 ORM（物件關聯對映）功能，能用 Python 物件操作資料庫，提升開發效率並防範 SQL Injection。
  - **前端頁面：Jinja2 + Vanilla CSS**
    - Jinja2：Flask 內建的強大模板引擎，能將後端資料無縫渲染至 HTML 頁面，預設具備 XSS 防護。
    - Vanilla CSS：無需編譯流程，直接撰寫 CSS 來打造現代化且響應式的網頁介面。

- **MVC 模式說明**：
  - **Model (資料模型)**：負責定義資料結構（如：食譜、分類）與資料庫互動的邏輯。
  - **View (視圖)**：負責呈現使用者介面，本專案由 Jinja2 模板搭配 HTML/CSS 組成。
  - **Controller (控制器)**：由 Flask 的路由（Routes）負責，接收使用者的 HTTP 請求，處理商業邏輯，並將 Model 資料傳遞給 View 進行渲染。

## 2. 專案資料夾結構

以下為專案的資料夾與檔案組織方式：

```text
web_app_development/
├── app/                      # 應用程式主目錄
│   ├── __init__.py           # Flask 應用程式工廠與初始化設定
│   ├── models.py             # 資料庫模型 (Models - 定義 Recipe, Category 等)
│   ├── routes.py             # Flask 路由控制器 (Controllers)
│   ├── static/               # 靜態資源檔案
│   │   ├── css/              # 樣式表 (style.css)
│   │   ├── js/               # 前端腳本 (如需微互動)
│   │   └── images/           # 圖片資源
│   └── templates/            # Jinja2 網頁模板 (Views)
│       ├── base.html         # 共用版型 (包含導覽列、頁尾)
│       ├── index.html        # 首頁 (食譜列表與搜尋)
│       ├── recipe_detail.html# 食譜詳細內容頁面
│       ├── recipe_form.html  # 新增/編輯食譜的表單頁面
│       └── error.html        # 錯誤提示頁面
├── instance/                 # 本機環境專用資料夾 (不進版控)
│   └── recipe_app.db         # SQLite 資料庫檔案
├── docs/                     # 專案文件
│   ├── PRD.md                # 產品需求文件
│   └── ARCHITECTURE.md       # 系統架構文件 (本文件)
├── app.py                    # 專案執行入口程式
├── requirements.txt          # Python 依賴套件清單
└── README.md                 # 專案說明與執行指南
```

## 3. 元件關係圖

以下展示使用者從瀏覽器操作時，系統各元件的互動流程：

```mermaid
flowchart TD
    Browser[瀏覽器 (Browser)]
    
    subgraph Flask App [Flask 應用程式]
        Router[Flask Route\n(Controller)]
        Model[SQLAlchemy Model\n(Model)]
        Template[Jinja2 Template\n(View)]
    end
    
    Database[(SQLite\n資料庫)]

    %% 使用者發送請求
    Browser -- "1. 發送 HTTP 請求\n(GET / POST)" --> Router
    
    %% Controller 處理邏輯
    Router -- "2. 查詢/寫入資料" --> Model
    Model -- "3. 讀寫操作" --> Database
    Database -- "4. 回傳資料結果" --> Model
    Model -- "5. 將資料物件傳給 Router" --> Router
    
    %% 渲染頁面
    Router -- "6. 傳遞資料與變數" --> Template
    Template -- "7. 渲染 HTML" --> Router
    
    %% 回傳給使用者
    Router -- "8. 回傳 HTTP 回應\n(包含 HTML 內容)" --> Browser
```

## 4. 關鍵設計決策

1. **不採用前後端分離架構 (SSR vs SPA)**
   - **原因**：本專案為輕量級個人工具，無須引入 React/Vue 等前端框架徒增複雜度。由 Flask + Jinja2 進行伺服器端渲染 (SSR) 能最快達到 MVP，且 SEO 友善、開發成本低。
2. **採用 SQLAlchemy 作為資料庫存取層**
   - **原因**：雖然可以直接寫原生 SQL，但使用 SQLAlchemy 能大幅減少重複的 CRUD 程式碼，提升維護性；更重要的是，其自動綁定參數的特性可有效防範 SQL Injection 攻擊。
3. **專案採用 Factory Pattern (應用程式工廠) 結構**
   - **原因**：將 `app/` 獨立作為模組，並透過 `__init__.py` 初始化，有助於未來專案擴充與單元測試。避免將所有程式碼塞在單一 `app.py` 中導致維護困難。
4. **Vanilla CSS 搭配現代化設計**
   - **原因**：不使用 Tailwind 等框架，直接撰寫乾淨的 CSS，保持專案依賴最小化，同時能專注實作高質感的個人化設計體驗（如微動畫與漸層效果）。
