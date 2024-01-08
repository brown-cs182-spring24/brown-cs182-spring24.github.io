import sys


def check_equivalence_local(input_file, scoring_matrix, gap_penalty, result, expected):
    if gap_penalty == "negInf":
        gap_penalty = float('-inf')
    else:
        gap_penalty = int(gap_penalty)
    with open(input_file, "r") as f:
        seq1 = f.readline().strip()
        seq2 = f.readline().strip()
    with open(scoring_matrix, "r") as f:
        score_dict = dict()
        label2 = f.readline()
        splabel2 = label2.split()
        for i in range(1, len(splabel2)):
            score_dict[("-", splabel2[i])] = gap_penalty
            score_dict[(splabel2[i], "-")] = gap_penalty
        line = label2
        while line != "":
            line = f.readline()
            spline = line.split()
            for i in range(1, len(spline)):
                score_dict[(spline[0], splabel2[i])] = int(spline[i])
    result_seq1 = result[0]
    result_seq2 = result[1]
    result_score = int(result[2])
    expected_score = int(expected[2])
    score = 0
    result_seq1_ungapped = ""
    result_seq2_ungapped = ""
    if not len(result_seq1) == len(result_seq2):
        return False
    for i in range(len(result_seq1)):
        if result_seq1[i] == "-" and result_seq2[i] == "-":
            return False
        score += score_dict[(result_seq1[i], result_seq2[i])]
        if result_seq1[i] != "-":
            result_seq1_ungapped += result_seq1[i]
        if result_seq2[i] != "-":
            result_seq2_ungapped += result_seq2[i]
    if result_seq1_ungapped in seq1 and result_seq2_ungapped in seq2:
        seqs_correct = True
    else:
        seqs_correct = False
    if seqs_correct and score == expected_score and score == result_score:
        test_correct = True
    else:
        test_correct = False
    return test_correct


def check_equivalence_seeding(result, expected):
    result = result.split('\n')
    expected = expected.split('\n')
    num_seeds_found = int(result[3])
    res_seeds = result[4:]
    sol_seeds = expected[4:]

    correct_ordering = True
    for i in range(num_seeds_found):
        if sol_seeds[i] != res_seeds[i]:
            correct_ordering = False

    seeds_not_found = set(sol_seeds) - set(res_seeds)
    extra_seeds_found = set(res_seeds) - set(sol_seeds)
    if len(seeds_not_found) == 0 and len(extra_seeds_found) == 0 and correct_ordering and num_seeds_found == len(res_seeds):
        test_correct = True
    else:
        test_correct = False
    return test_correct, sorted(list(seeds_not_found)), sorted(list(extra_seeds_found))


def check_equivalence_extension(result, expected):
    result = result.split('\n')  # result[0:3] are inputs, result[4] is the number of HSPs
    expected = expected.split('\n')

    num_hsps_found = int(result[3])
    res_hsps = []
    sol_hsps = []
    for i in range(5, len(result), 5):  # individual HSPs start on line 5, in groups of 5
        # [i] = position string, [i+1] = query, [i+2] = database, [i+3] = score, [i+4] = dash-separator line
        hsp = "{} {} {} {}".format(result[i], result[i+1], result[i+2], result[i+3])
        res_hsps.append(hsp)
    for i in range(5, len(expected), 5):
        hsp = "{} {} {} {}".format(expected[i], expected[i+1], expected[i+2], expected[i+3])
        sol_hsps.append(hsp)

    correct_ordering = True
    for i in range(num_hsps_found):
        if sol_hsps[i] != res_hsps[i]:
            correct_ordering = False

    hsps_not_found = set(sol_hsps) - set(res_hsps)
    extra_hsps_found = set(res_hsps) - set(sol_hsps)
    if len(hsps_not_found) == 0 and len(extra_hsps_found) == 0 and correct_ordering and num_hsps_found == len(res_hsps):
        test_correct = True
    else:
        test_correct = False
    return test_correct, sorted(list(hsps_not_found)), sorted(list(extra_hsps_found))


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == "local":
        # command is check_equivalence local <sequences.txt> <matrix.m> <gap_penalty> $result $expected
        result = sys.argv[5]
        expected = sys.argv[6]
        result = result.split()
        expected = expected.split()
        if len(expected) == 1:  # empty test case
            if sys.argv[5] == sys.argv[6]:
                print("Test case passed")
            else:
                print("Test case failed")
        elif len(result) < 3:
            print("Test case failed")
        else:
            passed = check_equivalence_local(sys.argv[2], sys.argv[3], sys.argv[4], result, expected)
            if passed:
                print("Test case passed")
            else:
                print("Test case failed")
    elif mode == "seeding":
        # command is check_equivalence seeding $result $expected
        result = sys.argv[2]
        expected = sys.argv[3]
        passed, missing_seeds, extra_seeds = check_equivalence_seeding(result, expected)
        if passed:
            print("Test case passed")
        else:
            print("Test case failed")
    elif mode == "extension":
        # command is check_equivalence extension $result $expected
        result = sys.argv[2]
        expected = sys.argv[3]
        passed, missing_hsps, extra_hsps = check_equivalence_extension(result, expected)
        if passed:
            print("Test case passed")
        else:
            print("Test case failed")
