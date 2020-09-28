"""
Parses a markdown file and saves the results in a JSON file.

Usage:
    python md2json.py /path/to/input /path/to/output
"""

import json
import re
import sys


def main(in_file, out_file):
    with open(in_file, 'r') as thefile:
        lines = thefile.readlines()

    lines = [l.rstrip() for l in lines]

    computations = parse_computations(lines)

    with open(out_file, 'w') as writefile:
        json.dump(computations, writefile, indent=4)


def extract(text, brackets):
    regexp = r"\{}.*?\{}".format(brackets[0], brackets[1])
    result = re.search(regexp, text)
    return result[0][1:-1]


def extract_github_user(github_url):
    return github_url.split('/')[-1]


def extract_person(line):
    person = dict()
    if '[' in line:
        name = extract(line, '[]')
    else:
        name = line.split(':')[-1]
        name = name.lstrip()
    person['first_name'], person['last_name'] = name.split(' ')

    if '(' in line:
        github = extract(line, '()')
        github_user = extract_github_user(github)
        person['github_url'] = github
        person['github_user'] = github_user
    else:
        person['github_url'] = ''
        person['github_user'] = ''

    return person


def parse_computations(lines):
    computations = list()

    for k, line in enumerate(lines):
        if not line:
            continue
        if line[0] == '-':
            computation = dict()
            computation['name'] = line[2:]
        elif line[:4] == '  - ':
            if 'Algorithm Developer' in line:
                computation['algo_dev'] = extract_person(line)
            elif 'Computation Creator' in line:
                computation['comp_creator'] = extract_person(line)
            elif 'Maintainer' in line:
                computation['maintainer'] = extract_person(line)
            elif 'Repository' in line:
                computation['repository'] = line.split(': ')[-1]
            elif 'Paper' in line:
                paper = dict()
                paper['citation'] = lines[k + 1].split('- ')[-1]
                paper['url'] = lines[k + 2].split('- ')[-1]
                computation['paper'] = paper
            elif 'Status' in line:
                computation['status'] = line.split(': ')[-1].lower()
                computations.append(computation)
    return computations


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
