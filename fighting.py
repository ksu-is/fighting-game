import sys
import random
import time
from colorama import init
init()

class colors():
    Red = "\u001b[31m"
    Green = "\u001b[32m"
    White = "\u001b[37m"
    Blue = "\u001b[34m"
    Yellow = "\u001b[33m"    

class Player():
    def __init__(self, name):
        self.health = 100
        self.name = name
        self.wins = 0
        self.paralyze = False

    def calculate_damage(self, damage_amount, attacker):
        if (damage_amount > self.health):
            overkill = abs(self.health - damage_amount)
            self.health = 0
            if (overkill > 0):
                print("{0} takes fatal damage from {1}, with {2} overkill!"
                      .format(self.name.capitalize(), attacker, overkill))
            else:
                print("{0} takes fatal damage from {1}!"
                      .format(self.name.capitalize(), attacker))
        else:
            self.health -= damage_amount
            print("{0} takes {1} damage from {2}!"
                  .format(self.name.capitalize(), colors.Red + str(damage_amount) + colors.White, attacker))

    def calculate_heal(self, heal_amount):
        if (heal_amount + self.health > 100):
            self.health = 100
            print("{0} heals back to full health!"
                  .format(self.name.capitalize()))
        else:
            self.health += heal_amount
            print("{0} heals for {1}!"
                  .format(self.name.capitalize(), heal_amount))


def parse_int(input):
    try:
        int(input)
        return True
    except ValueError:
        return False


def get_selection():
    valid_input = False
    while (valid_input is False):
        print()
        choice = input("Select an attack: ")
        if (parse_int(choice) is True):
            return int(choice)
        else:
            print("The input was invalid. Please try again.")


def get_computer_selection(health):
    sleep_time = random.randrange(2, 5)
    print("....thinking....")
    time.sleep(sleep_time)

    if (health <= 35):
        # Have the computer heal ~50% of its turns when <= 35
        result = random.randint(1, 6)
        if (result % 2 == 0):
            return 4
        else:
            return random.randint(1, 3)
    elif (health == 100):
        return random.randint(1, 3)
    else:
        return random.randint(1, 4)


def play_round(computer, human):
    game_in_progress = True
    current_player = computer

    while game_in_progress:
        # swap the current player each round
        if (current_player == computer):
            current_player = human
        else:
            current_player = computer
        if (current_player.paralyze == False):
            print()
            print(
                "You have " + colors.Green + str(human.health) + colors.White + " health remaining and the "
                "Computer has " + colors.Green + str(computer.health) + colors.White + " health remaining."
                )
            print()

            if (current_player == human):
                print("Available attacks:")
                print("1) Piercing Strike - Causes moderate damage.")
                print("2) Ferocious Swing - High or low damage, "
                    "depending on your luck!")
                print("3) Paralyzing Touch - Stuns opponent while applying a small amount of damage. Be careful, you can miss!")
                print("4) Mead Chug - Restores a moderate amount of health.")
                move = get_selection()
            else:
                move = get_computer_selection(computer.health)
                print("Computer selected attack: " + str(move))

            if (move == 1):
                damage = random.randrange(18, 25)
                if (current_player == human):
                    computer.calculate_damage(damage, human.name.capitalize())
                else:
                    human.calculate_damage(damage, computer.name.capitalize())
            elif (move == 2):
                damage = random.randrange(10, 35)
                if (current_player == human):
                    computer.calculate_damage(damage, human.name.capitalize())
                else:
                    human.calculate_damage(damage, computer.name.capitalize())
            elif (move == 3):
                chance = random.randrange(1,100)
                if (chance > 75):
                    damage = random.randrange(5, 15)
                    if (current_player == human):
                        computer.paralyze = True
                        computer.calculate_damage(damage, human.name.capitalize())
                    else:
                        human.paralyze = True
                        human.calculate_damage(damage, computer.name.capitalize())
                else:
                     print ("Attack " + colors.Yellow + "failed. " + colors.White +  "Turn lost.")
            elif (move == 4):
                heal = random.randrange(18, 25)
                current_player.calculate_heal(heal)
            else:
                print ("The input was not valid. Please select a choice again.")
                if (current_player == computer):
                    current_player = human
                else:
                    current_player = computer
            if (human.health == 0):
                print("Sorry, you lose!")
                computer.wins += 1
                game_in_progress = False

            if (computer.health == 0):
                print("Congratulations, you beat the computer!")
                human.wins += 1
                game_in_progress = False
        else:
            current_player.paralyze = False
            print(current_player.name + " is " + colors.Blue + "paralyzed" + colors.White + " and cannot attack!")


def start_game():
    print("Welcome to Chivalry is Lost: a turn-based fighting game!")

    computer = Player("Computer")

    name = input("Please enter your name: ")
    human = Player(name)

    keep_playing = True

    while (keep_playing is True):
        print("Current Score:")
        print("You - {0}".format(human.wins))
        print("Computer - {0}".format(computer.wins))

        computer.health = 100
        human.health = 100
        play_round(computer, human)
        print()
        response = input("Play another round?(Y/N)")
        if (response.lower() == "n"):
            break

start_game()
