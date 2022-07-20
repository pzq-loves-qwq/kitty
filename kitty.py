import sys, functools, random, copy
import lifelib

argv = sys.argv
if len(argv) != 2:
    print("Usage: python3 %s input-file" % argv[0])
    sys.exit(1)

# Get input file
filename = argv[1]
try:
    input_file = open(filename, "r")
    s = input_file.read()
except FileNotFoundError:
    raise ValueError("Input file %s does not exist" % filename)

# Read input file
rule = 'b3s23'
active_region = catalysts = num_cats = duration = bbx = bby = None
for line in s.split('\n'):
    try:
        words = line.split(' ')
    
        if not words:
            continue
        elif words[0] == "rule":
            rule = words[1]
        elif words[0] == "active_region":
            active_region = words[1]
        elif words[0] == "catalysts":
            catalysts = words[1:]
        elif words[0] == "num_cats":
            num_cats = int(words[1])
        elif words[0] == "duration":
            duration = int(words[1])
        elif words[0] == "bounding_box":
            bbx, bby = int(words[1]), int(words[2])
    except:
        raise ValueError("Invalid line: %s" % line)

sess = lifelib.load_rules(rule)
lt = sess.lifetree()

# Convert RLEs into lt.pattern's:
active_region = lt.pattern(active_region)
catalysts = list(map(lt.pattern, catalysts))

# Translate active region to center of bounding box
rect = active_region.bounding_box
active_region = active_region((bbx - rect[2]) // 2, (bby - rect[3]) // 2)

# Helper funcs:
def test_cats(active_region, cat): # Test a set of catalysts
    if active_region & cat: # sanity check
        return False
    if cat[1] != cat:
        return False

    test_pattern = active_region | cat
    test_pattern = test_pattern[duration]
    return (test_pattern & cat) == cat

def move_cats(cat): # Returns a list of all possible translations/reflections of `cat` fitting the bounding box
    refl = []
    for transform in ['flip', 'rot180', 'identity', 'transpose', 'flip_x', 'flip_y', 'rot90', 'rot270', 'swap_xy', 'swap_xy_flip', 'rcw', 'rccw']:
        cat2 = cat(transform, 0, 0)
        if cat2 not in refl:
            refl.append(cat2)

    l = []
    for patt in refl:
        pattx, patty = patt.bounding_box[2:]
        for i in range(bbx - pattx + 1):
            for j in range(bby - patty + 1):
                l.append(patt(i, j))
    return l

# Do the search!
catalysts = map(move_cats, catalysts)
catalysts = functools.reduce(lambda x, y: x + y, catalysts)

def dfs(i, patt):
    if i == num_cats:
        if test_cats(active_region, patt):
            print((active_region | patt).rle_string())
            sys.stdout.flush()
        return

    catalysts2 = copy.copy(catalysts)
    random.shuffle(catalysts2)
    for cat in catalysts2:
        if not patt & cat:
            dfs(i + 1, patt | cat)

dfs(0, lt.pattern("!"))
