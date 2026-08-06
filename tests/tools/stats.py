import time

def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time

        print(f"Total execution time: {total_time:.4f} seconds")
        return result 
        
    return wrapper
