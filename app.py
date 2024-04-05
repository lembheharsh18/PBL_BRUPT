
from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
encoding = 'utf-16'
popular_df = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_scores = pd.read_pickle('similarity_scores.pkl')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    try:
        index = np.where(pt.index == user_input)[0][0]
    except IndexError:
        return render_template('recommend.html', data=[], message="Book not found.")

    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data, message="")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve form data from the request
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Do something with the form data (e.g., print it)
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")

        # You can perform further actions here, such as sending an email or storing in a database

        # Redirect to the thank_you.html page
        return redirect(url_for('thank_you'))
    else:
        return render_template('contact.html')


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/Top50Books')
def top50():
    return render_template('Top50Books.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/personality')
def personality():
    return render_template('personality.html')


if __name__ == '__main__':
    app.run(debug=True)
