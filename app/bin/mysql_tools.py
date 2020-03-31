# Class to handle database connections

import mysql.connector


class Database():
    # dictionary containing all the queries 
    __queries = {
        'all_users':'SELECT * FROM users',
        'user_by_id':'SELECT * FROM users WHERE id=%s',
        'user_by_password':'SELECT * FROM users WHERE users.password = %s',
        'user_by_username':'SELECT * FROM users WHERE users.username = %s',
        'all_profiles':'SELECT * FROM profiles ORDER BY profiles.userid',
        'insert_page':'INSERT INTO pages (pageid, title, image, link, summary, category) VALUES (%s, %s, %s, %s, %s, %s)',
        'insert_recommendation':'INSERT INTO recommendations (userid, pageid) VALUES (%s, %s)',
        'search_recommendation':'SELECT * FROM recommendations WHERE recommendations.userid=%s AND recommendations.pageid=%s',
        'search_page':'SELECT * FROM pages WHERE pages.pageid=%s',
        'update_page':'UPDATE pages SET title=%s, image=%s, link=%s, summary=%s, category=%s WHERE pageid=%s',
        'sp_page_number_check':'CALL sp_page_number_check()',
        'sp_page':'CALL sp_page()'
    }

    def __init__(self):
        self.__db_con = mysql.connector.connect(
                            host = 'localhost', # change this to change mysql server's host
                            user = 'wnow', # change this to change mysql server's account (user)
                            passwd = '2020', # change this to change mysql server's account password
                            database = 'wnow', # change this to change target database
                            charset = "utf8mb4",
                        )
        self.__db_con.autocommit = False # autocommit disabled
        self.__cursor = self.__db_con.cursor()

    def __del__(self):
        self.__cursor.close()
        self.__db_con.close()

    # This method is required in order to make changes persistent 
    def commit(self):
        self.__db_con.commit()

    # This method returns all the users in the table users
    # It returns a tuple
    def get_users(self):
        self.__cursor.execute(self.__queries['all_users'])
        return self.__cursor.fetchall()

    # This method returns the user in the table users specified either by id (default), password or username
    # It returns a tuple
    def get_user(self, by='id', where=''):
        if by == 'id':
            self.__cursor.execute(self.__queries['user_by_id'], (where,))
            return self.__cursor.fetchone()
        elif by == 'password':
            self.__cursor.execute(self.__queries['user_by_password'], (where,))
            return self.__cursor.fetchone()
        else:
            self.__cursor.execute(self.__queries['user_by_username'], (where,))
            return self.__cursor.fetchone()

    # This method returns all the user profiles in the table profiles
    # It returns a tuple
    def get_profiles(self):
        self.__cursor.execute(self.__queries['all_profiles'])
        return self.__cursor.fetchall()

    # Attribute page is dictionary-like (for example, pandas.DataFrame)
    # Attribute category is of type str
    def insert_page(self, page, category):
        self.__cursor.execute(self.__queries['search_page'], (page['pageid'],)) # search if the page provided exists
        if not self.__cursor.fetchone(): # if page does not exist, perform an INSERT query
            values = (
                page['pageid'],
                page['title'],
                page['image'],
                page['link'],
                page['summary'],
                category
            )
            self.__cursor.execute(self.__queries['insert_page'], values)
        else: # if page already exists into table pages, perform an UPDATE query
            values = (
                page['title'],
                page['image'],
                page['link'],
                page['summary'],
                category,
                page['pageid']
            )
            self.__cursor.execute(self.__queries['update_page'], values)

    def insert_recommendations(self, userid, pageid):
        values = (
            userid,
            pageid
        )
        self.__cursor.execute(self.__queries['search_recommendation'], values)
        if not self.__cursor.fetchone():
            self.__cursor.execute(self.__queries['insert_recommendation'], values)

    # This method excecutes the query associated to statemnt in __queries dictionary
    def execute(self, statement):
        self.__cursor.execute(self.__queries[statement])
        self.__db_con.commit()
