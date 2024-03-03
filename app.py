from flask import Flask, render_template, request, redirect, url_for
from flask import redirect, url_for
import pickle

import numpy as np

app = Flask(__name__)
encoding = 'utf-16'
popular_df = pickle.load(open('popular.pkl', 'rb'), encoding=encoding)
pt = pickle.load(open('pt.pkl', 'rb'), encoding=encoding)
books = pickle.load(open('books.pkl', 'rb'), encoding=encoding)
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'), encoding=encoding)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend', methods=['POST'])
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

@app.route('/contact')
def contact_ui():
    return render_template('contact.html')


@app.route('/contact', methods=['POST'])
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

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


if __name__ == '__main__':
    app.run(debug=True)
