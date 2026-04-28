import re

from flask import Flask, render_template, url_for, flash, redirect, abort, request
from config import Config
from models import db, Post
from forms import PostForm, VideoForm
from urllib.parse import urlparse, parse_qs

CATEGORIES = ['general', 'CS50', 'CS51', 'CS54', 'CS62', 'CS101', 'CS105', 'CS140']
NAV_TABS = [
    ('general', 'General'),
    ('CS50', 'CS50'),
    ('CS51', 'CS51'),
    ('CS54', 'CS54'),
    ('CS62', 'CS62'),
    ('CS101', 'CS101'),
    ('CS105', 'CS105'),
    ('CS140', 'CS140'),
    ('video', 'Video Advice from Alumni'),
]

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.context_processor
def inject_categories():
    return {
        'nav_tabs': NAV_TABS,
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

# def get_youtube_embed_url(url):
#     patterns = [
#         r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)',
#         r'(?:https?://)?(?:www\.)?youtu\.be/([^?&]+)',
#         r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^?&]+)',
#     ]
#     for pattern in patterns:
#         match = re.search(pattern, url)
#         if match:
#             return f'https://www.youtube.com/embed/{match.group(1)}'
#     return None

# @app.route('/video', methods=['GET', 'POST'])
# def video_advice():
#     form = VideoForm()
#     embed_url = None
#     if form.validate_on_submit():
#         embed_url = get_youtube_embed_url(form.youtube_url.data.strip())
#         if not embed_url:
#             flash('Enter a valid YouTube video URL.', 'danger')
#     return render_template('videos.html', form=form, embed_url=embed_url, active_tab='video')
@app.route('/video-advice', methods=['GET', 'POST'])
def video_advice():
    form = VideoForm()
    embed_url = None
    original_url = None

    if form.validate_on_submit():
        original_url = form.youtube_url.data
        embed_url = convert_to_embed(original_url)

    return render_template('videos.html',
                           form=form,
                           embed_url=embed_url,
                           original_url=original_url)


def convert_to_embed(url):
    """Convert any YouTube URL format to an embed URL."""
    try:
        parsed = urlparse(url)

        # Standard: https://www.youtube.com/watch?v=VIDEO_ID
        if 'youtube.com' in parsed.netloc:
            params = parse_qs(parsed.query)
            if 'v' in params:
                video_id = params['v'][0]
                return f"https://www.youtube.com/embed/{video_id}?rel=0"

        # Short: https://youtu.be/VIDEO_ID
        elif 'youtu.be' in parsed.netloc:
            video_id = parsed.path.lstrip('/')
            return f"https://www.youtube.com/embed/{video_id}?rel=0"

        return None  # unrecognized format

    except Exception:
        return None

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