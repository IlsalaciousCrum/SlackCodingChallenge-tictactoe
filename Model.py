"""Models for Slack TicTacToe Coding Challenge"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Model definitions


class Game(db.Model):
    """A game of TicTacToe. One per channel"""

    __tablename__ = "games"

    game_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    channel_id = db.Column(db.String(64), nullable=False)
    channel_name = db.Column(db.String(64), nullable=False)
    response_url = db.Column(db.String(120), nullable=False)
    whose_turn = db.Column(db.Integer, db.ForeignKey('players.player_id'))
    game_active = db.Column(db.Boolean, default=True, nullable=False)
    a1 = db.Column(db.String(64), nullable=False, default=":one:")
    a2 = db.Column(db.String(64), nullable=False, default=":two:")
    a3 = db.Column(db.String(64), nullable=False, default=":three:")
    b1 = db.Column(db.String(64), nullable=False, default=":four:")
    b2 = db.Column(db.String(64), nullable=False, default=":five:")
    b3 = db.Column(db.String(64), nullable=False, default=":six:")
    c1 = db.Column(db.String(64), nullable=False, default=":seven:")
    c2 = db.Column(db.String(64), nullable=False, default=":eight:")
    c3 = db.Column(db.String(64), nullable=False, default=":nine:")

    players = db.relationship('Player',
                              secondary='players_in_game',
                              backref='games')

    def board(self):
        """A helper method to show the current board, formatted as a string for json"""

        board = "{0}{1}{2}\n{3}{4}{5}\n{6}{7}{8}".format(self.a1, self.a2, self.a3, self.b1, self.b2, self.b3, self.c1, self.c2, self.c3)

        return board

    def check_for_winner(self):
        """A helper method to check for a winner"""

        row_1 = [self.a1, self.a2, self.a3]
        row_2 = [self.b1, self.b2, self.b3]
        row_3 = [self.c1, self.c2, self.c3]

        if row_1[0] == row_1[1] and row_1[1] == row_1[2]:  # horizontal
            return True
        elif row_2[0] == row_2[1] and row_2[1] == row_2[2]:  # horizontal
            return True
        elif row_3[0] == row_3[1] and row_3[1] == row_3[2]:  # horizontal
            return True
        elif row_1[0] == row_2[0] and row_2[0] == row_3[0]:  # vertical
            return True
        elif row_1[1] == row_2[1] and row_2[1] == row_3[1]:  # vertical
            return True
        elif row_1[2] == row_2[2] and row_2[2] == row_3[2]:  # vertical
            return True
        elif row_1[0] == row_2[1] and row_2[1] == row_3[2]:  # diagonal
            return True
        elif row_1[2] == row_2[1] and row_2[1] == row_3[0]:  # diagonal
            return True
        else:
            return False

    def make_move(self, channel_id, user_id, square):
        """Records a move for any user"""

        player = db.session.query(Player).filter(Player.user_id == user_id).first()
        self.square = player.emoji
        next_player = db.session.query(Player).filter(Player.user_id != user_id).first()
        self.whose_next = next_player.player_id


class PlayerInGame(db.Model):
    """An association table to enable easy querying"""

    __tablename__ = "players_in_game"

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)


class Player(db.Model):
    """Player of TicTacToe. Must be a team member"""

    __tablename__ = "players"

    player_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    user_name = db.Column(db.String(64), nullable=False, unique=False)
    player_emoji = db.Column(db.Integer, db.ForeignKey('emojis.emoji_id'), nullable=False)

    emojis = db.relationship('Emoji')


class Emoji(db.Model):
    "The valid emojis that work on Slack and don't interfere with game design."

    __tablename__ = "emojis"

    emoji_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    emoji = db.Column(db.String(64), nullable=False, unique=True)

    players = db.relationship('Player')


##############################################################################
# Database Helper functions

def load_emoji():
    """Loads the emojis from a seed file"""

    for row in (open("seed_data/valid_emojis")):
        row = row.rstrip()
        this_emoji = Emoji(emoji=row)
        db.session.add(this_emoji)
        db.session.commit()


def connect_to_db(app, db_uri=None):
    '''Connect the database to Flask app.'''

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgres:///oxo'
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':

    from server import app
    connect_to_db(app)
    print 'Connected to DB.'
