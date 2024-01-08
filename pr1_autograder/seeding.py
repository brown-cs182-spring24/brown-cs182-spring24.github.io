import sys

def kmers_from_query(query, k):
    query_kmers_dict = {}
    l = len(query) - k + 1
    for i in range(l):
        kmer = query[i:i+k]
        try:
            query_kmers_dict[kmer].append(i)
        except:
            query_kmers_dict[kmer] = [i]
    return query_kmers_dict

def kmers_from_alph_wrap(alph, k):
    all_kmers = []
    l = len(alph)
    num_kmers = l**k
    for i in range(num_kmers):
        all_kmers.append('')
    for i in range(k):
        kmers_from_alph(all_kmers, alph, int(l**i), int(num_kmers/(l**i)), l)
    return all_kmers

def kmers_from_alph(all_kmers, alph, num1, num2, len_alph):
    base = 0
    for i in range(num1):
        a = 0
        next = num2/len_alph
        for j in range(num2):
            if j % next == 0:
                a += 1
            all_kmers[base+j] = all_kmers[base+j] + alph[a-1]
        base = num2*(i+1)

def calc_ungapped_align_score(seq1, seq2, score_matrix):
    score = 0
    l = len(seq1)
    for i in range(l):
        score += score_matrix[(seq1[i], seq2[i])]
    return score

def find_all_seeds(all_kmers, query_kmers_dict, t, score_matrix):
    all_kmers_dict = {}
    for kmer in all_kmers:
        for query_kmer in query_kmers_dict.keys():
            if calc_ungapped_align_score(kmer, query_kmer, score_matrix) > t:
                try:
                    all_kmers_dict[kmer] = all_kmers_dict[kmer] + query_kmers_dict[query_kmer]
                except:
                    all_kmers_dict[kmer] = query_kmers_dict[query_kmer]
    return all_kmers_dict

def find_seed_positions(db, all_kmers_dict, k):
    seeds = set(all_kmers_dict.keys())
    num_seqs = len(db)
    hits = []
    for i in range(num_seqs):
        seq_len = len(db[i])
        for j in range(seq_len - k + 1):
            if db[i][j:j+k] in seeds:
                for q_index in all_kmers_dict[db[i][j:j+k]]:
                    hits.append((i,j,q_index))
    return hits

def print_info(query, k, t, hits):
    print(query)
    print(k)
    print(t)
    print(len(hits))
    for hit in hits:
        print('Sequence ' + str(hit[0]) + ' Position ' + str(hit[1]) + ' Q-index ' + str(hit[2]))
        
if __name__=="__main__":
    db_file = open(sys.argv[1], 'r').read()
    db = db_file.splitlines()

    query_file = open(sys.argv[2], 'r')
    query = query_file.readline().strip()
    query_file.close

    score_matrix = {}
    mat_file = open(sys.argv[3], 'r')
    alphabet = mat_file.readline().split()[1:]
    alph_len = len(alphabet)
    for i in range(alph_len):
        line = mat_file.readline().split()
        char1 = line[0]
        for j in range(1,alph_len):
            score_matrix[(char1, alphabet[j-1])] = int(line[j])
    
    k = int(sys.argv[4])
    t = int(sys.argv[5])

    query_kmers_dict = kmers_from_query(query, k)
    all_kmers = kmers_from_alph_wrap(alphabet, k)
    all_kmers_dict = find_all_seeds(all_kmers, query_kmers_dict, t, score_matrix)
    hits = find_seed_positions(db, all_kmers_dict, k)
    print_info(query, k, t, hits)