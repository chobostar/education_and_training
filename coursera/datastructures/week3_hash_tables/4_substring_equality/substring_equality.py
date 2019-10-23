# python3


class Solver:
	def __init__(self, s):
		self.s = s
		self.len_s = len(s)
		self.m1 = 7541
		self.x1 = 2
		self.hash1 = self.precompute_hashes(self.m1, self.x1)
		self.m2 = 4703
		self.x2 = 3
		self.hash2 = self.precompute_hashes(self.m2, self.x2)
		self.powers1 = [self.pow_mod(self.x1, i, self.m1) for i in range(1,self.len_s+1)]
		self.powers2 = [self.pow_mod(self.x2, i, self.m2) for i in range(1,self.len_s+1)]

	def pow_mod(self, x, y, z):
		"Calculate (x ** y) % z efficiently."
		number = 1
		while y:
			if y & 1:
				number = number * x % z
			y >>= 1
			x = x * x % z
		return numbe

	def precompute_hashes(self, p, x):
		h = [0] * (self.len_s+1)
		h[0] = 0
		for i in range(1, self.len_s+1):
			h[i] = ((x * h[i-1]) % p + ord(s[i-1])) % p
		return h

	def get_hash_of(self, hash, powers, a, p, l):
		return (hash[a+l] - ( powers[l-1] * hash[a])) % p

	def ask(self, a, b, l):
		if self.get_hash_of(self.hash1, self.powers1, a, self.m1, l) == self.get_hash_of(self.hash1, self.powers1, b, self.m1, l):
			if self.get_hash_of(self.hash2, self.powers2, a, self.m2, l) == self.get_hash_of(self.hash2, self.powers2, b, self.m2, l):
				return True #return s[a:a+l] == s[b:b+l]
		return False


class SolverNaive:
	def __init__(self, s):
		self.s = s
	def ask(self, a, b, l):
		return s[a:a+l] == s[b:b+l]


if __name__ == '__main__':
	s = input()
	q = int(input())
	solver = Solver(s)
	#solver_naive = SolverNaive(s)
	for i in range(q):
		a, b, l = map(int, input().rstrip().split())
		# a, b = random.randint(1, 9), random.randint(1, 9)
		# l = random.randint(1, 10 - max(a, b))
		#if solver.ask(a, b, l) != solver_naive.ask(a, b, l):
		#	print(a, b, l, solver.ask(a, b, l), solver_naive.ask(a, b, l))
		#print((a, b, l) if solver.ask(a, b, l) != solver_naive.ask(a, b, l) else "Ok")
		print("Yes" if solver.ask(a, b, l) else "No")
