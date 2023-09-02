import numpy as np


def check_stability(m, r, j):
    """ "Verify the internal stability of a truss"""

    try:
        if (m > 1 and r > 2 and j > 2) and (m + r) >= 2 * j:
            return True
        else:
            return False
    except ValueError:
        ...
    return False


# def swap(index, arr):
#     """Swap the columns and rows of a matrix based on sorting the index."""

#     # Check if the index and the shape of the array are correct
#     if len(index) != arr.shape[0] or arr.shape[0] != arr.shape[1]:
#         print(len(index), arr.ndim)
#         raise ValueError("Index and matrix dimension don't match. Check your inputs")

#     # Check if it's already sorted
#     sorted_index = sorted(index)
#     if index == sorted_index:
#         return index, arr

#     for i in range(len(index)):
#         if index[i] != sorted_index[i]:
#             counter = 0
#             for j in range(len(index)):
#                 if index[j] == sorted_index[i]:
#                     arr[[counter, i]] = arr[[i, counter]]
#                     arr[:, [counter, i]] = arr[:, [i, counter]]
#                     index[i] = sorted_index[i]
#                     break
#                 counter += 1

#     return sorted_index, arr


def globalize(dim, index, arr):
    """Transforms a local stiffness matrix to a global matrix of the entire structure by filling
    the columns and rows that are absent from the index by zeros and return the global matrix.
    """

    c = 0
    for i in range(len(index)):
        while c + 1 < index[i]:
            arr = np.insert(arr, c, 0, 0)
            arr = np.insert(arr, c, 0, 1)
            c += 1
        c += 1
    # Completing the end of the matrix if the last row or column is not the same as in the global matrix
    while c < dim:
        arr = np.insert(arr, c, 0, 0)
        arr = np.insert(arr, c, 0, 1)
        c += 1

    return arr
