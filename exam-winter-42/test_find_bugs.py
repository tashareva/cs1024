import unittest 
from pyfakefs.fake_filesystem_unittest import TestCase


class bugsTestCase(TestCase):
    def test_find_bugs(self):
        tasks([A->B, B->C, C->B], [A->A, B->B], [A->A, B->C, C->A])
        self.assertEqual(task, correct_task) 
