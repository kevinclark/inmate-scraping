facility_map = {
    'HIGH SECURITY': 'PO Box 8200, Cranston, RI 02920',
     'INTAKE SERVICE CNTR': 'PO Box 8249, Cranston, RI 02920',
     'MAXIMUM SECURITY': 'PO Box 8273, Cranston, RI 02920',
     'MEDIUM SECURITY': 'MEDIUM SECURITY',
     'MINIMUM SECURITY': 'PO Box 8212, Cranston, RI 02920',
     'WOMENS FACILITY 1': 'PO Box 8312, Cranston, RI 02920'
}


with open('data/cleaned.tsv', 'w') as cleaned:
    with open('data/inmates.tsv') as inmates:
        for line_no, line in enumerate(inmates):
            if line_no == 0:
                cleaned.write(line)
                continue
            parts = line.strip().split('\t')
            cleaned.write('\t'.join(parts[0:-1] + [facility_map[parts[-1]]]))
            cleaned.write('\n')
