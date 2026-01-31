from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-123' # 公開時は変更してください
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bbs.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- データベースモデル ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    threads = db.relationship('Thread', backref='board', lazy=True)

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    posts = db.relationship('Post', backref='thread', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    user = db.relationship('User', backref='posts')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ルート定義 ---

@app.route('/')
def index():
    boards = Board.query.all()
    return render_template('index.html', boards=boards)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('既に存在するユーザー名です')
            return redirect(url_for('register'))
        new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('ログインに失敗しました')
    return render_template('register.html') # 登録と兼用

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/board/<int:board_id>')
def view_board(board_id):
    board = Board.query.get_or_404(board_id)
    return render_template('board.html', board=board)

@app.route('/board/<int:board_id>/new_thread', methods=['POST'])
@login_required
def create_thread(board_id):
    title = request.form.get('title')
    content = request.form.get('content')
    new_thread = Thread(title=title, board_id=board_id)
    db.session.add(new_thread)
    db.session.flush()
    first_post = Post(content=content, thread_id=new_thread.id, user_id=current_user.id)
    db.session.add(first_post)
    db.session.commit()
    return redirect(url_for('view_board', board_id=board_id))

# --- app.py の view_thread 関数内 ---

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('ログインが必要です')
            return redirect(url_for('login'))
            
        content = request.form.get('content')
        parent_id = request.form.get('parent_id')
        
        # 空の投稿を防ぐ
        if not content:
            return redirect(url_for('view_thread', thread_id=thread_id))

        # 数値変換の安全策
        p_id = int(parent_id) if parent_id and parent_id.isdigit() else None

        new_post = Post(
            content=content, 
            thread_id=thread_id, 
            user_id=current_user.id, 
            parent_id=p_id
        )
        
        db.session.add(new_post)
        db.session.commit()  # <--- ここでエラーが出ていないか、保存されているか確認
        
        return redirect(url_for('view_thread', thread_id=thread_id))
    
    return render_template('thread.html', thread=thread)
# 初期データ投入
with app.app_context():
    db.create_all()
    if not Board.query.first():
        db.session.add_all([Board(title='ニュース'), Board(title='テクノロジー'), Board(title='雑談')])
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)