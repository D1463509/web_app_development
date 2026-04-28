from flask import Blueprint, render_template, request, redirect, url_for, flash

# 建立 Blueprint 物件
main_bp = Blueprint('main', __name__)
recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipe')

@main_bp.route('/')
def index():
    """
    首頁：顯示食譜列表
    輸入：支援 ?q=keyword 進行標題搜尋
    處理：查詢 Recipe Model
    輸出：渲染 index.html，傳遞 recipes 變數
    """
    pass

@recipe_bp.route('/new', methods=['GET', 'POST'])
def create_recipe():
    """
    新增食譜
    GET: 查詢分類並渲染 recipe_form.html 顯示表單
    POST: 接收表單資料，驗證後寫入資料庫，成功則重導回首頁
    """
    pass

@recipe_bp.route('/<int:id>')
def recipe_detail(id):
    """
    食譜詳情
    輸入：食譜 ID
    處理：根據 ID 查詢食譜，若找不到則報 404
    輸出：渲染 recipe_detail.html，顯示詳細材料與作法
    """
    pass

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """
    編輯食譜
    GET: 根據 ID 查詢食譜，渲染 recipe_form.html，預填原有資料
    POST: 接收表單資料更新資料庫，成功則重導回詳情頁
    """
    pass

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除食譜
    接收 POST 請求，刪除該 ID 食譜，完成後重導回首頁
    """
    pass
