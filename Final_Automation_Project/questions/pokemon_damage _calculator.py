import logging

# define some constants to represent the effectiveness of attack types in the game. A score of 2 means the attack is
# super effective, 1 means it is neutral, and 0.5 means it is not very effective.
EFFECTIVE_SCORE = 2
NON_EFFECTIVE_SCORE = 0.5
NEUTRAL_SCORE = 1

# This dictionary contains the different types of attacks in the game. Each attack type is a key,
# and its value maps all the types of Pokemon to their corresponding effectiveness scores.
MATCHUP_DICT = {
    "fire": {
        "grass": EFFECTIVE_SCORE,
        "water": NON_EFFECTIVE_SCORE,
        "electric": NEUTRAL_SCORE,
        "fire": NON_EFFECTIVE_SCORE,
    },
    "grass": {
        "fire": NON_EFFECTIVE_SCORE,
        "water": EFFECTIVE_SCORE,
        "electric": NEUTRAL_SCORE,
        "grass": NON_EFFECTIVE_SCORE,
    },
    "water": {
        "fire": EFFECTIVE_SCORE,
        "grass": NON_EFFECTIVE_SCORE,
        "electric": NON_EFFECTIVE_SCORE,
        "water": NON_EFFECTIVE_SCORE,
    },
    "electric": {
        "fire": NEUTRAL_SCORE,
        "water": EFFECTIVE_SCORE,
        "grass": NEUTRAL_SCORE,
        "electric": NON_EFFECTIVE_SCORE,
    },
}


# This is the class definition for a Player. It contains the player's first and last names, their Pokemon's name,
# and their current life (set to 1000 at the beginning of the game).
class Player:
    def __init__(self, first_name, last_name, pokemon_name):
        self.first_name = first_name
        self.last_name = last_name
        self.pokemon_name = pokemon_name
        self.life = 1000


# This is the class definition for a Pokemon battle.
# It takes two Player objects as arguments and sets them as the first and second players for the game.
class PokemonBattle:
    def __init__(self, first_player, second_player):
        self.first_player = first_player
        self.second_player = second_player

# This is a private method that prints out the name of the winner at the end of the game. It checks the life of both
    # players and determines the winner based on whose life is greater.
    def _print_winner(self):
        winner = self.first_player if self.second_player.life <= 0 else self.second_player
        print(f"{winner.first_name} {winner.last_name} ({winner.pokemon_name}) wins!")

# This is a static method that calculates the damage inflicted by an attack. It takes the attacker's type,
    # the defender's type, the power of the attack, and the defense power of the defender. It looks up the
    # effectiveness score from the MATCHUP_DICT and calculates the damage based on the formula given.
    @staticmethod
    def calculate_damage(attacker_type, defender_type, attack_power, defense_power):
        effectiveness = MATCHUP_DICT[attacker_type][defender_type]
        damage = 50 * (attack_power / defense_power) * effectiveness
        return damage

# This is a static method that is used to get the details of a player's turn. The player
    # argument is the player who is taking the turn, and the action argument is the action (attack or defense) that
    # the player is taking.
    @staticmethod
    def _turn(player, action):
        print(f"{player.first_name}'s turn")
        print(f"Current life: {player.life}")
        action_types = set(MATCHUP_DICT.keys())
        action_type = input(f"Enter the type of your {action} {action_types}: ")
        while action_type not in MATCHUP_DICT.keys():
            logging.error(f"Wrong action type: {action_type}")
            action_type = input(f"Enter the type of your {action} {action_types}: ")
        action_power = input(f"Enter the power of your {action} (1-100): ")
        while not action_power.isnumeric() or int(action_power) not in range(1, 101):
            logging.error(f"Wrong power amount: {action_power}")
            action_power = input(f"Enter the power of your {action} (1-100): ")
        return action_type, int(action_power)

# These lines define the play method of the PokemonBattle class.
    # The attack_player and defense_player variables are initialized to the first and second players, respectively.
    def play(self):
        attack_player = self.first_player
        defense_player = self.second_player

# This while loop runs as long as both players have life points remaining.
        while self.first_player.life > 0 and self.second_player.life > 0:
            # Attack player turn
            attack_type, attack_power = self._turn(attack_player, "attack")

            # Defense player turn
            defense_type, defense_power = self._turn(defense_player, "defense")

            # calculate the damage done by the attack, based on the attack and defense types and powers,
            # and prints the damage done to the console.
            damage = self.calculate_damage(attack_type, defense_type, attack_power, defense_power)
            print(f"{attack_player.first_name} did {damage} damage to {defense_player.first_name}")

            # Update players' life
            attack_player.life -= attack_power
            defense_player.life -= defense_power + damage

            # Switch players
            attack_player, defense_player = defense_player, attack_player

        # Print winner
        self._print_winner()


# Example usage
player_1 = Player("Avi", "Via", "Charmander")
player_2 = Player("Moshe", "Via", "Squirtle")

game = PokemonBattle(player_1, player_2)
game.play()
