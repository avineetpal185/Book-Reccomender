from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# ✅ Base directory (IMPORTANT for deployment)
base_dir = os.path.dirname(os.path.abspath(__file__))

# ✅ Load data using correct path
popular_df = pickle.load(open(os.path.join(base_dir, 'popular.pkl'), 'rb'))
pt = pickle.load(open(os.path.join(base_dir, 'pt.pkl'), 'rb'))
books = pickle.load(open(os.path.join(base_dir, 'books.pkl'), 'rb'))
similarity_scores = pickle.load(open(os.path.join(base_dir, 'similarity_scores.pkl'), 'rb'))

@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        rating=list(popular_df['avg_rating'].values)
    )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    if not user_input:
        return render_template('recommend.html', data=[])

    user_input = user_input.strip()

    if user_input not in pt.index:
        return render_template('recommend.html', data=[])

    index = np.where(pt.index == user_input)[0][0]

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


# ✅ IMPORTANT FOR DEPLOYMENT
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
