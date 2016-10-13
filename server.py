"""Slack Slash Command TicTacToe"""

from flask import Flask, request, make_response, abort

import os

import json

import requests

from Model import (connect_to_db, db, Game, Emoji, Player, PlayerInGame)

from helper_functions import (board, check_for_winner, create_a_player, create_game, add_player_to_game)

# ___________________________________________________________________________

app = Flask(__name__)

app.secret_key = os.environ['APP_SECRET_KEY']

slack_token = os.environ['SLACK_TOKEN']

# ___________________________________________________________________________

# @app.route('/test', methods=['GET'])
# def test():
#     """Route to seed the database with valid emojis"""

    #     html = "<html><body>Testing testing, is this thing on?</body></html>"
    #  Pretty silly, but this is how I loaded my seed data into the Heroku
    # database for the emojis because I was getting error messages from the
    # Heroku python CLI

    # for row in (open("valid_emojis.txt")):
    #     row = row.rstrip()
    #     this_emoji = Emoji(emoji=row)
    #     db.session.add(this_emoji)
    #     db.session.commit()

    # return html

# `/ttt :alien:`
# `/ttt 1`


        # check if a player exists for this sender
        # check if a game exists for this channel
        # check if the game is in play


# -Check which channel the game is being played in


@app.route('/game.json', methods=['POST'])
def new_game():
    '''Processes slash commands to play Tic-Tac-Toe'''

    data = request.form
    token = data['token']
    query_text = data['text']
    # team_id = data['team_id']
    channel_id = data['channel_id']
    channel_name = data['channel_name']
    token = data['token']
    # team_domain = data['team_domain']
    username = data['user_name']
    user_id = data['user_id']
    response_url = data['response_url']
    this_game = Game.query.filter_by(channel_id=channel_id).first()
    this_player = Player.query.filter_by(user_name=username).first()
    if token != slack_token:
        return abort(403)
    elif query_text == "help":
        payload = {"text": "*How to play OXO Emoji Tic-Tac-Toe:*\n-Challenge anyone on your team to a game by entering `/ttt` and your opponents username in any channel, e.g. `/ttt @kenny`. There is one game per channel, at a time.\n- By default, your moves will show as :heavy_multiplication_x: and your opponents moves will show as :O:.  To change the emoji that represents your moves, type `/ttt` and the emoji you would like to use, e.g. `/ttt :alien:`. If the emoji you chose has aleady been chosen by another player, your emoji will not be updated.\n- Anyone can type `/ttt board` at any time to show the game board and whose turn it is, but only the person whose turn it is can make a move.\n- To make your move, type `/ttt #` and the number of the square you would like to claim, e.g. `/ttt #1`.\n- To end the game prematurely, type `/ttt catsgame`\n- To see this message again,type `/ttt help`\nThis:\n\n:one:|:two:|:three:\n:four:|:five:|:six:\n:seven:|:eight:|:nine:\n\n Quickly turns into this:\n\n :ghost:|:alien:|:three:\n:four:|:ghost:|:six:\n:alien:|:alien:|:ghost:"}
        json_payload = json.dumps(payload)
        response = make_response(json_payload)
        response.headers['content-type'] = 'application/json'
        return response
    elif query_text == "board":
        if not this_game:
            return "Looks like there is no game in play. Challenge someone to a game by typing /ttt and a username"
        elif this_game.game_active is False:
            return "Looks like there is no game in play. Challenge someone to a game by typing /ttt and a username"
        else:
            payload = board(this_game)
            json_payload = json.dumps(payload)
            response = make_response(json_payload)
            response.headers['content-type'] = 'application/json'
            return response
    elif query_text[0] == "@":
        if this_player:
            this_player.user_id = user_id
            db.session.commit()
            this_game = Game.query.filter_by(channel_id=channel_id).first()
            if this_game:
                if this_game.game_active is True:
                    return "Oops, looks like there is already an active game. Type `/ttt board` to see it or start a game in another channel."
                else:
                    this_game.response_url = response_url
                    this_game.whose_turn = query_text[1:]
                    this_game.game_active = True
                    this_player.emoji = ":heavy_multiplication_x:"
                    db.session.commit()
                    add_player_to_game(game_id=this_game.game_id, player_id=this_player.player_id)
                    opponent = Player.query.filter_by(username=query_text[1:]).first()
                    if not opponent:
                        opponent = create_a_player(username=query_text[1:], emoji=":O:")
                        add_player_to_game(game_id=this_game.game_id, player_id=opponent.player_id)
                        return board(this_game)
                    else:
                        add_player_to_game(game_id=this_game.game_id, player_id=opponent.player_id)
                        opponent.emoji = ":O:"
                        db.session.commit()
                        return this_game.board()
            else:
                this_game = create_game(channel_id=channel_id, channel_name=channel_name,
                                        response_url=response_url, whose_turn=opponent.player_id)
                this_player.emoji = ":heavy_multiplication_x:"
                db.session.commit()
                add_player_to_game(game_id=this_game.game_id, player_id=this_player.player_id)
                opponent = Player.query.filter_by(username=query_text[1:]).first()
                if not opponent:
                        opponent = create_a_player(username=query_text[1:], emoji=":O:")
                        add_player_to_game(game_id=this_game.game_id, player_id=opponent.player_id)
                        return board(this_game)
                else:
                    add_player_to_game(game_id=this_game.game_id, player_id=opponent.player_id)
                    opponent.emoji = ":O:"
                    db.session.commit()
                    return board(this_game)
        else:
            this_player = create_a_player(username=username, emoji=":O:", user_id=user_id)
            this_game = Game.query.filter_by(channel_id=channel_id).first()
            if this_game:
                if this_game.game_active is True:
                    return "Oops, looks like there is already an active game. Type `/ttt board` to see it or start a game in another channel."
                else:
                    this_game.response_url = response_url
                    this_game.whose_turn = query_text[1:]
                    this_game.game_active = True
                    this_player.emoji = ":heavy_multiplication_x:"
                    db.session.commit()
                    add_player_to_game(game_id=this_game.game_id, player_id=this_player.player_id)
                    opponent = Player.query.filter_by(username=query_text[1:]).first()
                    if not opponent:
                        opponent = create_a_player(username=query_text[1:], emoji=":O:")
                        add_player_to_game(game_id=this_game.game_id, player_id=opponent.player_id)
                        return board(this_game)
                    else:
                        add_player_to_game(game_id=this_game.game_id, player_id=opponent.player_id)
                        opponent.emoji = ":O:"
                        db.session.commit()
                        return board(this_game)
            else:
                this_game = create_game(channel_id=channel_id, channel_name=channel_name,
                                        response_url=response_url, whose_turn=opponent.player_id)
                this_player.emoji = ":heavy_multiplication_x:"
                db.session.commit()
                add_player_to_game(game_id=this_game.game_id, player_id=this_player.player_id)
                opponent = Player.query.filter_by(username=query_text[1:]).first()
                if not opponent:
                    opponent = create_a_player(username=query_text[1:], emoji=":O:")
                    add_player_to_game(game_id=this_game.game_id, player_id=opponent.player_id)
                    return board(this_game)
                else:
                    add_player_to_game(game_id=this_game.game_id, player_id=opponent.player_id)
                    opponent.emoji = ":O:"
                    db.session.commit()
                    return board(this_game)
    elif query_text[0] == ":":
        if this_game.game_active is True:
            in_this_game = db.session.query(PlayerInGame).filter(PlayerInGame.game_id == this_game.game_id, PlayerInGame.player_id == this_player.player_id).first()
            if in_this_game:
                this_player.emoji = query_text
                db.session.commit()
            else:
                return "Oops, looks like you aren't in this game. Type `/ttt board` to see the current game or start a game in another channel."
        else:
            "Oops, looks like there is no game being played currently. Challenge someone to a game by typing `/ttt` and the username of someone in this channel"
    elif query_text[0] == "#":
        pass
    else:
        return 'I don\'t know that one. Enter `ttt help` to see valid `/ttt` commands'


# ___________________________________________________________________________


if __name__ == "__main__":

    connect_to_db(app, os.environ.get("DATABASE_URL"))

    app.debug = True

    DEBUG = "NO_DEBUG" not in os.environ

    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
