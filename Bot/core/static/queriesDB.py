from datetime import datetime


def get_insert_user(user):
    values = [user.id, user.first_name, user.last_name, user.username]
    res = 'INSERT INTO Users (id, firstName, lastName, nickName) VALUES ({0[0]}, "{0[1]}", "{0[2]}", "{0[3]}")'\
        .format(values)
    return res


def get_insert_team(name):
    res = 'INSERT INTO Teams (title) VALUES ("{0}")'.format(name)
    return res


def update_users_team(user_id, name):
    res = 'UPDATE Users SET id_team = (SELECT id FROM Teams WHERE title LIKE "{0}") WHERE id LIKE {1}'\
        .format(name, user_id)
    return res


def update_teams_psw(user_id, psq):
    res = 'UPDATE Teams SET password = "{0}" WHERE id LIKE (SELECT id_team FROM Users WHERE id LIKE {1})'\
        .format(psq, user_id)
    return res


def insert_coordinates(point, user_id):
    res = 'INSERT INTO Coordinates (point, date, id_team) VALUES (PointFromText("POINT({0[0]} {0[1]})"), "{1}", ' \
          '(SELECT id_team FROM Users WHERE id LIKE {2}))'\
        .format(point, datetime.now(tz=None), user_id)
    return res

def update_coordinates(height, id_user):
    res = 'UPDATE Coordinates SET height = {0} WHERE id_team = (SELECT id_team FROM Users WHERE id LIKE {1}) AND date IN(SELECT MAX(date) FROM(SELECT * FROM Coordinates) AS Coord GROUP BY id_team)' .format(height, id_user)
    return res


def select_teams():
    return 'SELECT title FROM Teams'


def select_team_psw(id_user):
    res = 'SELECT password FROM Teams WHERE id LIKE (SELECT id_team FROM Users WHERE id LIKE {0})'.format(id_user)
    return res


def clear_id_team(id_user):
    return 'UPDATE Users SET id_team = NULL WHERE id LIKE {0}'.format(id_user)

def select_all_point():
    return 'SELECT X(`point`), Y(`point`), height FROM Coordinates'


def coordinates_verify(user_id):
    res = 'SELECT X(`point`), Y(`point`) FROM Coordinates WHERE id_team LIKE (SELECT id_team FROM Users WHERE id LIKE {0})'.format(user_id)
    return res

def select_points(user_id):
    res = 'SELECT X(`point`), Y(`point`), height, date FROM Coordinates WHERE id_team LIKE (SELECT id_team FROM Users WHERE id LIKE {0})'.format(user_id)
    return res

def select_register(user_id):
    res = 'SELECT id_team FROM Users WHERE id LIKE {0}'.format(user_id)
    return res
