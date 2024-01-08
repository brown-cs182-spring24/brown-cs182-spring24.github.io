import sys

def calc_ungapped_align_score(seq1, seq2, score_matrix):
    score = 0
    l = len(seq1)
    for i in range(l):
        score += score_matrix[(seq1[i], seq2[i])]
    return score

def extend_seeds(seeds, db, query, k, score_matrix, x, s):
    extended_seeds = set()
    for seed in seeds:
        db_seq = db[seed[0]]
        hit_seq = db_seq[seed[1]:seed[1]+k]
        query_seq = query[seed[2]:seed[2]+k]
        seed_score = calc_ungapped_align_score(hit_seq, query_seq, score_matrix)
        right_idx_db, right_idx_query = extend_seed_right(db_seq, query, seed, seed_score, score_matrix, x)
        left_idx_db, left_idx_query = extend_seed_left(db_seq, query, seed, seed_score, score_matrix, x)
        hit_extended = db_seq[left_idx_db:right_idx_db]
        query_extended = query[left_idx_query:right_idx_query]
        final_score = calc_ungapped_align_score(hit_extended, query_extended, score_matrix)
        if final_score > s:
            extended_seeds.add((seed[0], left_idx_db, left_idx_query, hit_extended, query_extended, final_score))
    return extended_seeds

def extend_seed_right(db_seq, query, seed, seed_score, score_matrix, x):
    max_score = seed_score
    curr_score = seed_score
    max_idx_db = seed[1]+k-1
    curr_idx_db = seed[1]+k-1
    max_idx_query = seed[2]+k-1
    curr_idx_query = seed[2]+k-1
    falloff = 0
    while falloff <= x:
        try:
            curr_score += score_matrix[(db_seq[curr_idx_db+1], query[curr_idx_query+1])]
        except:
            break
        curr_idx_db += 1
        curr_idx_query += 1
        if curr_score >= max_score:
            max_score = curr_score
            max_idx_db = curr_idx_db
            max_idx_query = curr_idx_query
        falloff = max_score - curr_score
    return max_idx_db+1, max_idx_query+1

def extend_seed_left(db_seq, query, seed, seed_score, score_matrix, x):
    max_score = seed_score
    curr_score = seed_score
    max_idx_db = seed[1]
    curr_idx_db = seed[1]
    max_idx_query = seed[2]
    curr_idx_query = seed[2]
    falloff = 0
    while falloff <= x:
        if curr_idx_db-1 < 0 or curr_idx_query-1 < 0:
            break
        curr_score += score_matrix[(db_seq[curr_idx_db-1], query[curr_idx_query-1])]
        curr_idx_db -= 1
        curr_idx_query -= 1
        if curr_score >= max_score:
            max_score = curr_score
            max_idx_db = curr_idx_db
            max_idx_query = curr_idx_query
        falloff = max_score - curr_score
    return max_idx_db, max_idx_query

def list_hsps(extended_seeds):
    sorted_hsps = sorted(extended_seeds, key = lambda x : (x[5], len(x[4]), -x[0], -x[1], -x[2]), reverse=True)
    for hsp in sorted_hsps:
        print('Sequence ' + str(hsp[0]) + ' Position ' + str(hsp[1]) + ' Q-index ' + str(hsp[2]))
        print(hsp[4])
        print(hsp[3])
        print(str(hsp[5]))
        print('-----------------------------------')

if __name__=="__main__":
    db_file = open(sys.argv[1], 'r').read()
    db = db_file.splitlines()

    score_matrix = {}
    mat_file = open(sys.argv[2], 'r')
    alphabet = mat_file.readline().split()[1:]
    alph_len = len(alphabet)
    for i in range(alph_len):
        line = mat_file.readline().split()
        char1 = line[0]
        for j in range(1,alph_len):
            score_matrix[(char1, alphabet[j-1])] = int(line[j])

    seeds_file = open(sys.argv[3], 'r')
    query = seeds_file.readline().strip()
    k = int(seeds_file.readline().strip())
    t = int(seeds_file.readline().strip())
    num_seeds = int(seeds_file.readline().strip())
    seeds = []
    for line in seeds_file:
        seed_info = line.strip('\n').split(' ')
        seeds.append((int(seed_info[1]), int(seed_info[3]), int(seed_info[5])))
    
    x = int(sys.argv[4])
    s = int(sys.argv[5])

    extended_seeds = extend_seeds(seeds, db, query, k, score_matrix, x, s)
    print(query)
    print(k)
    print(t)
    print(len(extended_seeds))
    print('-----------------------------------')
    list_hsps(extended_seeds)