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

def create_tuples(already_done):
    people=fill_people()
    left=people.copy()
    first=random.choice(tuple(left))
    choice=first
    tuples=[]
    left.remove(choice)
    while len(left) > 0:
        prev=choice
        choice=random.choice(tuple(left))
        while("%s-%s" %(prev, choice) in already_done):
            choice=random.choice(tuple(left))
        left.remove(choice)
        tuples.append((prev, choice))
    tuples.append((choice, first))
    return tuples

def main():
    already_done=get_existing_tuples()
    tuples=create_tuples(already_done)
    print_and_save_results(tuples)

if __name__ == "__main__":
    main()
