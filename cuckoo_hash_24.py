import random as rand
from typing import List

class CuckooHash24:
    def __init__(self, init_size: int):
        self.__num_rehashes = 0
        self.bucket_size = 4
        self.CYCLE_THRESHOLD = 10
        self.table_size = init_size
        self.tables = [[None] * init_size for _ in range(2)]

    def get_rand_idx_from_bucket(self, bucket_idx: int, table_id: int) -> int:
        rand.seed(int(str(bucket_idx) + str(table_id)))
        return rand.randint(0, self.bucket_size - 1)

    def hash_func(self, key: int, table_id: int) -> int:
        key = int(str(key) + str(self.__num_rehashes) + str(table_id))
        rand.seed(key)
        return rand.randint(0, self.table_size - 1)

    def get_table_contents(self) -> List[List[int]]:
        return self.tables

    def insert(self, key: int) -> bool:
        t = 0
        p = key
        cycle_count = 0

        while True:
            if cycle_count > self.CYCLE_THRESHOLD:
                return False
            index = self.hash_func(key,t)
            #creating an empty bucket
            if self.tables[t][index] == None:
                li = []
                li.append(key)
                self.tables[t][index] = li
                return True
            else:
                #bucket size not reached, simply insert the key
                if len(self.tables[t][index]) < self.bucket_size:
                    self.tables[t][index].append(key)
                    return True
                else:
                    #bucket full, displace random element
                    rand_idx = self.get_rand_idx_from_bucket(index, t)        
                    temp_value= self.tables[t][index][rand_idx]
                    self.tables[t][index][rand_idx] = key
                    key = temp_value
                    t = 1-t
                    cycle_count += 1  


    def lookup(self, key: int) -> bool:
        index1 = self.hash_func(key, 0)
        index2 = self.hash_func(key, 1)

        if self.tables[0][index1] is not None and key in self.tables[0][index1]:
            return True

        if self.tables[1][index2] is not None and key in self.tables[1][index2]:
            return True

        return False

    def delete(self, key: int) -> None:
        index1 = self.hash_func(key, 0)
        index2 = self.hash_func(key, 1)

        if key in self.tables[0][index1]:
            self.tables[0][index1].remove(key)
            if len(self.tables[0][index1]) == 0:
                self.tables[0][index1] = None
            return True
        elif key in self.tables[1][index2]:
            self.tables[1][index2].remove(key)
            if len(self.tables[1][index2]) == 0:
                self.tables[1][index2] = None
            return True
        else:
            return False       

    def rehash(self, new_table_size: int) -> None:
        temp = self.tables
        self.tables = [[None] * new_table_size for _ in range(2)]
        self.table_size = new_table_size
        self.__num_rehashes += 1
        
        for t in temp:
            for bucket in t:
                if bucket is not None:
                    for element in bucket:
                            self.insert(element)

