import os
import random

# TODO
# change headers to match cleaning

candidates = []

facility_and_race_to_line = {}

with open(os.path.join('data', 'cleaned.tsv')) as source:
    with open(os.path.join('data', 'sampled.tsv'), 'w') as sink:
        for line_no, line in enumerate(source):
            if line_no == 0:
                sink.write(line)
                continue
            _, _, race, facility, _ = line.split('\t')

            if not (facility, race) in facility_and_race_to_line:
                facility_and_race_to_line[(facility, race)] = []
            facility_and_race_to_line[(facility, race)].append(line)

        sampled = {}

        for k, v in sorted(facility_and_race_to_line.items(), key=lambda x: (x[0][0], x[0][1])):
            for line in random.sample(v, k=min(len(v),2)):
                sink.write(line)






