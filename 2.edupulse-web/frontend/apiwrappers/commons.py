from functools import wraps
import functools
from wsgiref import headers
#import time

'''
from o11y import LogCollector

log_collector = LogCollector(flush_interval=60, max_queue_size=1000)

def timer_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        #print(f"'{func.__name__}' execution time: {execution_time:.2f} ms")
        log = {
            "timestamp": start_time,
            "function_name": func.__name__,
            "execution_time": execution_time
        }
        log_collector.add_log(log)

        return result
    return wrapper

def safe_int(value):
    try:
        return int(value)
    except ValueError:
        return 0
'''
import jwt

# Generate JWT token
def generate_jwt_token(user):
    payload = {
        '_id': user['_id'],
        'userEmail': user['userEmail'],
        'tenantName': user['tenantName'],
        'userType': user['userType'],
        'userName': user['userName'],
        'userGrade': user['userGrade'],
        'userLevel': user['userLevel'],
        'userGroup': user['userGroup'],
        'profilePic': user['profilePic']

    }
    secret_key = 'your_secret_key_here_IntentionallyDidntChangeIt'
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

# Verify JWT token
def verify_jwt_token(token):
    secret_key = 'your_secret_key_here_IntentionallyDidntChangeIt'
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def jwt_requiredV1(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'jwt' in kwargs:
            headers['Authorization'] = f"Bearer {kwargs.pop('jwt')}"
        else:
            raise ValueError("JWT token is required")
        return func(*args, **kwargs)
    return wrapper

def jwt_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        local_headers = {'Content-Type': 'application/json'}  # Create a local headers dictionary
        if 'jwt' in kwargs:
            local_headers['Authorization'] = f"Bearer {kwargs.pop('jwt')}"
        else:
            raise ValueError("JWT token is required")
        # Pass the local headers dictionary to the function
        return func(hdrs=local_headers, *args, **kwargs)
    return wrapper
