from .celery import celery
import pymysql

pymysql.install_as_MySQLdb()