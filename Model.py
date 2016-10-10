'''Models for Slack TicTacToe Coding Challenge'''

##############################################################################
# Model definitions


class Game(object):
    '''Instantiates a game of TicTacToe using object oriented programming'''

    channel_id = None
    player_one_user_id = None
    player_one_user_name = None
    player_one_emoji_choice = ":heavy_multiplication_x:"
    player_two_user_id = None
    player_two_user_name = None
    player_two_emoji_choice = ":o:"
    response_url = None
    whose_turn = "player_two"
    a1 = ":one:"
    a2 = ":two:"
    a3 = ":three:"
    b1 = ":four:"
    b2 = ":five:"
    b3 = ":six:"
    c1 = ":seven:"
    c2 = ":eight:"
    c3 = ":nine:"

    def __init__(self, channel_id, player_one_user_id, player_one_user_name,
                 player_two_user_id, player_two_user_name, response_url):
        self.channel_id = channel_id
        self.player_one_user_id = player_one_user_id
        self.player_one_user_name = player_one_user_name
        self.player_two_user_id = player_two_user_id
        self.player_two_user_name = player_two_user_name
        self.response_url = response_url

    def show_board(self, player_one_emoji, player_two_emoji, next_players_name):
        '''Any channel member can pull up a board'''
{
    "response_type": "in_channel",
    "text": "It is Player Two's turn now.",
    "attachments": [
        {
            "title": "Player One vs Player Two",
            "fallback": "You are unable to choose a game",
            "callback_id": "wopr_game",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "chess",
                    "text": ":grey_question:",
                    "type": "button",
                    "value": "chess"
                },
                {
                    "name": "maze",
                    "text": ":smile:",
                    "type": "button",
                    "value": "maze"
                },
            {
                    "name": "maze",
                    "text": ":grey_question:",
                    "type": "button",
                    "value": "maze"
                }
                
                
            ]
        
        },
        {
            "fallback": "You are unable to choose a game",
            "callback_id": "wopr_game",
            
            "attachment_type": "default",
            "actions": [
                {
                    "name": "chess",
                    "text": ":rage:",
                    "type": "button",
                    "value": "chess"
                },
                {
                    "name": "maze",
                    "text": ":grey_question:",
                    "type": "button",
                    "value": "maze"
                },
            {
                    "name": "maze",
                    "text": ":grey_question:",
                    "type": "button",
                    "value": "maze"
                }
                
                
            ]
        
        },
                {
            "fallback": "You are unable to choose a game",
            "callback_id": "wopr_game",
            
            "attachment_type": "default",
            "actions": [
                {
                    "name": "chess",
                    "text": ":grey_question:",
                    "type": "button",
                    "value": "chess"
                },
                {
                    "name": "maze",
                    "text": ":grey_question:",
                    "type": "button",
                    "value": "maze"
                },
            {
                    "name": "maze",
                    "text": ":grey_question:",
                    "type": "button",
                    "value": "maze"
                }
                
                
            ]
        
        }
    ]
}

        pass

    def take_turn(self, emoji, position):
        '''The player whose turn it is can make a move'''

        pass

    def check_for_win(self, a1, b1, c1, d1, )


    def set_emoji(self, user_id, emoji):
        '''Set a custom emoji for a user avatar'''

        pass

    def end_game(self, user_id):
        '''Deletes an class object so a new game can be started'''