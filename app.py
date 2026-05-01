from flask import Flask, render_template, request
import pickle
import numpy as np
import os
import sys
import numpy

# 🔥 FIX: numpy pickle compatibility
sys.modules['numpy._core'] = numpy.core

app = Flask(__name__)

# ✅ Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# 🔥 GLOBAL CACHE (VERY IMPORTANT)
popular_df = None
pt = None
books = None
similarity_scores = None

# 🔥 LOAD DATA ONLY ONCE
def load_data():
    global popular_df, pt, books, similarity_scores

    if popular_df is None:
        popular_df = pickle.load(open(os.path.join(base_dir, 'popular.pkl'), 'rb'))

    if pt is None:
        pt = pickle.load(open(os.path.join(base_dir, 'pt.pkl'), 'rb'))

    if books is None:
        books = pickle.load(open(os.path.join(base_dir, 'books.pkl'), 'rb'))

    if similarity_scores is None:
        similarity_scores = pickle.load(open(os.path.join(base_dir, 'similarity_scores.pkl'), 'rb'))


# ✅ Home Page
@app.route('/')
def index():
    try:
        load_data()

        return render_template(
            'index.html',
            book_name=list(popular_df['Book-Title'].values),
            author=list(popular_df['Book-Author'].values),
            image=list(popular_df['Image-URL-M'].values),
            votes=list(popular_df['num_ratings'].values),
            rating=list(popular_df['avg_rating'].values)
        )
    except Exception as e:
        return f"Error loading homepage: {e}"


# ✅ Recommendation UI
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


# ✅ Recommendation Logic
@app.route('/recommend_books', methods=['POST'])
def recommend():
    try:
        load_data()

        user_input = request.form.get('user_input')

        if not user_input:
            return render_template('recommend.html', data=[])

        user_input = user_input.strip().lower()

        pt_index = pt.index.str.lower()

        if user_input not in pt_index:
            return render_template('recommend.html', data=[])

        index = np.where(pt_index == user_input)[0][0]

        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:9]

        data = []

        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]

            item = []
            item.append(temp_df['Book-Title'].values[0])
            item.append(temp_df['Book-Author'].values[0])
            item.append(temp_df['Image-URL-M'].values[0])

            data.append(item)

        return render_template('recommend.html', data=data)

    except Exception as e:
        print("RECOMMEND ERROR:", e)
        return render_template('recommend.html', data=[])


# ✅ Deployment config
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
