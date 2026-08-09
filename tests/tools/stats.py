import time, platform, psutil, GPUtil

def benchmark_timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time

        post_print()
        print(f"Total execution time: {total_time:.4f} seconds")
        return result 
        
    return wrapper


def benchmark_stats(func):
    def wrapper(*args, **kwargs):
        post_print()
        memory = psutil.virtual_memory()
        gpus = GPUtil.getGPUs()
        if not gpus:
            gpu = BlankGPU()
        else:
            gpu = gpus[0]

        stats = f"OS: {platform.platform()}\nCPU: {platform.processor()}\nGPU: {gpu.name}\nVRAM: {gpu.memoryTotal} GiB\nRAM: {round(memory.total / (1024**3), 2)} GiB"
        print(stats)
        post_print()

        return func(*args, **kwargs)

    return wrapper

def post_print() -> None:
    print("")
    print("----------------------------------------------------------------------")
    print("")

class BlankGPU:
    def __init__(self):
        self.name = "No GPU Detected"
        self.memoryTotal = 0
