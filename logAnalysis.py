#! /usr/bin/env python3

import psycopg2

# Constants and assets
DBNAME = "dbname=news"
query_1 = '''select articles.title, count(*) as views
from articles left join log
on log.path like '%' || articles.slug || '%'
where log.status = '200 OK'
group by articles.title
order by views desc
limit 3;'''
query_2 = '''select name, views from authors,
(select articles.author, count(*) as views
from articles left join log
on log.path like '%' || articles.slug || '%'
where log.status = '200 OK'
group by articles.author) as subq
where authors.id = subq.author
order by views desc;'''
query_3 = '''select day, percentage
from err_rate_tbl where percentage > 1.0
order by day;'''


def execute_query(cursor, query):
    """ Returns data fetched from database

    Attributes:
        cursor (cursor):        Cursor object
        query (str):            SQL query
    """
    cursor.execute(query)
    return cursor.fetchall()


def print_data(data, indicator):
    """ Prints data to command line

    Attributes:
        data (list):            Data retrieved from database
        indicator (str):        E.g. views or errors
    """
    for item in data:
        print("\t" + str(item[0]) + " --> " + str(item[1]) + indicator)


# Preparing user
print("Processing, please wait...")

# Creating connection to DB and cursor
conn = psycopg2.connect(DBNAME)
cur = conn.cursor()

# Fetch data from DB for the most popular articles
data1 = execute_query(cur, query_1)


# Fetch data from DB for the most popular authors
data2 = execute_query(cur, query_2)


# Fetch data from DB for error rates more than 1%
data3 = execute_query(cur, query_3)

# Closing DB connection and cursor
cur.close()
conn.close()

# Printing UI results
print("\nWhat are the most popular three articles of all time? \n")
print_data(data1, " views")

print("\nWho are the most popular article authors of all time? \n")
print_data(data2, " views")

print("\nOn which days did more than 1% of requests lead to errors? \n")
print_data(data3, "% errors")
