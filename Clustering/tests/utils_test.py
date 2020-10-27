import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *
from tests.test import *


print(test_function_with_one_var(is_iter, test_vars)[1])
print(test_function_with_one_var(recursive_min, test_vars)[1])
print(test_function_with_one_var(recursive_max, test_vars)[1])
print(test_function_with_one_var(recursive_list, test_vars)[1])
print(test_function_with_one_var(recursive_nparray, test_vars)[1])
print(test_function_with_one_var(recursive_mean, [[vars for _ in range(5)] for vars in test_vars[1:]])[1])



