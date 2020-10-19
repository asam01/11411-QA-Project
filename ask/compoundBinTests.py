import unittest
from compoundBinary import ask_compound_bin_question as bin_q

class TestFirstPerson (unittest.TestCase):

    def testSimpleCases(self):
        s1 = 'I like ice cream a lot.'
        q1 = 'Do I like ice cream a lot?'

        s2 = 'I run in the park every week.'
        q2 = 'Do I run in the park every week?'

        s3 = 'I like the grocery store.'
        q3 = 'Do I like the grocery store?'

        self.assertEqual(q1, bin_q(s1))
        self.assertEqual(q2, bin_q(s2))
        self.assertEqual(q3, bin_q(s3))

    def testComplexCases(self):
        s1 = 'I go shopping every month.'
        q1 = 'Do I go shopping every month?'

        s2 = 'I always carry my purse with me.'
        q2 = 'Do I always carry my purse with me?'

        self.assertEqual(q1, bin_q(s1))
        self.assertEqual(q2, bin_q(s2))

class TestThirdPersonSingular (unittest.TestCase):

    def testSimpleCases(self):
        s1 = 'John likes ice cream a lot.'
        q1 = 'Does John like ice cream a lot?'

        s2 = 'Jan runs in the park every week.'
        q2 = 'Does Jan run in the park every week?'

        s3 = 'Jack likes the grocery store.'
        q3 = 'Does Jack like the grocery store?'

        self.assertEqual(q1, bin_q(s1))
        self.assertEqual(q2, bin_q(s2))
        self.assertEqual(q3, bin_q(s3))

    def testComplexCases(self):
        s1 = 'John goes shopping every month.'
        q1 = 'Does John go shopping every month?'

        s2 = 'Jan always carries her purse with her.'
        q2 = 'Does Jan always carry her purse with her?'

        self.assertEqual(q1, bin_q(s1))
        self.assertEqual(q2, bin_q(s2))

class TestThirdPersonPlural (unittest.TestCase):

    def testSimpleCases(self):
        s1 = 'They like ice cream a lot.'
        q1 = 'Do they like ice cream a lot?'

        s2 = 'They runs in the park every week.'
        q2 = 'Do they run in the park every week?'

        s3 = 'They like the grocery store.'
        q3 = 'Do they like the grocery store?'

        self.assertEqual(q1, bin_q(s1))
        self.assertEqual(q2, bin_q(s2))
        self.assertEqual(q3, bin_q(s3))

    def testComplexCases(self):
        s1 = 'They go shopping every month.'
        q1 = 'Do they go shopping every month?'

        s2 = 'They always carry their purses with them.'
        q2 = 'Do they always carry their purses with them?'

        s3 = 'Alice and Bob love going to parties.'
        q3 = 'Do Alice and Bob love going to parties?'

        s4 = 'Well, Alice and Bob really hate brussel sprouts.'
        q4 = 'Do Alice and Bob really hate brussel sprouts?'

        self.assertEqual(q1, bin_q(s1))
        self.assertEqual(q2, bin_q(s2))
        self.assertEqual(q3, bin_q(s3))
        self.assertEqual(q4, bin_q(s4))

if __name__ == '__main__':
    unittest.main()