import os
import pickle
import sys

import numpy as np
import streamlit as st


# Keep compatibility with pickle files created with a different NumPy layout.
sys.modules["numpy._core"] = np.core
sys.modules["numpy._core.multiarray"] = np.core.multiarray
sys.modules["numpy._core._multiarray_umath"] = np.core._multiarray_umath

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_resource(show_spinner="Loading recommendation data...")
def load_data():
    with open(os.path.join(BASE_DIR, "popular.pkl"), "rb") as file:
        popular_df = pickle.load(file)

    with open(os.path.join(BASE_DIR, "pt.pkl"), "rb") as file:
        pt = pickle.load(file)

    with open(os.path.join(BASE_DIR, "books.pkl"), "rb") as file:
        books = pickle.load(file)

    with open(os.path.join(BASE_DIR, "similarity_scores.pkl"), "rb") as file:
        similarity_scores = pickle.load(file)

    return popular_df, pt, books, similarity_scores


def get_book_details(books, title):
    matches = books[books["Book-Title"] == title].drop_duplicates("Book-Title")
    if matches.empty:
        return {
            "title": title,
            "author": "Unknown author",
            "image": None,
        }

    row = matches.iloc[0]
    return {
        "title": row["Book-Title"],
        "author": row["Book-Author"],
        "image": row["Image-URL-M"],
    }


def recommend_books(book_title, pt, books, similarity_scores, limit=8):
    matches = np.where(pt.index == book_title)[0]
    if len(matches) == 0:
        return []

    index = matches[0]
    similar_items = sorted(
        enumerate(similarity_scores[index]),
        key=lambda item: item[1],
        reverse=True,
    )[1 : limit + 1]

    recommendations = []
    for item_index, _score in similar_items:
        recommendations.append(get_book_details(books, pt.index[item_index]))

    return recommendations


def render_book_grid(books_to_render, columns=4, show_rating=False):
    for row_start in range(0, len(books_to_render), columns):
        cols = st.columns(columns)
        for col, book in zip(cols, books_to_render[row_start : row_start + columns]):
            with col:
                if book.get("image"):
                    st.image(book["image"], width=140)
                st.markdown(f"**{book['title']}**")
                st.caption(book["author"])
                if show_rating:
                    st.caption(f"Votes: {book['votes']} | Rating: {book['rating']:.1f}")


def main():
    st.set_page_config(page_title="Book Recommender", layout="wide")

    popular_df, pt, books, similarity_scores = load_data()

    st.title("Book Recommender")

    top_books_tab, recommender_tab = st.tabs(["Top 50 Books", "Recommend Books"])

    with top_books_tab:
        st.subheader("Top 50 Books")
        top_books = [
            {
                "title": row["Book-Title"],
                "author": row["Book-Author"],
                "image": row["Image-URL-M"],
                "votes": int(row["num_ratings"]),
                "rating": float(row["avg_rating"]),
            }
            for _, row in popular_df.iterrows()
        ]
        render_book_grid(top_books, columns=4, show_rating=True)

    with recommender_tab:
        st.subheader("Recommend Similar Books")

        selected_book = st.selectbox(
            "Book name",
            options=pt.index.tolist(),
            index=None,
            placeholder="Search for a book title...",
        )

        if st.button("Get Recommendations", type="primary", disabled=selected_book is None):
            recommendations = recommend_books(
                selected_book,
                pt,
                books,
                similarity_scores,
            )

            if not recommendations:
                st.warning("No recommendations found for this book.")
            else:
                st.success(f"Books similar to '{selected_book}'")
                render_book_grid(recommendations, columns=4)


if __name__ == "__main__":
    main()
