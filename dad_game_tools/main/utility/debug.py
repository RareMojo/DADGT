import time
import datetime
import cv2
from utility.settings import DadgtPaths as paths
from functools import wraps

global DEBUG_MODE
DEBUG_MODE = False

class DadgtDebug():
    """
    Debugging tools for DADGT
    Can be used to time functions and save images
    Call enable_debug_mode() to enable debug mode
    Call disable_debug_mode() to disable debug mode
    """

    @classmethod
    def enable_debug_mode(cls):
        global DEBUG_MODE
        DEBUG_MODE = True
        print("Debug mode enabled.")

    @classmethod
    def disable_debug_mode(cls):
        global DEBUG_MODE
        DEBUG_MODE = False
        print("Debug mode disabled.")

    def save_image(filename: cv2.Mat):
        """
        Save an image to the test_images folder
        Args: filename (cv2.Mat): The image to save
        Saves as a .png to the test_images folder
        """
        print(f"Saving image '{filename}'...")
        cv2.imwrite(paths.test_images_path, filename)

    def debug_args(*args, **kwargs):
        """
        Print out the values of function arguments
        Only runs if DEBUG_MODE is True
        """
        if DEBUG_MODE:
            print("Function arguments:")
            for i, arg in enumerate(args):
                print(f"  arg{i}: {arg}")
            for key, value in kwargs.items():
                print(f"  {key}: {value}")

    def current_time(format="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.now().strftime(format)

    def timer(unit="ms", message=None):
        """
        Decorator to time a function
        Usage: @timer() or @timer("my message")
        Only runs if DEBUG_MODE is True
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if DEBUG_MODE:
                    print(f"Starting '{func.__name__}' at {current_time()}...")
                    start = time.time_ns() // 1_000_000
                result = func(*args, **kwargs)
                if DEBUG_MODE:
                    end = time.time_ns() // 1_000_000
                    time_elapsed = round(end - start, 2)
                    if unit == "ms":
                        time_unit = "milliseconds"
                    elif unit == "s":
                        time_unit = "seconds"
                        time_elapsed /= 1000
                    else:
                        time_unit = "milliseconds"
                    if message:
                        print(f"{message} took {time_elapsed} {time_unit}.")
                    else:
                        print(f"`{func.__name__}` took {time_elapsed} {time_unit}.")
                    print(f"Finished '{func.__name__}' at {current_time()}.")
                return result
            return wrapper

        return decorator

def current_time(format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format)

