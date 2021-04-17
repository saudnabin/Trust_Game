
#---------------------------------------------------------------------------------
# creating an class that represents a move indicating a choice to cheat or not
#---------------------------------------------------------------------------------

class Move:
	def __init__(self, cooperate = True):
		self.cooperate= cooperate

	def __str__(self):
		# checking if cooperate is True
		if self.cooperate:
			return "."
		else:
			return "x"

	def __repr__(self):
		return "Move("+ str(self.cooperate)+")"

	def __eq__(self,other):
		# checking if self cooperate is same as the other cooperate
		if self.cooperate == other:
			return True
		else:
			return False 

	def change (self):
		# changing the cooperate status 
		self.cooperate = not self.cooperate
	
	def copy (self):
		# creating an object "turn"
		return Move(self.cooperate)

#---------------------------------------------------------------------------------
# creatign a class that represents any exceptional situation for players
#---------------------------------------------------------------------------------

class PlayerException(Exception):
	def __init__(self, msg):
		self.msg= msg

	def __str__(self):
		return self.msg

	def __repr__(self):
		return "PlayerException('"+self.msg+"')"

#---------------------------------------------------------------------------------
# creating a class that represents a player whose style will resolve the behavior
#---------------------------------------------------------------------------------

class Player:
	def __init__(self, style, points=0, history= None):
		# top(types of player) is the list with all five accepted styles
		top = ['previous','friend','cheater','grudger','detective']
		self.style=style
		# checking if the style is any of the types of players
		if style not in top:
			# raising an exception to display a message
			raise PlayerException("no style '{}'.".format(self.style))
			
		self.points = points
		# checking if history is None
		if history == None:
			# assigning hisotyr an emptylist
			self.history= []
		else:
			self.history = history

	def __str__(self):
		# assigning answer an empty string
		answer = ""
		# running loop for every single index in history
		for index in self.history:
			answer += str(index)
		return "{}({}){}".format(self.style,self.points, answer)

	def __repr__(self):
		return "Player('{}', {}, {})".format(self.style,self.points, str(self.history))

	def reset_history(self):
		# reseting history leaving it an empty list
		self.history = []

	def reset(self):
		# reseting history leaving it an empty list
		self.history = []
		# assinging 0 to points
		self.points = 0

	def update_points(self,amount):
		self.points += amount

	def ever_betrayed(self):
		# running loop for every single index in history
		for index in self.history:
			if 'x' == index.__str__():
				return True
		return False

	def record_opponent_move(self, move):
		self.move = move
		# adding move to the history
		self.history.append(self.move)

	def copy_with_style(self):
		player= Player(self.style, history = None)
		return player

	def choose_move(self):
		stats = self.history
		answer = ''
		# checkinf if the type of player is previous
		if self.style == 'previous':
			if len(self.history) == 0:
				answer = Move(True)
			else:
				answer = Move(self.history[-1].cooperate)
		# checking if the type of player is friend
		elif self.style == 'friend':
			answer = Move(True)
		# checking if the type of player is cheater
		elif self.style == 'cheater':
			answer = Move(False)
		# checking if the type of the player is grudger
		elif self.style == 'grudger':
			# checking if the opponent ever cheated
			if self.ever_betrayed():
				answer = Move(False)
			else:
				answer = Move(True)
		# checking if the type of player is detective
		elif self.style == 'detective':
			if len(self.history) == 0:
				answer = Move(True)
			elif len(self.history) == 1:
				answer = Move(False)
			elif len(self.history) == 2:
				answer = Move(True)
			elif len(self.history) == 3:
				answer = Move(True)
			# checking if the opponent ever cheated 
			elif self.ever_betrayed():
				answer = Move(stats[-1])
			else:
				answer = Move(False)
		return answer

#---------------------------------------------------------------------------------
# returns a tuple of the payouts players a and b
#---------------------------------------------------------------------------------

def turn_payouts(move_a, move_b):
	# checking of the move_a and b was cooperate or not
	if move_a.__str__() == '.' and move_b.__str__()=='.':
		return (2,2)
	# checking of the move_a cheated and b cooperated 
	elif move_a.__str__() == 'x' and move_b.__str__()=='.':
		return (3,-1)
	# checking of the move_a cooperated and b cheated 
	elif move_a.__str__() == '.' and move_b.__str__()=='x':
		return (-1,3)
	else:
		return (0,0)

