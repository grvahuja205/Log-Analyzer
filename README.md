# Log Analyzer
This project analyzes a database using SQL queries to produce 3 outputs,
* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors? 

The databse has data about the articles published the authors who published them and a web server logs showing the details of the articles visted on online, this database is having 3 tables,
* articles
* authors
* log
## Requirements
- Python needs to be installed, you may install python from [here](https://www.python.org/downloads/)
- Postgres SQL needs to be installed, you may install posstgres from [here](https://www.postgresql.org/download/) 
- Configure the database to use account 'postgres' using this [link](https://help.ubuntu.com/stable/serverguide/postgresql.html)

## Usage
* Clone the repository to a local directory on your system
* Run the following commnds to create database news having the 3 tables using command line,
    ```
    psql -U postgres -W (Will Prompt For Password)
    CREATE DATABASE news;
    ```
* Quit from database using, ```\q``` from same command line
* To create tables use the following commands, first download the file ```newsdata.sql``` from Udacity as given in the course,
    ```
    cd <path file newsdata.sql>
    psql -U postgres -d news -f newsdata.sql -W(prompt for password)
    psql -U postgres -d news -W(prompt for password)
    ```
* Now you are connected to 'news' database and have the 3 tables created, next step is to create the 3 views from which we are going to run the queries to have the output
    ```
    CREATE VIEW TopArticles AS SELECT articles.title, anv.num from ARTICLES, (select split_part(log.path, '/', 3) as slug_log, COUNT(*) as num from log GROUP BY slug_log HAVING length(split_part(log.path, '/', 3)) >1 ORDER BY num desc) as anv WHERE articles.slug=anv.slug_log;
    ```
    ```
    CREATE VIEW PopularAuthor AS SELECT SUM(nv.slug_log) as nviews, authors.name FROM authors, articles, (SELECT COUNT(split_part(log.path, '/', 3)) as slug_log, articles.title AS title FROM log, articles WHERE split_part(log.path, '/', 3) = articles.slug GROUP BY articles.title order by slug_log desc) AS nv WHERE articles.author = authors.id AND nv.title = articles.title GROUP BY authors.name ORDER BY nviews DESC;
    ```
    ```
    CREATE VIEW ErrorsPercent AS SELECT t.mdate AS ndate, t.ctotal AS total, er.failure AS fail FROM (SELECT date(time) as mdate, CAST(count(*) AS INTEGER) AS ctotal FROM log GROUP BY mdate ORDER BY mdate) AS t,(SELECT date(time) AS cdate, CAST(count(*) AS INTEGER) AS failure FROM log WHERE CAST(split_part(status, ' ', 1) AS INTEGER) >399 AND CAST(split_part(status, ' ', 1) AS INTEGER) < 600 GROUP BY cdate ORDER BY cdate) AS er WHERE t.mdate=er.cdate;
    ```
* Last step is to run the python file in the repository, open up the command prompt and run the follwing commands,
    ```
    cd <path to cloned repository>
    python log_analysis.py
    ```
* For sample output look at file ```output.txt```, the same will appear on the command line where you run the above python file.
## License
