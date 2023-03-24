import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ml.helper.debug import is_debug_on, set_debug, change_name
print(is_debug_on())
set_debug()
print(is_debug_on())
name = "test"
print(change_name(name))