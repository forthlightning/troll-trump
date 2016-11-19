from __future__ import absolute_import, print_function
import psycopg2
import datetime
import tweepy
import time

credentials = {"chinahoax": {
    "consumer_key":"qGukKFrGvJkbbvAdaoJovhW0d",
    "consumer_secret":"f3q1rdhDlr0dGAyxOmQosJWalkg0YwDNtn7QUQp0fqPxgBYmhv",
    "access_token":"2902869899-nGULNzeuoNQSmlE5fY7db2vEEUlmGIvjzYhkVXs",
    "access_token_secret":"2CTfaZrgWIw16YhhNJN34DQebjwamQlGyd0h3IwsK6dQZ"},
    "chinahoax1":{
    "consumer_key":"ektj3xDdIxcWsJzhKdG5n062N",
    "consumer_secret":"K4gbdPlSTfrQHRtGFGo4S8z5JXMUEWhawCS4zPElZFLwnPDtGy",
    "access_token":"800077289132130304-RFxDYnYCk1LNWkbOBTQ02vgVQoBNdDT",
    "access_token_secret":"vzWHx7ZvPxPeLOJe9DInqZPoFY42xRFpZyTYHqRaAt39K"}
}

def login_user(consumer_key,consumer_secret,access_token,access_token_secret):
    # page located at https://dev.twitter.com/apps (under "OAuth settings")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def update_status(api, new_status):
    api.update_status(status=new_status)
    
def create_postgres_table(db_name, table_name, col_type_tuples):
    '''
    :param db_name: name of the postgres database
    :param table_name: name of the postgres table
    :param col_type_tuples: list of tuples with desired names and types of columns
    :return:
    '''

    #connect to postgres database
    conn = psycopg2.connect(dbname=db_name, user="postgres")
    c = conn.cursor()

    #construct string that will be executed
    psql_string = "CREATE TABLE %s (" % (table_name)

    for col, type in col_type_tuples:
        psql_string+="%s %s, " % (col, type)

    psql_string = psql_string[:-2]+");"
    print(psql_string)

    #execute constructed string
    c.execute(psql_string)
    conn.commit()
    #cloase connection
    conn.close()
    
def update_single_obs(db_name, table_name, data_dict, meta=False):
    '''
    :param db_name: name of the postgres database
    :param table_name: name of the postgres table
    :param data_dict: dictionary with columns names as keys and data as values
    :return: n/a
    '''

    #connect to postgres database
    conn = psycopg2.connect(dbname=db_name, user="postgres")
    c = conn.cursor()

    #construct string that will be executed
    psql_string = "INSERT INTO %s (" % table_name
    psql_string += ", ".join(col for col in data_dict.keys()) + ') VALUES ('
    for val in data_dict.values():
        if type(val)==str:
            if "(" not in val:
                psql_string += "'%s'" % val + ', '
            else:
                psql_string += val + ', '
        else:
            psql_string += str(val) + ', '
    psql_string = psql_string[:-2]+");"
    c.execute(psql_string)

    conn.commit()
    #close connection
    conn.close()

    return None

def append_tweets_to_db(api, username, page_start):
    page = page_start
    deadend = False
    while not deadend:
        try:
            tweets = api.user_timeline(username, page = page)
        except:
            deadend = True
            return page
        
        if len(tweets)==0:
            deadend = True
        else:
            for tweet in tweets:
                tweet_text = tweet.text.encode("utf-8")
                try:
                    data_dict = create_data_dict(tweet)
                    update_single_obs("climate_tweets", "republican_tweets", data_dict)
                except:
                    print(tweet_text)    
        page+=1
    return page

def create_data_dict(tweet):
    data_dict = {
    "username": "'"+tweet._json['user']['screen_name']+"'",
   "date_created": tweet.created_at.strftime("%Y-%m-%d"),
    "favorite":tweet.favorite_count,
    "retweeted":tweet.retweet_count,
    "content":"'"+tweet._json['text'].replace(",","")+"'"}
    return data_dict



def run_scraper(api, username, page_start):
    page = 1
    run_scraper=True
    while run_scraper:
        print("Starting to Pull at page num: " + str(page))
        page = append_tweets_to_db(api, "myronebell", page_start=1)
        if page!=False:
            time.sleep(60*15)
            print("Sleeping!")
        else:
            run_scraper=False
    print("Finished Scraper.")
    return None

# create_postgres_table("climate_tweets", "republican_tweets", [('id', 'serial primary key'), ('username', 'text'),
#                                                      ('date_created', 'text'), ('favorite', 'int'), 
#                                                      ('retweeted','int'), ("content","text")])


chinahoax = credentials['chinahoax']
chinahoax1 = credentials['chinahoax1']

api = login_user(chinahoax['consumer_key'],chinahoax['consumer_secret'],chinahoax['access_token'],chinahoax['access_token_secret'])
api2 = login_user(chinahoax1['consumer_key'],chinahoax1['consumer_secret'],chinahoax1['access_token'],chinahoax1['access_token_secret'])



# end_page = append_tweets_to_db(api, "myronebell", page_start=1)
run_scraper(api, "RepMikePompeo", page_start=1)