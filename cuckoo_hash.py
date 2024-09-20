# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import math
import random as rand
from typing import List, Optional


class CuckooHash:
    def __init__(self, init_size: int):
        self.__num_rehashes = 0
        self.CYCLE_THRESHOLD = 10

        self.table_size = init_size
        self.tables = [[None] * init_size for _ in range(2)]

    def hash_func(self, key: int, table_id: int) -> int:
        key = int(str(key) + str(self.__num_rehashes) + str(table_id))
        rand.seed(key)
        return rand.randint(0, self.table_size - 1)

    def get_table_contents(self) -> List[List[int]]:
        return self.tables

    # you should *NOT* change any of the existing code above this line
    # you may however define additional instance variables inside the __init__ method.

    def insert(self, key: int) -> bool:
        t = 0
        p = key
        cycle_count = 0

        while True:
            index = self.hash_func(key, t)

            p, self.tables[t][index] = self.tables[t][index], p

            if p is None:
                return True

            if cycle_count >= self.CYCLE_THRESHOLD:
                return False

            t = 1 - t
            cycle_count += 1
            key = p

    def lookup(self, key: int) -> bool:
        # TODO
        index1 = self.hash_func(key, 0)
        index2 = self.hash_func(key, 1)
        if self.tables[0][index1] is not None and self.tables[0][index1] == key:
            return True
        if self.tables[1][index2] is not None and self.tables[1][index2] == key:
            return True

        return False

    def delete(self, key: int) -> None:
        # TODO
        index1 = self.hash_func(key, 0)
        index2 = self.hash_func(key, 1)
        if self.tables[0][index1] == key:
            self.tables[0][index1] = None
        if self.tables[1][index2] == key:
            self.tables[1][index2] = None

    def rehash(self, new_table_size: int) -> None:
        self.__num_rehashes += 1
        self.table_size = new_table_size  # do not modify this line
        # TODO
        temp = self.tables
        self.tables = [[None] * self.table_size for _ in range(2)]
        for t in temp:
            for element in t:
                if element is not None:
                    self.insert(element)



# feel free to define new methods in addition to the above
# fill in the definitions of each required member function (above),
# and for any additional member functions you define



