import sqlite3 as sl
db = "dond.db"

conn = sl.connect(db)

curs = conn.cursor()

curs.execute('DROP TABLE IF EXISTS games')
curs.execute('DROP TABLE IF EXISTS rounds')
curs.execute('DROP TABLE IF EXISTS errors')

conn.execute("CREATE TABLE IF NOT EXISTS games ("
             "game_id INTEGER PRIMARY KEY,"
             "player_id INTEGER,"
             "game_mode INTEGER,"
             "end_result STRING,"
             "stop_round INTEGER,"
             "winnings FLOAT)")

conn.execute("INSERT INTO games (game_id, player_id, game_mode, end_result, stop_round, winnings)"
             "VALUES (11111, 10111, 0, 'TEST', 0, 0)")
conn.execute("INSERT INTO games (game_id, player_id, game_mode, end_result, stop_round, winnings)"
             "VALUES (11112, 10112, 0, 'TEST', 0, 0)")
conn.execute("INSERT INTO games (game_id, player_id, game_mode, end_result, stop_round, winnings)"
             "VALUES (11113, 10113, 0, 'TEST', 0, 0)")


conn.execute("CREATE TABLE IF NOT EXISTS rounds ("
             "game_id INTEGER,"
             "player_id INTEGER,"
             "game_mode INTEGER,"
             "round INTEGER,"
             "offer INTEGER,"
             "remaining_cases STRING)")

conn.execute("INSERT INTO rounds (game_id, player_id, game_mode, round, offer, remaining_cases)"
             "VALUES (11111, 97283, 0, 0, 97, '[1,10,20]')")


conn.execute("CREATE TABLE IF NOT EXISTS errors ("
             "game_id INTEGER,"
             "player_id INTEGER,"
             "round INTEGER,"
             "error_descr STRING)")

conn.execute("INSERT INTO errors (game_id, player_id, round, error_descr)"
             "VALUES (11111, 11111, 0, 'chose case #m not numeric')")


ex_game_id = 34523
ex_player_id = 10000
ex_round = 4
ex_error_descr = "chose neither 1 or 0 for DOND"


stmt = "INSERT INTO errors (game_id, player_id, round, error_descr) VALUES (" + str(ex_game_id) +", " + \
                    str(ex_player_id) + ", " + \
                    str(ex_round) + ", '" + \
                    str(ex_error_descr) + "')"

print(stmt)

# curs = conn.execute(stmt)



curs = conn.execute("SELECT * FROM games")
print(curs.fetchall())
curs = conn.execute("SELECT * FROM rounds")
print(curs.fetchall())
curs = conn.execute("SELECT * FROM errors")
print(curs.fetchall())

curs = conn.execute("SELECT game_id, player_id FROM games")
cols = curs.fetchall()
game_ids = [cols[i][0] for i in range(len(cols))]
player_ids = [cols[i][1] for i in range(len(cols))]
id_list = game_ids + player_ids
print(id_list)



conn.commit()
conn.close()