#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys as trans
import random
import csv

# not used, does not generate strongly connected graphs
# i.e. A -> B -> C -> A is possible
def non_strongly_connected():
    left=people.copy()
    for p in people:
        choice=random.choice(tuple(left))
        # Make sure nobody gets attributed to themselves
        while choice == p:
            choice=random.choice(tuple(left))
        print("%s -> %s" % (p, choice))
        left.remove(choice)

def fill_people():
    people=set()
    with open('people.csv', newline='') as csvfile:
        for row in csvfile:
            people.add(row.strip())
    return people

def create_tuples():
    people=fill_people()
    left=people.copy()
    first=random.choice(tuple(left))
    choice=first
    tuples=[]
    left.remove(choice)
    while len(left) > 0:
        prev=choice
        choice=random.choice(tuple(left))
        left.remove(choice)
        tuples.append((prev, choice))
    tuples.append((choice, first))
    return tuples

def main():
    tuples=create_tuples()
    with open('tuples.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for t in tuples:
            print("%s -> %s" % (t[0], t[1]))
            writer.writerow(t)

if __name__ == "__main__":
    main()
