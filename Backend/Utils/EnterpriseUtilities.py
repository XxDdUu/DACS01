import random
import string

def generate_random_enterprise_id():
	prefix = "ENT_"
	random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
	return prefix + random_part