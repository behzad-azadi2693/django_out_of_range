from django.db import connection, reset_queries
import time

def debugger(func):
    def wrapper(*args, **kwargs):
        reset_queries()
        st=time.time()
        value = func(*args, **kwargs)
        et=time.time()

        queries = len(connection.queries)
        print(f"'--------------------------------------',{queries} ,' ----time:',{et-st}")
        return value
    return wrapper
