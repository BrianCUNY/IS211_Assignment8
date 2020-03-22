#! /usr/bin/env python3

#IS211 Assignment 8 - Design Patterns / Pig game continuation

import random
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--player1', help="choose either a human or computer")
parser.add_argument('--player2', help="choose either a human or computer")
parser.add_argument('--timed', help="complete game in 60 seconds or less.")
args = parser.parse_args()

class Die(object):
#6 sided die, creates a randint from 1 to 6
	random.seed(0)

	def __init__(self):
	#constructor for Die
		self.rolled = 0
	
	def roll(self):
	#simulates dice roll, returns a randint 1-6
		self.rolled = random.randint(1, 6)
		return self.rolled

class Player(object):
#class for a player of the pig game, stores their name
	
	def __init__(self, name):
	#constructor for Player
		self.name = name
		self.totscore = 0
		self.turnscore = 0
		self.turn_status = 0
		print('Welcome to the game of pig, {}.'.format(self.name))

class Game(object):
#class for the pig game, calls the Die class and stores player names via Player class

	def __init__(self, player1, player2):
	#constructor for Game
		pigplayers = PlayerFactory()
		self.player1 = pigplayers.player_type(args.player1)
		self.player2 = pigplayers.player_type(args.player2)
		self.die = Die()
		self.turn(self.player1)

	def turn(self, player):
	#function for a player's turn in the game
		player.turn_status = 1
		print('It\'s {}\'s turn.'.format(player.name))
		while player.turn_status == 1 and player.totscore < 100:
			if args.timed:
				timer = self.time_keeper()
			roll = self.die.roll()
			if roll == 1:
				print('Sorrt {}! You rolled a 1 and forfeit all'
				' points this turn. Your turn total score is {}. Pass Die'
				' to next player.'.format(player.name, player.totscore))
				player.turnscore = 0
				self.next_player()
			else:
				print('{} rolled a {}.'.format(player.name, roll))
				player.turnscore += roll
				print('Your current point total for this turn is {}.' ' Your total score is {}.'.format(player.turnscore, player.totscore))
				self.turn_choice(player)
		print('{} score is {} and has won the game!'.format(player.name, player.totscore))
	  
	def turn_choice(self, player):
		#game asks player if they want to roll the dice again or hold current points
		if player.type == 'Computer':
			hold_limit = 100 - player.totscore
			if hold_limit > 25:
				hold_limit = 25
			if player.turnscore >= hold_limit:
				player.totscore += player.turnscore
				print('{} points have been added to {}\'s totalscore.').format(player.turnscore. player.name)
				if player.totscore >= 100:
					print('{} wins with a total score of {}.').format(player.name, player.totscore)
					raise SystemExit
				else:
					player.turnscore = 0
					print('{}\'s score is now {}. Please die to next player.').format(player.name, player.totscore)
					self.next_player()
		else:
			self.turn(player)
		choice = input('{}, hold or roll?'.format(player.name))
		choice = (choice[0])
		if choice.lower() == 'h':
			player.totscore += player.turnscore
			print('{} points have been added to {}\'s total score.'.format(player.turnscore, player.name))
			if player.totscore >= 100:
				print('{} wins with a score of {}.'.format(player.name, player.totscore))
				raise SystemExit
			else:
				player.turnscore = 0
				print('{}\'s score is now {}. Please pass die to next player.'.format(player.name, player.totscore))
				self.next_player()
		elif choice.lower() == 'r':
			self.turn(player)
		else:
			print('Type hold (h) or roll (r) only please.')
			self.turn_choice(player)
		
	def next_player(self):
		#changes to the next player
		if self.player1.turn_status ==1:
			self.player1.turn_status = 0
			self.turn(self.player2)
		else:
			self.player2.turn_status = 0
			self.turn(self.player1)
			
class ComputerPlayer(Player):
	#class for a computer player of the pig game
	
	def __init__(self):
		#constructor for ComputerPlayer
		Player.__init__(self, name='Computer')
		self.type = 'Computer'
			
class PlayerFactory(object):
	#class for the created palyer types
	
	def player_type(self, player_type, name='Brian Kiernan'):
		#creates the player type from entered choice
		if player_type[0].lower() =='h':
			return Player(name)
		elif player_type[0].lower() =='c':
			return ComputerPlayer()
			
class TimedGameProxy(Game):
	#class for a timed pig game
	
	def __init__(self):
		#constructorfor TimedGameProxy
		self.start_time = time.time()
		Game.__init__(self, 'Player 1', 'Player 2')
	
	def time_keeper(self):
		#tracks/keeps time of game, if time reaches 1 minute then game ends, player with highests totscore wins
		if time.time() - self.start_time >= 60:
			if self.player1.totscore > self.player2.totscore:
				print('Time is up! {} ' 'wins with a total score of {}.').format(self.player1.name, self.player1.totscore)
			else:
				print('Time is up! {} ' 'wins with a total score of {}.').format(self.player2.name, self.player2.totscore)
				raise SystemExit
		else:
			time_left = time.time() - self.start_time
			print('{} seconds have passed, keep going.').format(time_left)

def main():
	if args.timed:
		pig = TimedGameProxy()
	else:
		pig = Game()
		
if __name__ == '__main__':
	main()
