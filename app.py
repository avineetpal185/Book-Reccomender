from flask import Flask, render_template, request
import pickle
import numpy as np
import os
import sys
import numpy

# 🔥 FIX: numpy pickle compatibility (VERY IMPORTANT)
sys.modules['numpy._core'] = numpy.core

app = Flask(__name__)

# ✅ Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))


# ✅ Lazy loading (fix memory crash on Render)
def load_popular():
    return pickle.load(open(os.path.join(base_dir, 'popular.pkl'), 'rb'))

def load_pt():
    return pickle.load(open(os.path.join(base_dir, 'pt.pkl'), 'rb'))

def load_books():
    return pickle.load(open(os.path.join(base_dir, 'books.pkl'), 'rb'))

def load_similarity():
    return pickle.load(open(os.path.join(base_dir, 'similarity_scores.pkl'), 'rb'))


# ✅ Home Page
@app.route('/')
def index():
    try:
        popular_df = load_popular()

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
        user_input = request.form.get('user_input')

        if not user_input:
            return render_template('recommend.html', data=[])

        user_input = user_input.strip().lower()

        # load only when needed
        pt = load_pt()
        books = load_books()
        similarity_scores = load_similarity()

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
