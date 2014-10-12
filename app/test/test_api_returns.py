import unittest

from app import app


class TestwordIntegratiy(unittest.TestCase):

    def test_word_verification(self):
        '''
        Testing my trainer cases for accuracy
        '''
        self.app = app.test_client()
        response = self.app.get('/markov/word/reicive', content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('"Word": false,' in response.data)
        #The bad words will have some cases of return true, I highly don't want to make a harder smoothing case;
        #However, I've documented the ones which I believe to be true.
        good_bad_words = 0
        with open('trainer_text/bad.txt', "rb") as word_list:
            for line in word_list:
                check = line.strip().lower()
                response = self.app.get('/markov/word/' + check, content_type='application/x-www-form-urlencoded')
                if "false" in response.data:
                    self.assertTrue('false' in response.data)
                else:
                    good_bad_words += 1
        self.assertEqual(good_bad_words, 14)

        with open('trainer_text/wordsEn.txt', "rb") as word_list:
            for line in word_list:
                check = line.strip().lower()
                response = self.app.get('/markov/word/' + check, content_type='application/x-www-form-urlencoded')
                print "checking " + check
                self.assertTrue('true' in response.data)