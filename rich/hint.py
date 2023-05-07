# Uses levenshtein distance to find similarly spelt words
# Returns string separated by 'or' if multiple matches found 
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    # Create two lists of size len(s2) + 1
    prev_row = list(range(len(s2) + 1))
    curr_row = [0] * (len(s2) + 1)

    for i, c1 in enumerate(s1):
        curr_row[0] = i + 1

        for j, c2 in enumerate(s2):
            # If characters are the same, use the previous diagonal value
            if c1 == c2:
                curr_row[j + 1] = prev_row[j]
            else:
                # If characters are different, use the minimum of the adjacent cells + 1
                curr_row[j + 1] = min(prev_row[j], prev_row[j + 1], curr_row[j]) + 1

        # Copy the current row to the previous row for the next iteration
        prev_row, curr_row = curr_row, prev_row

    return prev_row[-1]


# Uses levenshtein distance to find similarly spelt words
# Returns string separated by 'or' if multiple matches found 
def find_closest_words(user_word, correct_words):
    min_distance = float("inf")
    closest_words = []
    for word in correct_words:
        distance = levenshtein_distance(user_word, word)

        # If a new minimum distance is found, clear the closest words list and update min_distance
        if distance <= min_distance:
            min_distance = distance
            closest_words = [word]
        elif distance == min_distance:
            # If the current word has the same minimum distance, add it to the list
            closest_words.append(word)

    return (closest_words, min_distance)
