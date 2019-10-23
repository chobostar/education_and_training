# python3


class RabinKarp(object):
    def __init__(self, pattern, text):
        self.pattern = pattern
        self.len_p = len(self.pattern)
        self.text = text
        self.len_t = len(self.text)
        self.hashes = [0] * (len(text)-len(pattern) + 1)
        self._multiplier = 1
        self._prime = 60919

    def _poly_hash(self, s):
        ans = 0
        i = 0
        for c in s:
            ans = (ans + ord(c) * self._multiplier ** i) % self._prime
            i += 1
        return ans

    def _precompute_hashes(self):
        s = self.text[-len(self.pattern):]
        self.hashes[len(self.text)-len(self.pattern)] = self._poly_hash(s)
        y = 1
        for i in range(1, self.len_p+1):
            y = (y * self._multiplier) % self._prime
        for i in reversed(range(self.len_t-self.len_p)):
            self.hashes[i] = ((self._multiplier * self.hashes[i+1]) + ord(self.text[i]) - (y * ord(self.text[i + self.len_p]))) % self._prime

    def _get_occurrences(self):
        result = []
        p_hash = self._poly_hash(self.pattern)
        self._precompute_hashes()
        for i in range(self.len_t-self.len_p+1):
            if p_hash != self.hashes[i]:
                continue
            if self.pattern == self.text[i:i+self.len_p]:
                result.append(i)
        return result

    def print_occurences(self):
        print(' '.join(map(str, self._get_occurrences())))

def read_input():
    return (input().rstrip(), input().rstrip())

if __name__ == '__main__':
    algorithm = RabinKarp(*read_input())
    algorithm.print_occurences()

