"""Runtime comparison of 'C' function of matrix multiply and
'Python' function of matrix multiply, 'cutilis' is a specially
written 'C' libriary with that function"""
import time
from random import randint
import cutils


def py_mul_matrix(arr1: list, arr2: list):
    """Python matrix multiply function"""
    res = []
    val = 0
    row1 = len(arr1)
    col1 = len(arr1[0])
    row2 = len(arr2)
    col2 = len(arr2[0])
    if col1 != row2:
        return None
    for i in range(row1):
        res.append([])
        for j in range(col2):
            for k in range(row2):
                val += arr1[i][k] * arr2[k][j]
            res[i].append(val)
            val = 0
    return res


def main():
    """Generate random big matrices, multiply them first on C,
    than on python, calculates execution of each one"""
    row1 = 10
    col1 = 11
    row2 = col1
    col2 = 12

    arr1 = [[randint(10000, 99999) for i in range(col1)] for j in range(row1)]
    arr2 = [[randint(10000, 99999) for i in range(col2)] for j in range(row2)]
    start_c_ts = time.time()
    try:
        res_c = cutils.mult_matrix(arr1, arr2)
        end_c_ts = time.time()
    except SystemError:
        res_c = None
        print("Error in running cutils")
    else:
        print(f"Time of execution of C matrix mult: {end_c_ts - start_c_ts}")
    start_ts = time.time()
    res_py = py_mul_matrix(arr1, arr2)
    end_ts = time.time()
    if res_py is None:
        print("Error in running python function")
    else:
        print(f"Time of execution of Py matrix mult: {end_ts - start_ts}")
    if res_c == res_py and res_py and res_c:
        print("Successfully")
    else:
        print("Failed")


if __name__ == "__main__":
    main()