#---------------------------------------------------------------------------------
# create and returns a list of Players with their styles and default values
#---------------------------------------------------------------------------------

def build_players(initials):
	# creating an empty list players
    players = []
    # running a loop for every single index in initials
    for index in initials:
        if index == 'p':
            player = Player('previous')
            # (1) adding player to the list players 
            players.append(player)
        elif index == 'f':
            player = Player('friend')
            # look for (1)
            players.append(player)
        elif index == 'c':
            player = Player('cheater')
            # look for (1)
            players.append(player)
        elif index == 'g':
            player = Player('grudger')
            # look for (1)
            players.append(player)
        elif index == 'd':
            player = Player('detective')
            # look for (1)
            players.append(player)
        else:
            raise PlayerException("no style with initial '"+ index + "'.")
    return players

#---------------------------------------------------------------------------------
# create and returns a dictionary of each player type 
#---------------------------------------------------------------------------------

def composition(players):
	# creating a dictionary
	stats = {}
	# running loop for every single index in players
	for index in players:
		# checking if index.style is in the dictionary(stats)
		if index.style in stats:
			stats[index.style] +=1
		else:
			stats[index.style] = 1
	return stats

#---------------------------------------------------------------------------------
#determines the players' paypouts and adjusts their points
#---------------------------------------------------------------------------------

def run_turn(player_a, player_b):
	# checkinf the id of player a and b
    if id(player_a) == id(player_b):
        raise PlayerException("players must be distinct.")
    else:
        player_a.update_points(-1)
        player_b.update_points(-1)
        
        # assigning a_play using choose_move function
        a_play = player_a.choose_move()        
        b_play = player_b.choose_move()
        
        player_a.record_opponent_move(b_play)
        player_b.record_opponent_move(a_play)
        
        answer = turn_payouts(a_play, b_play)
        
        player_a.update_points(answer[0])
        player_b.update_points(answer[1])
        
    return None

#---------------------------------------------------------------------------------
# reset the history of players and have them play 5 turns
#---------------------------------------------------------------------------------

def run_game(player_a, player_b,num_turns= 5):
	# calling reset_history function
	player_a.reset_history()
	player_b.reset_history()
	# running loop for every single index in the range of num_turns
	for index in range(num_turns):
		try:
			# calling run_turn function with parameters player_a and okayer_b
			run_turn(player_a,player_b)
		except PlayerException:
			return None
	return None

#---------------------------------------------------------------------------------

def get_points(players): 
#Gets points of all the players and returns the list of their points 
	answer = []
	for index in range(len(players)):
		answer.append(players[index].points)
	return answer

def lowest(players, replace): 
	#Function that replaces the lowest point players in the list provided  
	ans = get_points(players)
	hold = replace
	while 0 < hold:
		mini = min(ans)
		for index in range(len(players)):
			if players[index].points == mini:
				players.remove(players[index])
				break
		ans.remove(mini)
		hold -= 1
	return None

def highest(players, replace): 
	#Function that copies the highest point players in the list provided  	
	if len(players) == 0:
		return None
	ans = get_points(players)
	hold = replace
	while 0 < hold:
		a = max(ans)
		for index in range(len(players)):
			if players[index].points == a:
				players.append(players[index].copy_with_style())
				break
		ans.remove(a)
		hold -= 1
	return None
	

#Find the lowest and highest scorers
def run_tournament(players, num_turns=10, num_rounds=5, starting_points=0, num_replaces=5): 

	for index in range(1, num_rounds+1):
		if len(players) == 0: 
			#Checks to see if players are all gone, if true then raise exception 
			raise PlayerException("all players died after round " + str(index) + ".")	
			break
		else:	
			#Resets players history and points to starting points 
			for k in range(len(players)):	
				players[k].points = starting_points
				players[k].reset_history()

			for x in range(len(players)): 
			#Runs the games making each player play everyone  
				for y in range(x+1, len(players)):
					run_game(players[x], players[y], num_turns)

		 	#Removes players with negative and lowest scores 
			lowest(players, num_replaces)

			start = 0
			stop = len(players)
			while start < stop: 
				if players[start].points < 0:			
					players.remove(players[start])
					stop -= 1
				else:
					start += 1

			highest(players, num_replaces)	

			if len(players) == 0:
				raise PlayerException("all players died after round " + str(index) + ".")	
				break
	return composition(players)	#The amount of players that im getting when this program is done is right




















