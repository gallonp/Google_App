import time

# complex_computation() simulates a slow function. time.sleep(n) causes the
# program to pause for n seconds. In real life, this might be a call to a
# database, or a request to another web service.
def complex_computation(a, b):
    time.sleep(.5)
    return a + b

# QUIZ - Improve the cached_computation() function below so that it caches
# results after computing them for the first time so future calls are faster
cache = {}
def cached_computation(a, b):
    key=str(a)+'+'+str(b)
    if cache.has_key(key):
        return cache[key]
    else:
        res=complex_computation(a,b)
        cache[key]=res
        return res


cached_computation(1,3)
