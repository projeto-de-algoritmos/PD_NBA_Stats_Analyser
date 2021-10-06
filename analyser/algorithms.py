from bisect import bisect_left

def longest_subsequence(array: list):
    subsequence = [array[0]]

    for number in array:
        insertion_position = bisect_left(subsequence, number)
        if insertion_position == len(subsequence):
            subsequence.append(number)
        elif subsequence[insertion_position] > number:
            subsequence[insertion_position] = number

    return subsequence
