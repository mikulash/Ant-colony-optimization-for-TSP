import random
import sys
import json

instance_path = sys.argv[1]
output_path = sys.argv[2]

with open(instance_path) as f:
    instance = json.load(f)

sol = [i for i in range(len(instance['Matrix']))]

with open(output_path, 'w') as f:
    json.dump(sol, f)
