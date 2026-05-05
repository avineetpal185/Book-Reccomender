# Book Recommender

This project is a book recommendation demo built from the Book-Crossing style
ratings data. It uses precomputed pickle files for the popular-books list,
the book-user pivot table, and cosine-similarity scores.

## Run With Streamlit

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
streamlit run streamlit_app.py
```

Then open the local URL printed by Streamlit.

## Streamlit Cloud Deployment

Use these settings when deploying from GitHub:

- Repository: this repository
- Branch: the branch containing `streamlit_app.py`
- Main file path: `streamlit_app.py`
- Python version: `3.10`

The Streamlit app reuses the existing `popular.pkl`, `pt.pkl`, `books.pkl`,
and `similarity_scores.pkl` files. The original Flask app is still present, but
Streamlit Cloud should use `streamlit_app.py` as the entry point.

## Verify Before Merge

To verify the pull request before merging it:

1. Open Streamlit Community Cloud.
2. Create a new app from this GitHub repository.
3. Select the pull request branch instead of the default branch.
4. Set the main file path to `streamlit_app.py`.
5. Deploy the app.
6. Open the generated Streamlit URL.
7. Confirm that the `Top 50 Books` tab loads.
8. Open `Recommend Books`, search for `1984`, and confirm that recommendations
   are shown.

You can also test locally with:

```bash
streamlit run streamlit_app.py
```
