from clickhouse_driver import Client
from make_table import make_table
from read_file import format_data

make_table('10.40.0.11')

data = format_data('event-data.json')

query = "INSERT INTO user.sessions FORMAT TabSeparated\n" + data


try:
    client = Client('10.40.0.11')
    result = client.execute(query)
    print(result)
except Client as e:
    print(e)
except Exception as e:
    print(e)