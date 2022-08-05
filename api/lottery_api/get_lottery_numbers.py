# Examples:
# ## Powerball by Month
# https://www.lottery.ok.gov/draw-games/past-draws?Month=02&Year=2022&GameId=16

# ## Megamillions by Month
# https://www.lottery.ok.gov/draw-games/past-draws?Month=05&Year=2022&GameId=17

import requests
import pandas as pd
import sqlite3
from datetime import datetime

def requestMonthlyLotteryInfo(month,year,gameid):
    return requests.get(f'https://www.lottery.ok.gov/draw-games/past-draws?Month={month}&Year={year}&GameId={gameid}')

# Data from requestMonthlyLotteryInfo call
def addLotteryInfoToDB(month, year, gameid):
    r = requestMonthlyLotteryInfo(month, year, gameid)
    df = pd.DataFrame.from_dict(r.json(), orient='columns')
    df['DrawDate'] = df['DrawDate'].str.replace("/Date(","",regex=False)
    df['DrawDate'] = df['DrawDate'].str.replace(")/","",regex=False)     
    df['DrawDate'] = pd.to_datetime(df['DrawDate'], unit='ms')   
    dbhelper('open')
    df.to_sql('lottery_info_temp',       # Name of the sql table
            conn,                   # sqlite.Connection or sqlalchemy.engine.Engine
            if_exists='replace',     # If the table already exists, {‘fail’, ‘replace’, ‘append’}, default ‘fail’
            index=False)
    conn.execute(
        '''
        INSERT INTO lottery_info
        SELECT * FROM lottery_info_temp
        WHERE id NOT IN (SELECT id FROM lottery_info)
        '''
    )
    dbhelper('commitclose')

# Period can be current or all - current is default 
def getLotteryInfoByPeriod(period = "current"):
    startingMonth = 1
    startingYear = 2019
    startingGameID = 16
    maxGameID = 17
    currentMonth = int(datetime.now().strftime('%m'))
    currentYear = int(datetime.now().strftime('%Y'))
    gameid = startingGameID
    if(period == "all"):
        while(gameid <= maxGameID):
            month = startingMonth
            year = startingYear
            if currentYear > year:
                targetMonth = 12
            else:
                targetMonth = currentMonth
            while(month <= targetMonth and year <= currentYear):
                addLotteryInfoToDB(month, year, gameid)
                if month == 12:
                    month = 0
                    year+=1
                    if currentYear > year:
                        targetMonth = 12
                    else:
                        targetMonth = currentMonth
                month+=1
            gameid+=1
    else: 
        while(gameid <= maxGameID):
            addLotteryInfoToDB(currentMonth, currentYear, gameid)
            gameid+=1
    return

def checkSQLiteTableExistsOrCreate(table_name, create_statement):
    dbhelper('open')
    try:
        # conn.execute("DROP TABLE IF EXISTS lottery_info;")
        # conn.commit()
        # print("dropping table")
        dfN_check = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        # print(dfN_check)
    except:
        # print("No such table: lottery_info")
        try:
            print(f"Creating a new table: {table_name}")
            conn.execute(create_statement)
            print("New table created successfully!!!")
        except Exception as e:
            print(e, " occured")
    
    dbhelper('commitclose')

def executeSQLStatement(statement):
    dbhelper('open')
    conn.execute(statement)
    dbhelper('commitclose')

def dbsetup():
    create_statement = '''
        CREATE TABLE "game_by_id" (
        "id"	INTEGER,
        "name"	TEXT,
        PRIMARY KEY("id")
        );
        '''
    checkSQLiteTableExistsOrCreate('game_by_id', create_statement)
    executeSQLStatement("INSERT OR IGNORE INTO game_by_id (id, name) VALUES (16, 'powerball')")
    executeSQLStatement("INSERT OR IGNORE INTO game_by_id (id, name) VALUES (17, 'megamillions')")
    create_statement = '''
        CREATE TABLE "lottery_info" (
         "Id"	INTEGER,
         "Game_Id"	INTEGER,
         "game"	TEXT,
         "ExternalId"	INTEGER,
         "DbNumber1"	INTEGER,
         "DbNumber2"	INTEGER,
         "DbNumber3"	INTEGER,
         "DbNumber4"	INTEGER,
         "DbNumber5"	INTEGER,
         "DbNumber6"	INTEGER,
         "DbNumber7"	INTEGER,
         "DrawDate"	TIMESTAMP,
         "Active"	INTEGER,
         "Winners"	TEXT,
         "CurGpAnnuity"	INTEGER,
         "CurGpCash"	INTEGER,
         "NextGpAnnuity"	INTEGER,
         "NextGpCash"	INTEGER,
         "Number1"	INTEGER,
         "Number2"	INTEGER,
         "Number3"	INTEGER,
         "Number4"	INTEGER,
         "Number5"	INTEGER,
         "Number6"	INTEGER,
         "Number7"	INTEGER,
         PRIMARY KEY("Id")
        ); 
        '''
    checkSQLiteTableExistsOrCreate('lottery_info', create_statement)

def dbhelper(action):
    global conn 
    if action == 'open':
        conn = sqlite3.connect('/mnt/c/Users/bamal/Desktop/lottery_info.db')
    if 'commit' in action:
        conn.commit()
    if 'close' in action:
        if(conn != None):
            conn.close()

def readFromDB(statement):
    dbhelper('open')
    df = pd.read_sql(statement, conn, parse_dates=["date_column"])
    dbhelper('commitclose')
    return df

def updateLotteryInfoDB():
    try:
        dbsetup()
        getLotteryInfoByPeriod()
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        dbhelper('close')