THREE_LETTER_PREFIXES_SEEN = set()
TWO_LETTER_PREFIXES_SEEN = set()

THREE_LETTER_PREFIXES = []
TWO_LETTER_PREFIXES = []

import os

for line_no, line in enumerate(open(os.path.join(os.path.dirname(__file__), 'Names_2010Census.csv'))):
    if line_no == 0:
        continue

    name = line.strip().split(',')[0]
    three_letter = name[:3]
    two_letter = name[:2]

    if three_letter not in THREE_LETTER_PREFIXES_SEEN:
        THREE_LETTER_PREFIXES.append(three_letter)
        THREE_LETTER_PREFIXES_SEEN.add(three_letter)

    if two_letter not in TWO_LETTER_PREFIXES_SEEN:
        TWO_LETTER_PREFIXES.append(two_letter)
        TWO_LETTER_PREFIXES_SEEN.add(two_letter)
