# 路由設計文件 (ROUTES)

本文件根據功能需求規劃 Flask 的路由設計，包含 URL 路徑、HTTP 方法與對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (食譜列表) | GET | `/` | `index.html` | 顯示所有食譜，支援 `?q=keyword` 關鍵字搜尋 |
| 新增食譜頁面 | GET | `/recipe/new` | `recipe_form.html` | 顯示新增食譜表單 |
| 建立食譜 | POST | `/recipe/new` | — | 接收表單，存入 DB，成功後重導向至首頁 |
| 食譜詳情 | GET | `/recipe/<int:id>` | `recipe_detail.html` | 顯示特定食譜的材料清單與作法 |
| 編輯食譜頁面 | GET | `/recipe/<int:id>/edit`| `recipe_form.html` | 顯示編輯表單，預填原有資料 |
| 更新食譜 | POST | `/recipe/<int:id>/edit`| — | 接收表單，更新 DB，成功後重導向至食譜詳情頁 |
| 刪除食譜 | POST | `/recipe/<int:id>/delete`| — | 刪除指定食譜，成功後重導向至首頁 |

## 2. 每個路由的詳細說明

### `GET /`
- **輸入**：URL Query Parameter `q` (可選，作為搜尋關鍵字)
- **處理邏輯**：查詢 `Recipe` Model。若有 `q` 則加上 `LIKE %keyword%` 條件。
- **輸出**：渲染 `index.html`，傳遞 `recipes` 變數。

### `GET /recipe/new`
- **處理邏輯**：查詢 `Category` Model 以提供分類選項。
- **輸出**：渲染 `recipe_form.html`。

### `POST /recipe/new`
- **輸入**：表單欄位 `title`, `ingredients`, `steps`, `category_id`
- **處理邏輯**：驗證必填欄位。建立 `Recipe` 實例並儲存至資料庫。
- **輸出**：重導向至 `index` 首頁。
- **錯誤處理**：驗證失敗則閃現 (flash) 錯誤訊息，重新渲染表單頁面。

### `GET /recipe/<int:id>`
- **輸入**：URL Path Parameter `id`
- **處理邏輯**：根據 `id` 查詢 `Recipe`，若找不到則回傳 404。
- **輸出**：渲染 `recipe_detail.html`，傳遞 `recipe` 變數。

### `GET /recipe/<int:id>/edit`
- **輸入**：URL Path Parameter `id`
- **處理邏輯**：根據 `id` 查詢 `Recipe`，並查詢所有 `Category` 作為選項。
- **輸出**：渲染 `recipe_form.html`，傳遞 `recipe` 變數以預填資料。

### `POST /recipe/<int:id>/edit`
- **輸入**：表單欄位 `title`, `ingredients`, `steps`, `category_id`
- **處理邏輯**：驗證資料後更新該 `Recipe` 記錄。
- **輸出**：重導向至該食譜的詳情頁。
- **錯誤處理**：驗證失敗則閃現錯誤訊息，重新渲染表單頁面。

### `POST /recipe/<int:id>/delete`
- **處理邏輯**：刪除該 `id` 的 `Recipe` 記錄。
- **輸出**：重導向至 `index` 首頁。

## 3. Jinja2 模板清單

所有模板皆將存放在 `app/templates/` 目錄中。

1. **`base.html`**
   - **說明**：全站共用版型，包含 HTML 骨架、`<head>` 引用、導覽列 (Navbar) 與頁尾 (Footer)。
2. **`index.html`**
   - **繼承自**：`base.html`
   - **說明**：首頁，包含搜尋框與食譜列表。
3. **`recipe_detail.html`**
   - **繼承自**：`base.html`
   - **說明**：單一食譜展示頁，清楚列出材料清單與作法，並提供編輯/刪除按鈕。
4. **`recipe_form.html`**
   - **繼承自**：`base.html`
   - **說明**：共用的表單頁面，依據傳入變數決定是「新增」還是「編輯」模式。
5. **`error.html`** (選用)
   - **繼承自**：`base.html`
   - **說明**：404 或 500 等錯誤提示畫面。
