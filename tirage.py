#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys as trans
import random
import csv
import os
import argparse

TUPLE_FILE = 'tuples.csv'
PEOPLE_FILE = 'people.csv'
args = None

def parse_command_line():
    global args
    parser = argparse.ArgumentParser(description="Make random attributions of people for a secret santa-style gift exchange. Results will always be a loop (fully connected graph) and no similar attribution will be made twice in successive runs.\nPlease indicate people in file %s.\nPrevious attributions are stored in file %s." % (PEOPLE_FILE, TUPLE_FILE))
    group_main = parser.add_argument_group('Options')
    group_main.add_argument('-q', '--quiet', action='store_const', const=True, help='Display results only, no failure messages.')
    group_main.add_argument('-m', '--max-retries', action='store', type=int, default=10000, help='Max number of attempts to find a solution.')
    args = parser.parse_args()

def fill_people():
    people = set()
    if not os.path.isfile(PEOPLE_FILE):
        print("Please create file %s. Indicate one person per line." % PEOPLE_FILE)
        trans.exit(1)
    with open(PEOPLE_FILE, newline='') as csvfile:
        for row in csvfile:
            people.add(row.strip())
    return people

def get_existing_tuples():
    already_done = set()
    if os.path.isfile(TUPLE_FILE):
        with open(TUPLE_FILE) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                already_done.add("%s-%s" % (row[0], row[1]))
    else:
        if not args.quiet:
            print("Tuple file not found, creating it.")
    return already_done

def print_and_save_results(tuples):
    with open(TUPLE_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for t in tuples:
            print("%s -> %s" % (t[0], t[1]))
            writer.writerow(t)

def tuples_loop(people, already_done):
    tuples = []
    left = people.copy()
    first = random.choice(tuple(left))
    choice = first
    left.remove(choice)
    while len(left) > 0:
        prev = choice
        choice = random.choice(tuple(left))
        not_tested=left.copy()
        while ("%s-%s" % (prev, choice) in already_done) and len(not_tested) > 0:
            choice=random.choice(tuple(left))
            if choice in not_tested:
                not_tested.remove(choice)
        if ("%s-%s" % (prev, choice) in already_done) and len(not_tested) == 0:
            # Oops, this person has already been attributed to all remaining
            # persons. Starting over.
            if not args.quiet:
                print("Solution failed, starting over.")
            return []
        left.remove(choice)
        tuples.append((prev, choice))
    if "%s-%s" % (choice, first) in already_done:
        # Oops, we can't close the loop because the last pairing has
        # already been done. We have to start over.
        if not args.quiet:
            print("Ending the loop failed, starting over.")
        return []
    tuples.append((choice, first))
    return tuples

def create_tuples(already_done, max_retries=1000):
    people=fill_people()
    ok=False
    retries=0
    tuples=[]
    while len(tuples) == 0 and retries < max_retries:
        tuples=tuples_loop(people, already_done)
        retries += 1
    if retries == max_retries:
        if not args.quiet:
            print("Failed finding a solution in %d tries." % max_retries)
        trans.exit(1)
    return tuples

def main():
    parse_command_line()
    already_done=get_existing_tuples()
    tuples=create_tuples(already_done, max_retries=args.max_retries)
    print_and_save_results(tuples)

if __name__ == "__main__":
    main()
