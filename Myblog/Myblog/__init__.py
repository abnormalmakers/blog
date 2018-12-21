import pymysql
import ssl

pymysql.install_as_MySQLdb()
ssl._create_default_https_context = ssl._create_unverified_context
