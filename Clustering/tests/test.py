import random

integer = 3
table_of_ints = [i for i in range(10)]
table_of_tables = [table_of_ints for _ in range(5)]
random_table = [[random.randint(1,5) for _ in range(random.randint(1,3))] for _ in range(random.randint(1, 3))]

test_vars = [integer, table_of_ints, table_of_tables, random_table]

def test_function_with_one_var(function, variables):
    for vars in variables:
        try:
            function(vars)
        except Exception as e:
            print(e)
            return False, 'Failed'
    return True, 'Passed'