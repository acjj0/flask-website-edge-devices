import random

birdcodes = ["norcar","spotow","sonspa","redcro","newbla","eursta","gbwwre1","houspa","rewbla","houwre"]

for i in range(1000):
    random_index = random.randint(0, len(birdcodes) - 1)
    print(birdcodes[random_index])