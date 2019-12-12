import json
import copy

class TypeJSON:

    __types = {
        'json0': {'name': 'json0', 'uri': 'http://sharejs.org/types/JSONv0'}
    }

    @staticmethod
    def register(subtype):
        TypeJSON.__types[subtype['name']] = subtype

    @staticmethod
    def create(object):
        return copy.deepcopy(object)

    @staticmethod
    def invert_component(c):
        raise Exception('not implemented yet')

    @staticmethod
    def invert(op):
        raise Exception('not implemented yet')

    @staticmethod
    def is_valid(operations):
        for op in operations:
            if 'p' not in op:
                raise Exception('invalid operation: {}'.format(json.dumps(op)))

    @staticmethod
    def from_text(c):
        raise Exception('not implemented yet')

    @staticmethod
    def to_text(c):
        raise Exception('not implemented yet')

    @staticmethod
    def apply(snapshot, operations):
        TypeJSON.is_valid(operations)

        operations = copy.deepcopy(operations)
        container = {'data': snapshot}

        for op in operations:
            if 'si' in op or 'sd' in op:
                TypeJSON.from_text(op)

            parent = None
            parent_key = None
            elem = container
            key = 'data'

            # path navigation
            for crumb in op['p']:
                parent = elem
                parent_key = key
                if elem is None:
                    print(op, snapshot)
                    raise Exception('invalid path')
                elem = elem[key]
                key = crumb

            if 't' in op and 'o' in op and op['t'] in TypeJSON.__types:
                elem[key] = TypeJSON.__types[op['t']].apply(elem[key], op['o'])

            # number add
            elif 'na' in op:
                if type(elem[key]) not in [int, float]:
                    raise Exception('referenced element not a number')
                elem[key] += op['na']

            # list replace
            elif 'li' in op and 'ld' in op:
                if not isinstance(elem, list):
                    raise Exception('refereneced element not a list')
                elem[key] = op['li']

            # list insert
            elif 'li' in op:
                if not isinstance(elem, list):
                    raise Exception('refereneced element not a list')
                elem.insert(key, op['li'])

            # list delete
            elif 'ld' in op:
                if not isinstance(elem, list):
                    raise Exception('refereneced element not a list')
                try:
                    del elem[key]
                except IndexError:
                    pass

            # list move
            elif 'lm' in op:
                if not isinstance(elem, list):
                    raise Exception('refereneced element not a list')
                if op['lm'] != key:
                    to_move = elem[key]
                    del elem[key]
                    elem.insert(op['lm'], to_move)

            # object insert/replace
            elif 'oi' in op:
                elem[key] = op['oi']

            # object delete
            elif 'od' in op:
                elem.pop(key, None)

            else:
                raise Exception('invalid operation {}'.format(json.dumps(op)))
        return container['data']