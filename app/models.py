from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    recipes = db.relationship('Recipe', backref='category', lazy=True)
    
    def __repr__(self):
        return f"<Category {self.name}>"

    @classmethod
    def create(cls, data):
        """
        新增一筆分類記錄
        :param data: 包含 'name' 的字典
        :return: 成功回傳 Category 物件，失敗回傳 None
        """
        try:
            new_category = cls(name=data.get('name'))
            db.session.add(new_category)
            db.session.commit()
            return new_category
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating category: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有分類記錄
        :return: Category 物件的列表
        """
        try:
            return cls.query.order_by(cls.name).all()
        except Exception as e:
            logging.error(f"Error getting categories: {e}")
            return []

    @classmethod
    def get_by_id(cls, category_id):
        """
        取得單筆分類記錄
        :param category_id: 分類 ID
        :return: Category 物件，若無則回傳 None
        """
        try:
            return db.session.get(cls, category_id)
        except Exception as e:
            logging.error(f"Error getting category by id: {e}")
            return None

    @classmethod
    def update(cls, category_id, data):
        """
        更新分類記錄
        :param category_id: 分類 ID
        :param data: 包含 'name' 的字典
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            category = cls.get_by_id(category_id)
            if category:
                if 'name' in data:
                    category.name = data['name']
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating category: {e}")
            return False

    @classmethod
    def delete(cls, category_id):
        """
        刪除分類記錄
        :param category_id: 分類 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            category = cls.get_by_id(category_id)
            if category:
                db.session.delete(category)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting category: {e}")
            return False


class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Recipe {self.title}>"

    @classmethod
    def create(cls, data):
        """
        新增一筆食譜記錄
        :param data: 包含 'title', 'ingredients', 'steps', 'category_id' 的字典
        :return: 成功回傳 Recipe 物件，失敗回傳 None
        """
        try:
            new_recipe = cls(
                title=data.get('title'),
                ingredients=data.get('ingredients'),
                steps=data.get('steps'),
                category_id=data.get('category_id') or None
            )
            db.session.add(new_recipe)
            db.session.commit()
            return new_recipe
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating recipe: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有食譜記錄
        :return: Recipe 物件的列表
        """
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            logging.error(f"Error getting recipes: {e}")
            return []

    @classmethod
    def get_by_id(cls, recipe_id):
        """
        取得單筆食譜記錄
        :param recipe_id: 食譜 ID
        :return: Recipe 物件，若無則回傳 None
        """
        try:
            return db.session.get(cls, recipe_id)
        except Exception as e:
            logging.error(f"Error getting recipe by id: {e}")
            return None

    @classmethod
    def update(cls, recipe_id, data):
        """
        更新食譜記錄
        :param recipe_id: 食譜 ID
        :param data: 包含要更新的欄位的字典
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            recipe = cls.get_by_id(recipe_id)
            if recipe:
                if 'title' in data:
                    recipe.title = data['title']
                if 'ingredients' in data:
                    recipe.ingredients = data['ingredients']
                if 'steps' in data:
                    recipe.steps = data['steps']
                if 'category_id' in data:
                    recipe.category_id = data['category_id'] or None
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating recipe: {e}")
            return False

    @classmethod
    def delete(cls, recipe_id):
        """
        刪除食譜記錄
        :param recipe_id: 食譜 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            recipe = cls.get_by_id(recipe_id)
            if recipe:
                db.session.delete(recipe)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting recipe: {e}")
            return False
