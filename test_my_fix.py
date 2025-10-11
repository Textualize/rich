# test_my_fix.py
import pathlib
from rich.pretty import pprint

# Create a Path object to test
my_file_path = pathlib.Path("./my_folder/my_script.py")

# This will use the code you just modified!
print("--- Running test with the fix ---")
pprint(my_file_path)
print("-------------------------------")