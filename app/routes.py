from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Recipe, Category

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
    query = request.args.get('q', '').strip()
    if query:
        # 進行簡單的模糊搜尋
        recipes = Recipe.query.filter(Recipe.title.ilike(f'%{query}%')).order_by(Recipe.created_at.desc()).all()
    else:
        recipes = Recipe.get_all()
        
    return render_template('index.html', recipes=recipes, search_query=query)

@recipe_bp.route('/new', methods=['GET', 'POST'])
def create_recipe():
    """
    新增食譜
    GET: 查詢分類並渲染 recipe_form.html 顯示表單
    POST: 接收表單資料，驗證後寫入資料庫，成功則重導回首頁
    """
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        category_id = request.form.get('category_id')

        # 簡單驗證
        if not title or not ingredients or not steps:
            flash('標題、材料與作法為必填欄位！', 'danger')
            # 發生錯誤時保留使用者輸入，方便修改
            # 這裡建立一個臨時字典來模擬 recipe 物件傳給模板
            temp_recipe = {
                'title': title, 
                'ingredients': ingredients, 
                'steps': steps, 
                'category_id': int(category_id) if category_id and category_id.isdigit() else None
            }
            return render_template('recipe_form.html', categories=Category.get_all(), recipe=temp_recipe)

        # 準備資料字典
        data = {
            'title': title,
            'ingredients': ingredients,
            'steps': steps,
            'category_id': int(category_id) if category_id and category_id.isdigit() else None
        }

        recipe = Recipe.create(data)
        if recipe:
            flash('新增食譜成功！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('新增食譜發生錯誤，請稍後再試。', 'danger')

    categories = Category.get_all()
    return render_template('recipe_form.html', categories=categories, recipe=None)

@recipe_bp.route('/<int:id>')
def recipe_detail(id):
    """
    食譜詳情
    輸入：食譜 ID
    處理：根據 ID 查詢食譜，若找不到則報 404
    輸出：渲染 recipe_detail.html，顯示詳細材料與作法
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
    return render_template('recipe_detail.html', recipe=recipe)

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """
    編輯食譜
    GET: 根據 ID 查詢食譜，渲染 recipe_form.html，預填原有資料
    POST: 接收表單資料更新資料庫，成功則重導回詳情頁
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)

    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        category_id = request.form.get('category_id')

        # 簡單驗證
        if not title or not ingredients or not steps:
            flash('標題、材料與作法為必填欄位！', 'danger')
            # 使用者送出錯誤時，將錯誤的資料塞回物件讓畫面呈現
            recipe.title = title
            recipe.ingredients = ingredients
            recipe.steps = steps
            recipe.category_id = int(category_id) if category_id and category_id.isdigit() else None
            return render_template('recipe_form.html', categories=Category.get_all(), recipe=recipe)

        data = {
            'title': title,
            'ingredients': ingredients,
            'steps': steps,
            'category_id': int(category_id) if category_id and category_id.isdigit() else None
        }

        if Recipe.update(id, data):
            flash('更新食譜成功！', 'success')
            return redirect(url_for('recipe.recipe_detail', id=id))
        else:
            flash('更新食譜發生錯誤，請稍後再試。', 'danger')

    categories = Category.get_all()
    return render_template('recipe_form.html', categories=categories, recipe=recipe)

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除食譜
    接收 POST 請求，刪除該 ID 食譜，完成後重導回首頁
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
        
    if Recipe.delete(id):
        flash('刪除食譜成功！', 'success')
    else:
        flash('刪除食譜失敗，請稍後再試。', 'danger')
        
    return redirect(url_for('main.index'))
