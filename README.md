# Log Analysis Project 
>The project demonstrates my skills in databases and SQL specifically PostgreSQL, and Python DB-API.
The application runs three queries and displays the output in the command-line that answers below three questions
  * What are the most popular three articles of all time?
  * Who are the most popular article authors of all time?
  * On which days did more than 1% of requests lead to errors?

# Requirement
  * [Python3](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)

# Quickstart

## Preparing the project:
1. Install Vagrant and VirtualBox
2. Download the [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
3. Unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.
4. To build the reporting tool, you'll need to load the site's data into your local database.

## Setting up the database and creating views:
1. To load the data, `cd` into the `vagrant` directory and use the command 
```
psql -d news -f newsdata.sql.
```
2. Create view err_rate_tbl using"
```
create view err_rate_tbl as 
select errtbl.day, round((errtbl.errors * 1.0) / (requesttbl.requests * 1.0) * 100, 2) as percentage
from
(select time::date as day, count(*) as requests from log group by day) as requesttbl, 
(select time::date as day, count(*) as errors from log where status = '404 NOT FOUND' group by day) as errtbl
where
requesttbl.day = errtbl.day;
```

## Run

From vagrant folder inside the virtual machine, run below:
```$ python logAnalysis.py```
