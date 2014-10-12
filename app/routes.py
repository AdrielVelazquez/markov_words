from flask import request, Blueprint
import pickle

import trainer

quiz = Blueprint('markov', __name__, url_prefix='/markov')
model_data = pickle.load(open('trainer_text/gib_model.pki', 'rb'))
word_set = set()
with open('trainer_text/wordsEn.txt', "rb") as word_list:
    for line in word_list:
        word_set.add(line.strip().lower())

@quiz.route("/word/<word>", methods=['GET'])
def word_identifier(word):
    '''
    Some additional smoothing is happening upon request, which basically verifies the word against a common set a words
    If no match, applies an additional penalty to the final word.
    '''
    model_mat = model_data['mat']
    threshold = model_data['thresh']
    if word.lower() in word_set:
        prob = trainer.avg_transition_prob(word, model_mat)
        if prob < threshold:
            prob += (threshold - prob)
        word_bool = True
    else:
        prob = trainer.avg_transition_prob(word, model_mat)
        prob -= 0.024
        word_bool = prob > threshold
    return {"Word": word_bool, "Input": word, "Prob": prob, "Threshold": threshold}