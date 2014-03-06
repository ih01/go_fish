import random

# yield modifiers:
# 2 = low yield
# 4 = medium yield
# 7 = high yield

class yieldGenerator(object):

	# base fish count on a field
	STDFISH = 5

	# constructor
	def __init__(self):

		# create empty dictionary
		self.map = dict()
		
		# assign default yield value to all grid fields
		for x in range( 0, 5 ):
			for y in range( 0, 5 ):
				# assign 2 where 2 means low yield modifier
				self.map.setdefault( ( x, y ), 2 ) 
		
		# give me a random number between 3 and 5
		randomNum = random.randint( 3, 5 )
		
		# assign high yield value to random fields
		for num in range ( randomNum ):
			# find random x
			x = random.randint( 0, 4 )
			# find random y
			y = random.randint( 0, 4 )
			
			# assign high yield modifier to respective dictionary entry
			self.map[ (x, y) ] = 7
			
			# assign medium yield to adjacent fields (left, right, above, under)
			if not( ( x + 1 ) > 4 ): 
				self.map[ (x+1), y] == 4
			if not( ( x - 1 ) < 0 ): 
				self.map[ (x-1), y] == 4
			if not( ( y + 1 ) > 4 ): 
				self.map[ x, (y+1) ] == 4
			if not( ( y - 1 ) < 0 ): 
				self.map[ x, (y-1) ] == 4
	
	# method which calculates yield, updates the yield field modifier
	# and returns the yield value
	def deplete( self, x, y, rodMod, baitMod ):
		# calculate the yield
		gain = self.map[ ( x, y ) ] * STDFISH * ( rodMod + baitMod )
		
		# deplete the field on which fishing has happened
		if self.map[ ( x , y ) ] == 0:
			return 0
		else:
			oldValue = self.map[ ( x, y ) ]
			self.map[ ( x, y ) ] = oldValue - 1
		
		# return the yield value
		return gain
		
		
	def print_map(self):
		print self.map

testYG = yieldGenerator()

print testYG.print_map()