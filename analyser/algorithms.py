from bisect import bisect_left

def longest_subsequence(array: list):
    points, game = array[0]
    subsequence = [
        (points, game,)
    ]

    for stat in array:
        points, game = stat

        insertion_position = bisect_left(
            subsequence,
            (points,)
        )
        if insertion_position == len(subsequence):
            subsequence.append(
                (points, game,)
            )
        elif subsequence[insertion_position][0] > points:
            subsequence[insertion_position] = (
                (points, game,)
            )

    return subsequence
