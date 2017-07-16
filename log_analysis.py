#!/usr/bin/python
import psycopg2


def logAnalyzer():
    try:
        # Connecting to postgres database
        conn = psycopg2.connect("dbname='news' user='postgres'\
                                password='root'")
        cur = conn.cursor()
        # TopArticles is a view in database fetching the top articles
        # by articles visted
        cur.execute(r"SELECT * FROM TopArticles")
        rows = cur.fetchall()
        print "The top 3 articles are"
        i = 0
        while i < 3:  # For displaying the top 3 results
            print "%s--%d views" % (rows[i][0], float(rows[i][1]))
            i = i+1
        # PopularAuthor is a view in database dispalying the name of the author
        # having views in sorted order by total number of pages authored
        # by them in decreasing order
        cur.execute(r"SELECT * FROM PopularAuthor")
        print "\nThe most popular authors are:"
        nv_rows = cur.fetchall()
        for nv_row in nv_rows:
            print "%s--%d views" % (nv_row[1], float(nv_row[0]))
        # ErrorsPercent is a view in database
        # representing the total no of times the pages are visisted
        # and the total number of times the request resulted in failure code
        cur.execute("SELECT * FROM ErrorsPercent")
        print "\nThe date on which failure was mor than 1 Percent are"
        p_rows = cur.fetchall()
        for p_row in p_rows:
            if (float(p_row[2])/float(p_row[1])*100) > 1.0:
                per = float(p_row[2])/float(p_row[1])*100
                print "%s--%f" % (p_row[0], per)+"%"
    except Exception as e:
        raise e
    finally:
        conn.close()   # Closing The Database Connection

if __name__ == '__main__':
    logAnalyzer()
