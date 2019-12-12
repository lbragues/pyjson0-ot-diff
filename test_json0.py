# coding=UTF-8

import unittest
from json0 import TypeJSON

class JSON0Tests(unittest.TestCase):
    def test_applyNumberAdd(self):
        self.assertEqual(
            TypeJSON.apply(
                1, [{'p':[], 'na':2}]
            ),
            3
        )
        self.assertEqual(
            TypeJSON.apply(
                [1], [{'p':[0], 'na':2}]
            ),
            [3]
        )
    
    def test_applyListInsert(self):
        self.assertEqual(
            TypeJSON.apply(
                ['b', 'c'], [{'p':[0], 'li':'a'}]
            ),
            ['a', 'b', 'c']
        )
        self.assertEqual(
            TypeJSON.apply(
                ['a', 'c'], [{'p':[1], 'li':'b'}]
            ),
            ['a', 'b', 'c']
        )
        self.assertEqual(
            TypeJSON.apply(
                ['a', 'b'], [{'p':[2], 'li':'c'}]
            ),
            ['a', 'b', 'c']
        )
    
    def test_applyListDelete(self):
        self.assertEqual(
            TypeJSON.apply(
                ['a', 'b', 'c'], [{'p':[0], 'ld':'a'}]
            ),
            ['b', 'c']
        )
        self.assertEqual(
            TypeJSON.apply(
                ['a', 'b', 'c'], [{'p':[1], 'ld':'b'}]
            ),
            ['a', 'c']
        )
        self.assertEqual(
            TypeJSON.apply(
                ['a', 'b', 'c'], [{'p':[2], 'ld':'c'}]
            ),
            ['a', 'b']
        )
    
    def test_applyReplace(self):
        self.assertEqual(
            TypeJSON.apply(
                ['a', 'x', 'b'], [{'p':[1], 'ld':'x', 'li': 'y'}]
            ),
            ['a', 'y', 'b']
        )

    def test_applyMove(self):
        self.assertEqual(
            TypeJSON.apply(
                ['b', 'a', 'c'], [{'p': [1], 'lm': 0}]
            ),
            ['a', 'b', 'c']
        )
        self.assertEqual(
            TypeJSON.apply(
                ['b', 'a', 'c'], [{'p': [0], 'lm': 1}]
            ),
            ['a', 'b', 'c']
        )
    
    def test_objectSanity(self):
        self.assertEqual(
            TypeJSON.apply(
                {'x': 'a'}, [{'p': ['y'], 'oi': 'b'}]
            ),
            {'x': 'a', 'y': 'b'}
        )
        self.assertEqual(
            TypeJSON.apply(
                {'x': 'a'}, [{'p': ['x'], 'od': 'a'}]
            ),
            {}
        )
        self.assertEqual(
            TypeJSON.apply(
                {'x': 'a'}, [{'p': ['x'], 'od': 'a', 'oi': 'b'}]
            ),
            {'x': 'b'}
        )

if __name__ == "__main__":
    unittest.main()