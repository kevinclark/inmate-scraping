import os
import random

candidates = []

facility_to_line = {}

with open(os.path.join('data', 'all_cleaned.tsv')) as source:
    with open(os.path.join('data', 'sampled_facilities.tsv'), 'w') as sink:
        for line_no, line in enumerate(source):
            if line_no == 0:
                sink.write(line)
                continue
            _, _, _, facility = line.split('\t')

            if not facility in facility_to_line:
                facility_to_line[facility] = []
            facility_to_line[facility].append(line)

        sampled = {}

        for k, v in sorted(facility_to_line.items(), key=lambda x: x[0]):
            for line in random.sample(v, k=min(len(v),50)):
                sink.write(line)






