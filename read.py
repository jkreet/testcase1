from clickhouse_driver import Client

query = "SELECT * FROM user.sessions"


try:
    client = Client('10.40.0.11')
    result = client.execute(query)
    print(result)
except Client as e:
    print(e)
except Exception as e:
    print(e)