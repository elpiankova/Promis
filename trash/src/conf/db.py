groups = {
    'remote': {
        'contributor' : {
            'host': '',
            'port': '',
            'user': '',
            'password': '',
            'driver': '',
            'db_name': ''
        },
        'root' : {
            'host': '',
            'port': '',
            'user': '',
            'password': '',
            'driver': '',
            'db_name': ''
        }
    },
    'local': {
        'contributor' : {
            'host': 'localhost',
            'port': '5432',
            'user': 'postgres',
            'password': 'xhtdj',
            'driver': 'postgresql',
            'db_name': 'promisdb'
        },
        'root' : {
            'host': 'localhost',
            'port': '5432',
            'user': 'postgres',
            'password': 'xhtdj',
            'driver': 'postgresql',
            'db_name': 'promisdb'
        }
    }
};

use = 'local';

def select(permissions, group=use):
    if (permissions in ['root', 'contributor']):
        return groups[group][permissions];
    else:
        raise 'DB CONF:: No such `%s` permissions category' % (permissions);
