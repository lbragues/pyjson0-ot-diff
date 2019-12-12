import json
import copy

try:
    import ujson
    PARSER = ujson
except:
    PARSER = json

def patches_to_ops(path, old, new, dmp_class, instance):
    ops = []
    patches = instance.patch_make(old, new);
    for patch in patches:
        offset = patch.start1
        for (type, value) in patch.diffs:
            if type == dmp_class.DIFF_DELETE :
                ops.append({ 'sd': value, 'p': copy.copy(path) + [offset]})
            elif type == dmp_class.DIFF_INSERT:
                ops.append({ 'si': value, 'p': copy.copy(path) + [offset]})
                offset += len(value)
            elif type == dmp_class.DIFF_EQUAL:
                offset += len(value)
    return ops

def optimization(ops, json_parser=PARSER):
    for index in range(len(ops) - 1):
        a = ops[index]
        b = ops[index + 1]

        # The op paths must be equal.
        if json_parser.dumps(a['p'][:-1]) != json_parser.dumps(b['p'][:-1]):
            continue

        if not isinstance(a['p'][-1], int) or not isinstance(b['p'][-1], int):
            continue

        # The indices must be successive
        if a['p'][-1] + 1 != b['p'][-1]:
            continue
        
        if 'li' in a and 'ld' in b and (json_parser.dumps(a['li']) == json_parser.dumps(b['ld'])):
            del a['li']
            del b['ld']
        elif 'li' in b and 'ld' in a and (json_parser.dumps(b['li']) == json_parser.dumps(a['ld'])):
            del b['li']
            del a['ld']

    new_ops = []
    for op in ops:
        if len(op) > 1:
            new_ops.append(op)
    return new_ops


def diff(input, output, path=[], diff_match_patch=None, optimize=True, json_parser=PARSER):

    primitives = [str, int, float, bool]
    queue = [(input, output, path, None)]
    ops = []
    dmp_instance = None

    while queue:
        session_ops = []
        input, output, path, group = queue.pop(0)

        # nodes are equal
        if json_parser.dumps(input) == json_parser.dumps(output):
            continue # Skip no ops for nodes that are equal
        
        is_object = isinstance(path[-1], str) if path else False

        # we need to delete the current data
        if output is None:
            op = {'p': copy.copy(path)}
            op['od' if is_object else 'ld'] = input
            session_ops.append(op)

        # we need to add the output data
        elif input is None:
            op = {'p': copy.copy(path)}
            op['oi' if is_object else 'li'] = output
            session_ops.append(op)

        elif diff_match_patch and isinstance(input, str) and isinstance(output, str):
            if dmp_instance is None:
                dmp_instance = diff_match_patch();

            session_ops = patches_to_ops(path, input, output, diff_match_patch, dmp_instance);

        elif type(output) in primitives or type(input) in primitives:
            op = {'p': copy.copy(path)}
            op['od' if is_object else 'ld'] = input
            op['oi' if is_object else 'li'] = output
            session_ops.append(op)

        elif type(output) is list:
            length = max(len(output), len(input))
            offset = 0
            new_group = []
            for index in range(length):
                new_path = copy.copy(path)
                new_path.append(index + offset)
                new_group.append([
                    input[index] if len(input) > index else None, 
                    output[index] if len(output) > index else None, 
                    new_path, 
                    new_group
                ])
                queue.insert(index, new_group[-1])
        else: # must be dicts
            keys = set(input.keys() if input else [])
            keys.update(output.keys() if output else [])
            for key in keys:
                new_path = copy.copy(path)
                new_path.append(key)
                # queue.append(
                #     [input.get(key, None), output.get(key, None), new_path, None]
                # )
                queue.insert(0, [input.get(key, None), output.get(key, None), new_path, None])
        
        if group:
            # pop the first element as it is this call
            group.pop(0)
            
            # fix the rest of the nodes if needed based on the session ops
            if len(group) > 0:
                call_input, call_output, call_path, call_group = group[0]
                str_path = json_parser.dumps(call_path[:-1])
                for op in session_ops:
                    if str_path == json_parser.dumps(op['p'][:-1]):
                        if 'ld' in op and 'li' not in op:
                            for call in group:
                                call[2][-1] -= 1 # fis the offset in every path

        ops.extend(session_ops)

    if optimize is True:
        return optimization(ops, json_parser)
    else:
        return ops