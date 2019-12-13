# coding=UTF-8

import unittest
from pyson0 import diff
from diff_match_patch import diff_match_patch

class Pyson0diffTests(unittest.TestCase):
    def test_listInsert(self):
        self.assertEqual(
            diff([], ['one'], optimize=False),
            [{'p': [0], 'li': 'one'}]
        )
        self.assertEqual(
            diff([], [1], optimize=False),
            [{'p': [0], 'li': 1}]
        )
        self.assertEqual(
            diff([], [False], optimize=False),
            [{'p': [0], 'li': False}]
        )
        self.assertEqual(
            diff(['one'], ['one', 'two'], optimize=False),
            [{'p': [1], 'li': 'two'}]
        )
        self.assertEqual(
            diff([1], [1, 2], optimize=False),
            [{'p': [1], 'li': 2}]
        )
        self.assertEqual(
            diff([False], [False, True], optimize=False),
            [{'p': [1], 'li': True}]
        )
        self.assertEqual(
            diff([0.1], [0.1, 0.2], optimize=False),
            [{'p': [1], 'li': 0.2}]
        )
    
    def test_listInsertOptimized(self):
        self.assertEqual(
            diff([], ['one']),
            [{'p': [0], 'li': 'one'}]
        )
        self.assertEqual(
            diff([], [1]),
            [{'p': [0], 'li': 1}]
        )
        self.assertEqual(
            diff([], [False]),
            [{'p': [0], 'li': False}]
        )
        self.assertEqual(
            diff(['one'], ['one', 'two']),
            [{'p': [1], 'li': 'two'}]
        )
        self.assertEqual(
            diff([1], [1, 2]),
            [{'p': [1], 'li': 2}]
        )
        self.assertEqual(
            diff([False], [False, True]),
            [{'p': [1], 'li': True}]
        )
        self.assertEqual(
            diff([0.1], [0.1, 0.2]),
            [{'p': [1], 'li': 0.2}]
        )
    
    def test_listReplace(self):
        self.assertEqual(
            diff(['one', 'two'], ['one', 'three', 'two'], optimize=False),
            [{'p': [1], 'ld': 'two', 'li': 'three'}, {'p': [2], 'li': 'two'}]
        )
        self.assertEqual(
            diff([1, 2], [1, 3, 2], optimize=False),
            [{'p': [1], 'ld': 2, 'li': 3}, {'p': [2], 'li': 2}]
        )
        self.assertEqual(
            diff([False, False], [False, True, False], optimize=False),
            [{'p': [1], 'ld': False, 'li': True}, {'p': [2], 'li': False}]
        )
        self.assertEqual(
            diff([0.1, 0.1], [0.1, 0.2, 0.1], optimize=False),
            [{'p': [1], 'ld': 0.1, 'li': 0.2}, {'p': [2], 'li': 0.1}]
        )

    def test_listReplaceOptimized(self):
        self.assertEqual(
            diff(['one', 'two'], ['one', 'three', 'two']),
            [{'p': [1], 'li': 'three'}]
        )
        self.assertEqual(
            diff([1, 2], [1, 3, 2]),
            [{'p': [1], 'li': 3}]
        )
        self.assertEqual(
            diff([False, False], [False, True, False]),
            [{'p': [1], 'li': True}]
        )
        self.assertEqual(
            diff([0.1, 0.1], [0.1, 0.2, 0.1]),
            [{'p': [1], 'li': 0.2}]
        )

    def test_objectInsert(self):
        self.assertEqual(
            diff({}, {'one': 'two'}, optimize=False),
            [{'p': ['one'], 'oi': 'two'}]
        )
        self.assertEqual(
            diff({}, {'one': 1}, optimize=False),
            [{'p': ['one'], 'oi': 1}]
        )
        self.assertEqual(
            diff({}, {'one': True}, optimize=False),
            [{'p': ['one'], 'oi': True}]
        )
        self.assertEqual(
            diff({}, {'one': 0.1}, optimize=False),
            [{'p': ['one'], 'oi': 0.1}]
        )
    
    def test_objectInsertOptimized(self):
        self.assertEqual(
            diff({}, {'one': 'two'}),
            [{'p': ['one'], 'oi': 'two'}]
        )
        self.assertEqual(
            diff({}, {'one': 1}),
            [{'p': ['one'], 'oi': 1}]
        )
        self.assertEqual(
            diff({}, {'one': True}),
            [{'p': ['one'], 'oi': True}]
        )
        self.assertEqual(
            diff({}, {'one': 0.1}),
            [{'p': ['one'], 'oi': 0.1}]
        )

    def test_objectReplace(self):
        self.assertEqual(
            diff({'one': 'one'}, {'one': 'two'}, optimize=False),
            [{'p': ['one'], 'oi': 'two', 'od': 'one'}]
        )
        self.assertEqual(
            diff({'one': 1}, {'one': 2}, optimize=False),
            [{'p': ['one'], 'oi': 2, 'od': 1}]
        )
        self.assertEqual(
            diff({'one': True}, {'one': False}, optimize=False),
            [{'p': ['one'], 'oi': False, 'od': True}]
        )
        self.assertEqual(
            diff({'one': 0.1}, {'one': 0.2}, optimize=False),
            [{'p': ['one'], 'oi': 0.2, 'od': 0.1}]
        )

    def test_objectReplaceOptimized(self):
        self.assertEqual(
            diff({'one': 'one'}, {'one': 'two'}),
            [{'p': ['one'], 'oi': 'two', 'od': 'one'}]
        )
        self.assertEqual(
            diff({'one': 1}, {'one': 2}),
            [{'p': ['one'], 'oi': 2, 'od': 1}]
        )
        self.assertEqual(
            diff({'one': True}, {'one': False}),
            [{'p': ['one'], 'oi': False, 'od': True}]
        )
        self.assertEqual(
            diff({'one': 0.1}, {'one': 0.2}),
            [{'p': ['one'], 'oi': 0.2, 'od': 0.1}]
        )
    
    def test_stringMutation(self):
        self.assertEqual(
            diff(
                {'one': 'one'}, 
                {'one': 'two'}, 
                diff_match_patch=diff_match_patch,
                optimize=False
            ),
            [{ 'sd': 'one', 'p': [ 'one', 0 ] }, { 'si': 'two', 'p': [ 'one', 0 ] }]
        )
        self.assertEqual(
            diff(
                {'one': '1234abcdef'}, 
                {'one': '1234xyz'}, 
                diff_match_patch=diff_match_patch,
                optimize=False
            ),
            [
                {'sd': 'abcdef', 'p':['one', 4]}, 
                {'si': 'xyz', 'p':['one', 4]}
            ]
        )
        self.assertEqual(
            diff(
                {'one': '1234'}, 
                {'one': '1234xyz'}, 
                diff_match_patch=diff_match_patch,
                optimize=False
            ),
            [
                {'si': 'xyz', 'p':['one', 4]}
            ]
        )
        self.assertEqual(
            diff(
                {'one': 'abcdef1234'}, 
                {'one': 'xyz1234'}, 
                diff_match_patch=diff_match_patch,
                optimize=False
            ),
            [
                {'sd': 'abcdef', 'p':['one', 0]}, 
                {'si': 'xyz', 'p':['one', 0]}
            ]
        )
        self.assertEqual(
            diff(
                {'one': '1234'}, 
                {'one': 'xyz1234'}, 
                diff_match_patch=diff_match_patch,
                optimize=False
            ),
            [
                {'si': 'xyz', 'p':['one', 0]}
            ]
        )
        self.assertEqual(
            diff(
                ['foo', 'The only change here is at the end.', 1, 2, 3], 
                ['foo', 'The only change here is at the very end.', 1, 2], 
                diff_match_patch=diff_match_patch,
                optimize=False
            ),
            [
                {'p': [1, 31], 'si': 'very '},
                {'p': [4], 'ld': 3}
            ]
        )

    def test_stringMutationOptimized(self):
        self.assertEqual(
            diff(
                {'one': 'one'}, 
                {'one': 'two'}, 
                diff_match_patch=diff_match_patch
            ),
            [{ 'sd': 'one', 'p': [ 'one', 0 ] }, { 'si': 'two', 'p': [ 'one', 0 ] }]
        )
        self.assertEqual(
            diff(
                {'one': '1234abcdef'}, 
                {'one': '1234xyz'}, 
                diff_match_patch=diff_match_patch
            ),
            [
                {'sd': 'abcdef', 'p':['one', 4]}, 
                {'si': 'xyz', 'p':['one', 4]}
            ]
        )
        self.assertEqual(
            diff(
                {'one': '1234'}, 
                {'one': '1234xyz'}, 
                diff_match_patch=diff_match_patch
            ),
            [
                {'si': 'xyz', 'p':['one', 4]}
            ]
        )
        self.assertEqual(
            diff(
                {'one': 'abcdef1234'}, 
                {'one': 'xyz1234'}, 
                diff_match_patch=diff_match_patch
            ),
            [
                {'sd': 'abcdef', 'p':['one', 0]}, 
                {'si': 'xyz', 'p':['one', 0]}
            ]
        )
        self.assertEqual(
            diff(
                {'one': '1234'}, 
                {'one': 'xyz1234'}, 
                diff_match_patch=diff_match_patch
            ),
            [
                {'si': 'xyz', 'p':['one', 0]}
            ]
        )
        self.assertEqual(
            diff(
                ['foo', 'The only change here is at the end.', 1, 2, 3], 
                ['foo', 'The only change here is at the very end.', 1, 2], 
                diff_match_patch=diff_match_patch
            ),
            [
                {'p': [1, 31], 'si': 'very '},
                {'p': [4], 'ld': 3}
            ]
        )

    def test_objectPropertyMutation(self):
        self.assertEqual(
            diff(
                {
                    'nodes': [{'content': 'string'}],
                },
                {
                    'nodes': [
                        {'content': 's'},
                        {'nodes': [{'content': 'trin'}]},
                        {'content': 'g'}
                    ],
                },
                optimize=False
            ),
            [
                {'od': 'string', 'oi': 's', 'p': ['nodes', 0, 'content']},
                {'li': {'nodes': [{'content': 'trin'}]}, 'p': ['nodes', 1]},
                {'li': {'content': 'g'}, 'p': ['nodes',2]}
            ]
        )

    def test_objectPropertyMutationOptimized(self):
        self.assertEqual(
            diff(
                {
                    'nodes': [{'content': 'string'}],
                },
                {
                    'nodes': [
                        {'content': 's'},
                        {'nodes': [{'content': 'trin'}]},
                        {'content': 'g'}
                    ],
                }
            ),
            [
                {'od': 'string', 'oi': 's', 'p': ['nodes', 0, 'content']},
                {'li': {'nodes': [{'content': 'trin'}]}, 'p': ['nodes', 1]},
                {'li': {'content': 'g'}, 'p': ['nodes',2]}
            ]
        )