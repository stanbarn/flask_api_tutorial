from flask import Flask, jsonify, request
app = Flask(__name__)
authors = [
    {'author_id': 1,'first_name':'barna','last_name':'stanley'},
    {'author_id': 2,'first_name':'barna','last_name':'stanley'},
    {'author_id': 3,'first_name':'barna','last_name':'stanley'}
]
books = [
    {'book_id':1,'title':'Introduction to Flask APis','authors':authors,'description':'this is a test book'}
]
@app.route('/')
def landing():
    return 'Welcome to our book store'

@app.route('/api/v1/books/<int:bookId>', methods = ['GET'])
def get_book(bookId):

    if not bookId or bookId < 1:
        return jsonify({
            'message': 'sorry! book ID is required and can not be less than 1'
        }), 400
    for book in books:
        if book['book_id'] == bookId:
            return jsonify({
                'book':book
            }), 200
    return jsonify({
        'message':'the book was not found'
    }), 204
@app.route('/api/v1/books', methods = ['POST'])    
def add_book():
    data = request.get_json()

    title = data.get('title')
    book_authors = data.get('authors')
    description = data.get('description') 
    book_id = len(books)+1

    if not title or title.isspace():
        return jsonify({
            'message':'sorry! the title is required and can not be an empty string'
        }), 400

    if not description or description.isspace():
        return jsonify({
            'message':'sorry! the description is required and can not be an empty string'
        }), 400

    if type(book_authors) == int:
        return jsonify({
            'message':'sorry!  the book authors should be a list'
        }), 400

    if not book_authors or len(book_authors) == 0:
        return jsonify({
            'message':'sorry!  the book should have at least an author'
        }), 400
    
    for author in book_authors:
        for single_author in authors:
            if author['author_id'] != single_author['author_id']:
                authors.append(author)
    
    book = dict(
        title = title,
        book_id = book_id,
        description = description,
        author = book_authors
    )

    books.append(book)

    return jsonify({
        'message': 'The book was created successully',
        'book': book
    }), 201

@app.route('/api/v1/authors')
def get_authors():
    return jsonify({
        'authors': authors
    })

@app.route('/api/v1/books/<int:bookId>', methods = ['PUT'])
def update_book(bookId):

    if not bookId or bookId < 1:
        return jsonify({
            'message': 'sorry! book ID is required and can not be less than 1'
        }), 400

    data = request.get_json()

    title = data.get('title')
    book_authors = data.get('authors')
    description = data.get('description') 

    if not title or title.isspace():
        return jsonify({
            'message':'sorry! the title is required and can not be an empty string'
        }), 400

    if not description or description.isspace():
        return jsonify({
            'message':'sorry! the description is required and can not be an empty string'
        }), 400

    if type(book_authors) == int:
        return jsonify({
            'message':'sorry!  the book authors should be a list'
        }), 400

    if not book_authors or len(book_authors) == 0:
        return jsonify({
            'message':'sorry!  the book should have at least an author'
        }), 400

    for author in book_authors:
        for single_author in authors:
            if author['author_id'] != single_author['author_id']:
                authors.append(author)

    book = dict(
        title = title,
        description = description,
        author = book_authors
    )

    for existing_book in books:
        if existing_book['book_id'] == book['book_id']:
            existing_book.update(book)

            return jsonify({
                'message':'book updated successfully.',
                'book': book
            })
            
        else:
            return jsonify({
                'message':'update failed! the book does not exist.'
            }), 200
    

    