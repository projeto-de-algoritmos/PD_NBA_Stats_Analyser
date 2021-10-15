from bisect import bisect_left

def longest_subsequence(array: list):
    criteria, game = array[0]
    subsequence = [
        (criteria, game,)
    ]

    for stat in array:
        criteria, game = stat

        insertion_position = bisect_left(
            subsequence,
            (criteria,)
        )
        if insertion_position == len(subsequence):
            subsequence.append(
                (criteria, game,)
            )
        elif subsequence[insertion_position][0] > criteria:
            subsequence[insertion_position] = (
                (criteria, game,)
            )

    return subsequence
