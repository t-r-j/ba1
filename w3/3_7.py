import sys
import random
import copy

def main():
	lines = [line.strip() for line in open(sys.argv[1])]
	K_T_N = lines[0].split()
	K = int(K_T_N[0])
	T = int(K_T_N[1])
	N = int(K_T_N[2])
	kmers = generate_kmers(lines, 1, K)

	# don't settle for one random iteration, do it multiple times as suggested in the discussion forum
	GlobalBestMotifs = rand_init_motifs(kmers, T)
	GlobalBestMotifs_Score = score(GlobalBestMotifs, K)

	g_counter = 0
	# don't settle for one random iteration, do it multiple times as suggested in the discussion forum
	while(g_counter < 30):
		BestMotifs = rand_init_motifs(kmers, T)
		BestMotif_Score = score(BestMotifs, K)
		motifs = copy.deepcopy(BestMotifs)
		itr_counter = 0
		while(itr_counter < N):
			rand_int = random.randint(0, T - 1)
			profile = generate_profile_with_pseudocounts(motifs, K, rand_int)
			motifs[rand_int] = Random(kmers[rand_int], profile)
			candidate_motifs_score = score(motifs, K)
			if(candidate_motifs_score < BestMotif_Score):
				BestMotifs = copy.deepcopy(motifs)
				BestMotif_Score = candidate_motifs_score
			itr_counter += 1

		if(BestMotif_Score <= GlobalBestMotifs_Score):
			GlobalBestMotifs_Score = BestMotif_Score
			GlobalBestMotifs = copy.deepcopy(BestMotifs)
			print 'GLOABL ITERATION ==>', g_counter, ' GLOBAL BEST_SCORE ==> ', GlobalBestMotifs_Score, 'BEST MOTIF ==>', GlobalBestMotifs
		g_counter += 1
	print_motifs(GlobalBestMotifs)

def Random(kmer_row, profile):
	probabilities = []
	for kmer in kmer_row:
		probability = get_probability(kmer, profile)
		probabilities.append(probability)
	p_array = gen_probability_array(probabilities)
	p_sum = p_array[len(p_array) - 1]
	rand_int = random.randint(0, p_sum - 1)
	counter = 0
	while(counter < len(p_array)):
		if(rand_int <= p_array[counter]):
			return kmer_row[counter]
		counter += 1
	return None


def gen_probability_array(probabilities):
	cumulative_probabilities = 0
	p_array = []
	for probability in probabilities:
		cumulative_probabilities += int(1000000000*probability)
		p_array.append(cumulative_probabilities)
	return p_array

def score(motifs, K):
	score = 0
	index = 0
	motifs_length = len(motifs)
	score_matrix = [[0, 0, 0, 0, 0] for x in range(K)] # list of A,C,G,T, -sum counts [[3,4,1,2,-10] [1,5,3,1,-10]...]
	while(index < motifs_length):
		motif_index = 0
		while(motif_index < K):
			score_matrix[motif_index][0] += (1 if motifs[index][motif_index] == 'A' else 0)
			score_matrix[motif_index][1] += (1 if motifs[index][motif_index] == 'C' else 0)
			score_matrix[motif_index][2] += (1 if motifs[index][motif_index] == 'G' else 0)
			score_matrix[motif_index][3] += (1 if motifs[index][motif_index] == 'T' else 0)
			score_matrix[motif_index][4] = -1 * (score_matrix[motif_index][0] + score_matrix[motif_index][1] + score_matrix[motif_index][2] + score_matrix[motif_index][3])
			motif_index += 1
		index += 1
	# now calculate the score ==> sum of all [total_sum (which is negative) + max_sum element]
	for element in score_matrix:
		score += (-1 * (element[4] + max(element)))
	return score

def get_probability(kmer, profile):
	index = 0
	probability = 1.0
	while(index < len(kmer)):
		probability *= profile[index][kmer[index]]
		index += 1
	return probability

def generate_profile_with_pseudocounts(motifs, K, avoid_row):
	profile = [{'A':1.0, 'C':1.0, 'G':1.0, 'T':1.0} for x in range(K)] # initializing with 1 because of pseudocounts
	index = 0
	motif_count = len(motifs)

	# calculate the counts
	motif_counter = 0
	while (motif_counter < motif_count):
		index = 0
		if(motif_counter != avoid_row):
			while(index < K):
				profile[index]['A'] += (1 if motifs[motif_counter][index] == 'A' else 0)
				profile[index]['C'] += (1 if motifs[motif_counter][index] == 'C' else 0)
				profile[index]['G'] += (1 if motifs[motif_counter][index] == 'G' else 0)
				profile[index]['T'] += (1 if motifs[motif_counter][index] == 'T' else 0)
				index += 1
		motif_counter += 1

	# calculate the percentages now
	motif_count += (4 - 1) # accomodating the pseudocounts. Subtracting 1 as 1 row is to be removed
	for dna_dict in profile:
		dna_dict['A'] = dna_dict['A']/motif_count
		dna_dict['C'] = dna_dict['C']/motif_count
		dna_dict['G'] = dna_dict['G']/motif_count
		dna_dict['T'] = dna_dict['T']/motif_count
	return profile

def rand_init_motifs(kmers, T):
	index = 0
	best_motifs = []
	kmer_max_len = len(kmers[0])
	while(index < T):
		rand_int = random.randint(0, kmer_max_len - 1)
		best_motifs.append(kmers[index][rand_int])
		index += 1
	return best_motifs

# generate k sized strings from the source strings (lines)
def generate_kmers(lines, s_index, K):
	max_line_num = len(lines)
	counter = s_index
	kmer_rows = []
	while(counter < max_line_num):
		kmer_rows.append(get_kmers(lines[counter], K))
		counter += 1
	return kmer_rows

def get_kmers(str, K):
	kmers = []
	index = 0
	while(index <= len(str) - K):
		kmers.append(list(str[index : index + K]))
		index += 1
	return kmers

def print_motifs(motifs):
	for kmer in motifs:
		print "".join(kmer)


if __name__ == '__main__':
	main()