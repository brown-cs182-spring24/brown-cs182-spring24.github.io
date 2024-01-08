"""
This program implements local sequence alignment.

	Input:	(1) a file containing two sequences to be aligned
			(2) a file containing the scoring matrix to be used
			(3) a gap penalty, either a nonpositive integer or "negInf"

	Output:	(1) the optimal local alignment for both sequences
			(2) the score of this alignment
"""

import sys

def main(argv):

	# read in the two sequences to be aligned
	readSeqs = open(argv[1], 'r')
	seq1 = readSeqs.readline().strip("\n")
	seq2 = readSeqs.readline().strip("\n")
	readSeqs.close()
	
	# read in the scoring matrix for reference later
	readScorer = open(argv[2], 'r')
	scores = []
	for line in readScorer:
		scores.append(line.split())
	readScorer.close()
	
	# generate the matrices for local alignment & traceback
	# align seq1 along the top and seq2 down the left side
	local = [[0 for i in range(len(seq1) + 1)] for i in range(len(seq2) + 1)]
	trcbk = [[0 for i in range(len(seq1) + 1)] for i in range(len(seq2) + 1)]
	
	# handle the nonpositive integer case first
	if argv[3] != "negInf":
		
		# store the gap penalty value for reference later
		gapPenalty = int(argv[3])

		# fill in both matrices w/ pairwise alignment algorithm; record final position of max score
		maxScore = 0
		maxRow = -1
		maxCol = -1
		for row in range(1, len(seq2) + 1):
			for col in range(1, len(seq1) + 1):
				top = local[row - 1][col] + gapPenalty
				diag = local[row - 1][col - 1] + score(seq1[col - 1], seq2[row - 1], scores)
				left = local[row][col - 1] + gapPenalty
				local[row][col] = max(0, top, diag, left)
				if(local[row][col] >= maxScore):
					maxScore = local[row][col]
					maxRow = row
					maxCol = col
				if local[row][col] == left:
					trcbk[row][col] = -1
				elif local[row][col] == top:
					trcbk[row][col] = 1
				# don't need to place 0 for local[row][col] == diag b/c it's already true

	else: # gapPenalty = negInf, so just assess all possible ungapped alignments
		
		# fill in first row & column of local alignment matrix using initial scores
		for col in range(1, len(seq1) + 1):
			local[1][col] = max(0, score(seq1[col - 1], seq2[0], scores))
		for row in range(1, len(seq2) + 1):
			local[row][1] = max(0, score(seq1[0], seq2[row - 1], scores))

		# fill in both matrices using diagonal-only alignment; record final position of max score
		maxScore = 0
		maxRow = -1
		maxCol = -1
		for row in range(2, len(seq2) + 1):
			for col in range(2, len(seq1) + 1):
				local[row][col] = (max(0, local[row - 1][col - 1] +
					score(seq1[col - 1], seq2[row - 1], scores)))
				if local[row][col] >= maxScore:
					maxScore = local[row][col]
					maxRow = row
					maxCol = col
				# leave all traceback entries as 0 since only diagonal alignments are considered

	# use the stored values of maxScore, maxRow and maxCol
	# to reconstruct the optimal local alignment in reverse
	seq1Optimal = ""
	seq2Optimal = ""
	row = maxRow
	col = maxCol
	while local[row][col] > 0: # stop when end is reached
		if trcbk[row][col] == 1 or col == 0: # traceback up
			seq1Optimal = '-' + seq1Optimal
			seq2Optimal = seq2[row - 1] + seq2Optimal
			row -=1
		elif trcbk[row][col] == -1 or row == 0: # traceback left
			seq1Optimal = seq1[col - 1] + seq1Optimal
			seq2Optimal = '-' + seq2Optimal
			col -=1
		else: #traceback diagonally
			seq1Optimal = seq1[col - 1] + seq1Optimal
			seq2Optimal = seq2[row - 1] + seq2Optimal
			row -= 1
			col -= 1

	# output optimal local alignments and score
	print(seq1Optimal)
	print(seq2Optimal)
	print(maxScore)

# returns the score of a pairing based on the scoring matrix
def score(a, b, scores):
	for row in range(len(scores)):
		if scores[row][0] == a:
			for col in range(len(scores)):
				if scores[0][col] == b:
					return int(scores[row][col])

if __name__ == '__main__':
	main(sys.argv)