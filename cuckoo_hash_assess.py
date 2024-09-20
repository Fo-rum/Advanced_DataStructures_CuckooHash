# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash24:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.bucket_size = 4
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.table = [None]*self.table_size

	def get_rand_bucket_index(self, bucket_idx: int) -> int:
		# you must use this function when you need to evict a random key from a bucket. this function
		# randomly chooses an index from a given cell index. this ensures that the random
		# index chosen by your code and our test script match.
		#
		# for example, if you need to remove a random element from the bucket at table index 5,
		# you will call get_rand_bucket_index(5) to determine which key from that bucket to evict, i.e. if get_random_bucket_index(5) returns 2, you
		# will evict the key at index 2 in that bucket.
		rand.seed(int(str(bucket_idx)))
		return rand.randint(0, self.bucket_size-1)

	def hash_func(self, key: int, func_id: int) -> int:
		# access h0 via func_id=0, access h1 via func_id=1
		key = int(str(key) + str(self.__num_rehashes) + str(func_id))
		rand.seed(key)
		result = rand.randint(0, self.table_size-1)
		return result

	def get_table_contents(self) -> List[Optional[List[int]]]:
		# the buckets should be implemented as lists. Table cells with no elements should still have None entries.
		return self.table

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		# TODO
		cycle_count = 0
		t = 0
		while True:
			if cycle_count > self.CYCLE_THRESHOLD:
				return False
			h0_index = self.hash_func(key,t)
			h1_index = self.hash_func(key, 1-t)

			#initial insertion using h0_index
			if self.table[h0_index] == None:
				li = []
				li.append(key)
				self.table[h0_index] = li
				return True

			#insertion using h0_index if its bucket size not full
			elif len(self.table[h0_index]) < self.bucket_size:
				self.table[h0_index].append(key)
				return True
			
			#if h0 bucket full, looking for h1_index bucket
			elif self.table[h1_index] == None:
				li = []
				li.append(key)
				self.table[h1_index] = li
				return True
			
			#insertion using h1_index if its bucket size not full
			elif len(self.table[h1_index]) < self.bucket_size:
				self.table[h1_index].append(key)
				return True

			else:
				#collision found, so compute random index of the key to be displaced and swap it
				rand_idx = self.get_rand_bucket_index(h0_index)
				key, self.table[h0_index][rand_idx] = self.table[h0_index][rand_idx], key
				cycle_count += 1

	def lookup(self, key: int) -> bool:
		# TODO
		t = 0
		h0_index = self.hash_func(key, t)
		h1_index = self.hash_func(key, 1-t)

		if self.table[h0_index] is not None and key in self.table[h0_index]:
			return True
		
		if self.table[h1_index] is not None and key in self.table[h1_index]:
			return True
		
		return False
		
	def delete(self, key: int) -> None:
		# TODO
		t = 0
		h0_index = self.hash_func(key, t)
		h1_index = self.hash_func(key,1-t)

		if key in self.table[h0_index]:
			self.table[h0_index].remove(key)
			#after removal if the length of the bucket becomes 0, reset it to None
			if len(self.table[h0_index]) == 0:
				self.table[h0_index] = None
			return True
		elif key in self.table[h1_index]:
			self.table[h1_index].remove(key)
			if len(self.table[h1_index]) == 0:
				self.table[h1_index] = None
			return True
		else:
			return False

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1
		self.table_size = new_table_size # do not modify this line
		# TODO
		temp = self.table
		self.table = [None]*self.table_size
		for t in temp:
			if t is not None:
				for element in t:
					#if element is not None:
						self.insert(element)
		
	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
