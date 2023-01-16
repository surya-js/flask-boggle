from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)

app.config['SECRET_KEY'] = "abc123"
app.debug = True
toolbar = DebugToolbarExtension(app)


@app.route('/')
def display_board():
    
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    no_plays = session.get("no_plays", 0)
    return render_template('display-board.html', 
        board = board, highscore = highscore, no_plays = no_plays)
    
@app.route('/check-word')
def check_word():

    word = request.args['word']
    board = session['board']
    print(request.args)
    response = boggle_game.check_valid_word(board, word.lower())
    print(response)
    return jsonify({'result' : response})

@app.route("/store-score", methods=["POST"])
def post_score():
    """Receive score, update no_plays, update high score if appropriate in the session."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    no_plays = session.get("no_plays", 0)

    session['no_plays'] = no_plays + 1
    # if the current score is higher than the previous highscore than update the highscore to the current score
    session['highscore'] = max(score, highscore) 
    
    # respond with json brokeRecord = true / false
    return jsonify(brokeRecord=score > highscore)
