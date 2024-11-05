def example(test_objects=None):
    try:
        import pickle as pickle
    except:
        import mpickle as pickle

    if test_objects is None:
        # some built in type instances
        test_objects = [
            'foo', 
            12, 
            1.2, 
            1+2j,
            True,
            bytes(1),
            bytearray('foo', 'utf-8'),
            [1, 2, 3],
            (1, 2, 3),
            {1, 2, 'foo', 'bar'},
            {'foo': 'bar'},
            None, 
            NotImplemented,
            Ellipsis,
        ]
    
    for obj in test_objects:
        dump = pickle.dumps(obj)
        print(f'object of {type(obj)}: {obj} encodes to: {dump}')