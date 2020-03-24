from clickhouse_driver import Client

def make_table(server_ip):
    try:
        client = Client(server_ip)
        query = 'CREATE DATABASE IF NOT EXISTS user'
        client.execute(query)
        print('DB created')

        query = 'CREATE TABLE IF NOT EXISTS user.sessions \
        (\
            ts Int64,\
            userId String,\
            sessionId Int16,\
            page String,\
            auth String,\
            method String,\
            status Int16,\
            level String,\
            itemInSession Int16,\
            location String,\
            userAgent String,\
            lastName String,\
            firstName String,\
            registration Int64,\
            gender String,\
            artist String,\
            song String,\
            length Float32\
        )\
        ENGINE = MergeTree() \
        PARTITION BY ts \
        ORDER BY (ts, intHash32(sessionId)) \
        SAMPLE BY intHash32(sessionId)'
        client.execute(query)
        print('Table created')
    except Client as e:
        print(e)
    except Exception as e:
        print(e)