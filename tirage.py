#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys as trans
import random
import csv
import os

TUPLE_FILE='tuples.csv'
PEOPLE_FILE='people.csv'

def fill_people():
    people=set()
    with open(PEOPLE_FILE, newline='') as csvfile:
        for row in csvfile:
            people.add(row.strip())
    return people

def get_existing_tuples():
    already_done=set()
    if os.path.isfile(TUPLE_FILE):
        with open(TUPLE_FILE) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                already_done.add("%s-%s" % (row[0], row[1]))
    else:
        print("Tuple file not found, creating it.")
    return already_done

def print_and_save_results(tuples):
    with open(TUPLE_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for t in tuples:
            print("%s -> %s" % (t[0], t[1]))
            writer.writerow(t)

def tuples_loop(people, already_done):
    tuples=[]
    left=people.copy()
    first=random.choice(tuple(left))
    choice=first
    left.remove(choice)
    while len(left) > 0:
        prev=choice
        choice=random.choice(tuple(left))
        not_tested=left.copy()
        while ("%s-%s" % (prev, choice) in already_done) and len(not_tested) > 0:
            choice=random.choice(tuple(left))
            if choice in not_tested:
                not_tested.remove(choice)
        if ("%s-%s" % (prev, choice) in already_done) and len(not_tested) == 0:
            # Oops, this person has already been attributed to all remaining
            # persons. Starting over.
            print("Solution failed, starting over.")
            return []
        left.remove(choice)
        tuples.append((prev, choice))
    if "%s-%s" % (choice, first) in already_done:
        # Oops, we can't close the loop because the last pairing has
        # already been done. We have to start over.
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
        print("Failed finding a solution in %d tries." % max_retries)
        trans.exit(1)
    return tuples

def main():
    already_done=get_existing_tuples()
    tuples=create_tuples(already_done)
    print_and_save_results(tuples)

if __name__ == "__main__":
    main()
