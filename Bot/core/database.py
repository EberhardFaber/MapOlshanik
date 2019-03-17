import MySQLdb
import config
from core.static import queriesDB


def register_user(user):
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql = queriesDB.get_insert_user(user)
    try:
        cursor.execute(sql)
        session.commit()
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        session.rollback()
    finally:
        session.close()


def register_team(user_id, team_name):
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql_insert_team = queriesDB.get_insert_team(team_name)
    sql_update_user = queriesDB.update_users_team(user_id, team_name)
    # Making new team
    try:
        cursor.execute(sql_insert_team)
        session.commit()
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        session.rollback()
    else:
        # Binding team to user
        try:
            cursor.execute(sql_update_user)
            session.commit()
        except MySQLdb.Error as e:
            print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            session.rollback()
    finally:
        session.close()


def inputPSW_team(user_id, team_psw):
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql_update_team = queriesDB.update_teams_psw(user_id, team_psw)
    # Binding password to team
    try:
        cursor.execute(sql_update_team)
        session.commit()
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        session.rollback()
    finally:
        session.close()


def input_point(user_id, point):
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql = queriesDB.insert_coordinates(point, user_id)
    try:
        cursor.execute(sql)
        session.commit()
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        session.rollback()
    finally:
        session.close()


def input_height(user_id, height):
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql = queriesDB.update_coordinates(height, user_id)
    print(sql)
    try:
        cursor.execute(sql)
        session.commit()
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        session.rollback()
    finally:
        session.close()


def take_teams():
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql = queriesDB.select_teams()
    list_teams = []
    try:
        cursor.execute(sql)
        tuple_teams = cursor.fetchall()
        for a in tuple_teams:
            list_teams.append(a[0])
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
    finally:
        session.close()
        return list_teams


def choose_team(user_id, team_name):
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql = queriesDB.update_users_team(user_id, team_name)
    print(sql)
    # Binding team to user
    try:
        cursor.execute(sql)
        session.commit()
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        session.rollback()
    finally:
        session.close()

def login_team(user_id, team_psw):
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql = queriesDB.select_team_psw(user_id)
    flag_res = False
    # Call team password
    print(sql)
    try:
        cursor.execute(sql)
        current_psw = cursor.fetchall()
        flag_res = current_psw[0][0] == team_psw
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        session.rollback()
    finally:
        session.close()
        return flag_res


def clear_team_for_user(user_id):
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql = queriesDB.clear_id_team(user_id)
    # Call team password
    print(sql)
    try:
        cursor.execute(sql)
        session.commit()
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        session.rollback()
    finally:
        session.close()


def get_all_point():
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql = queriesDB.select_all_point()
    res = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for a in range(0, len(result)):
            res.append([str(result[a][0]), str(result[a][1]), str(result[a][2])])
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        session.rollback()
    finally:
        session.close()
        return res

def coordinates_verify(user_id):
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql = queriesDB.coordinates_verify(user_id)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except MySQLdb.Error:
        session.rollback()

def show_points(user_id):
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql = queriesDB.select_points(user_id)
    list_coords = []
    try:
        cursor.execute(sql)
        tuple_coords = cursor.fetchall()
        for a in tuple_coords:
            list_coords.append([a[0], a[1], a[2], a[3]])
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
    finally:
        session.close()
        return list_coords

def check_register(user_id):
    session = MySQLdb.connect(
        user=config.DB_USER,
        host=config.DB_HOST,
        passwd=config.DB_PSW,
        db=config.DB_NAME,
        use_unicode=True,
        charset="utf8"
    )
    cursor = session.cursor()
    sql = queriesDB.select_register(user_id)
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        result = (res[0][0])
    finally:
        session.close()
        return result