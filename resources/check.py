def check_string( str = None, label = "", max_length = 64 ):
	# can't have a null value!
	if str == None:
		raise ValueError( f'Variable {label} cannot be null!' )
	
	# strip the string of leading & trailing whitespace
	str = str.strip()
	
	if str == "":
		raise ValueError( f'Variable {label} is empty!' )
	elif len( str ) > max_length:
		raise ValueError( f'Variable {label} is too long! {len(str)} > {max_length}' )

	return str
	
def check_int( num = None, label = "", min = float('-inf'), max = float('inf') ):
	try:
		num = int( num )
	except:
		raise ValueError( f'Variable {label} malformed! ({num})' )

		
	if num < min or num > max:
		raise ValueError( f'Variable {label} is out of range! ({num} <> [{min},{max}])' )
		
	return num
	
def check_float( num = None, label = "", min = float('-inf'), max = float('inf') ):
	try:
		num = float( num )
	except:
		raise ValueError( f'Variable {label} malformed! ({num})' )
	
	if num < min or num > max:
		raise ValueError( f'Variable {label} is out of range! ({num} <> [{min},{max}])' )
		
	return num
	

print( check_float( '1', "foo", 0 ) )