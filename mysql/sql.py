# -*- coding: utf-8 -*-
import pymysql
from log.logger import log

db_item = pymysql.connect(host="localhost", user="root", password="jszxsyd0128",
                          db="jd_comment", port=3306, charset='utf8')

cur_item = db_item.cursor()

class Sql:
    @classmethod
    def insert_new_comment(x, comment_type, comment,create_time):
        statement = 'INSERT INTO jd_comment (comment_type,comment,create_time) ' \
                    'VALUES (\'%s\',\'%s\')' \
                    % (comment_type, comment,create_time)
        log.debug(statement)
        cur_item.execute(statement)
        db_item.commit()

    @classmethod
    def delete_comment(cls, comment_id):
        statement = 'DELETE FROM jd_comment WHERE id=\'%s\'' % comment_id
        log.debug(statement)
        cur_item.execute(statement)

    @classmethod
    def delete_all_comment(cls):
        statement = 'truncate table jd_comment'
        log.debug(statement)
        cur_item.execute(statement)


if __name__ == '__main__':
    sql = Sql()