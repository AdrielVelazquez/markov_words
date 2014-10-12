import math
import pickle

accepted_chars = 'abcdefghijklmnopqrstuvwxyz '

pos = dict([(char, idx) for idx, char in enumerate(accepted_chars)])

def normalize(line):
    """ Return only the subset of chars from accepted_chars.
    This helps keep the  model relatively small by ignoring punctuation, 
    infrequenty symbols, etc. """
    return [c.lower() for c in line if c.lower() in accepted_chars]

def ngram(n, l):
    """ Return all n grams from l after normalizing """
    filtered = normalize(l)
    for start in range(0, len(filtered) - n + 1):
        yield ''.join(filtered[start:start + n])

def train():
    '''
    This trainer follows closely the following trainer
    https://github.com/rrenaud/Gibberish-Detector/blob/master/gib_detect_train.py
    '''

    k = len(accepted_chars)
    # Assume we have seen 10 of each character pair.  This acts as a kind of
    # prior or smoothing factor.  This way, if we see a character transition
    # live that we've never observed in the past, we won't assume the entire
    # string has 0 probability.
    # the counts are in the following format
    # 27 rows and 27 columns with 729 possibilities.
    # Each row and column represents a letter and a final space
    # There are some basic words that aren't matched, which I'm going to do it another way.
    counts = [[10 for i in xrange(k)] for i in xrange(k)]

    # Count transitions from big text file, taken
    # from http://norvig.com/spell-correct.html
    for line in open('trainer_text/big.txt'):
        for a, b in ngram(2, line):
            counts[pos[a]][pos[b]] += 1

    for line in open('trainer_text/wordsEn.txt'):
        for a, b in ngram(2, line):
            counts[pos[a]][pos[b]] += 1

    for line in open('trainer_text/double_vowels.txt'):
        for a, b in ngram(2, line):
            counts[pos[a]][pos[b]] += 1


    # Normalize the counts so that they become log probabilities.  
    # We use log probabilities rather than straight probabilities to avoid
    # numeric underflow issues with long texts.
    # This contains a justification:
    # http://squarecog.wordpress.com/2009/01/10/dealing-with-underflow-in-joint-probability-calculations/
    for i, row in enumerate(counts):
        s = float(sum(row))
        for j in xrange(len(row)):
            row[j] = math.log(row[j] / s)

    # Find the probability of generating a few arbitrarily choosen good and
    # bad phrases.
    good_probs = [avg_transition_prob(l, counts) for l in open('trainer_text/good.txt')]
    bad_probs = [avg_transition_prob(l, counts) for l in open('trainer_text/bad.txt')]
    # And pick a threshold halfway between the worst good and best bad inputs.
    thresh = (min(good_probs) + max(bad_probs)) / 2
    print thresh, sum(bad_probs)/float(len(bad_probs))
    pickle.dump({'mat': counts, 'thresh': thresh}, open('trainer_text/gib_model.pki', 'wb'))

def avg_transition_prob(l, log_prob_mat):
    """ Return the average transition prob from l through log_prob_mat. """
    log_prob = 0.0
    transition_ct = 0
    for a, b in ngram(2, l):
        log_prob += log_prob_mat[pos[a]][pos[b]]
        transition_ct += 1
    # The exponentiation translates from log probs to probs.
    return math.exp(log_prob / (transition_ct or 1))

if __name__ == '__main__':
    train()