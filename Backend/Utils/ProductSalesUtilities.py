from datetime import datetime

def generate_PS_id():
    postfix = 'PS'
    now = datetime.now()
    time_string = now.strftime("%Y%m%d%H%M%S")
    return time_string + postfix

