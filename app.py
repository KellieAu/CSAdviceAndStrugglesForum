from flask import Flask, render_template, url_for, flash, redirect, abort
from config import Config
from models import db, Post
from forms import PostForm

CATEGORIES = ['general', 'CS50', 'CS51', 'CS54', 'CS62', 'CS101', 'CS105', 'CS140']

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.context_processor
def inject_categories():
    return {
        'nav_categories': [
            ('general', 'General'),
            ('CS50', 'CS50'),
            ('CS51', 'CS51'),
            ('CS54', 'CS54'),
            ('CS62', 'CS62'),
            ('CS101', 'CS101'),
            ('CS105', 'CS105'),
            ('CS140', 'CS140'),
        ],
    }

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts=posts)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            post_type=form.post_type.data,
            category=form.category.data,
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been submitted!', 'success')
        return redirect(url_for('home'))
    return render_template('submit.html', form=form)

@app.route('/category/<category_name>')
def category_page(category_name):
    if category_name not in CATEGORIES:
        abort(404)
    posts = Post.query.filter_by(category=category_name).order_by(Post.date_posted.desc()).all()
    title = 'General' if category_name == 'general' else category_name
    return render_template('category.html', posts=posts, title=title, category_name=category_name)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)