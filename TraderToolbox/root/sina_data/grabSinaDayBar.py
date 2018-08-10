#coding=utf-8
'''
##Chinese Stock API Data Grabber#
##@ycooi ooiyungchaw@hotmail.com#
##@version 1.0#
#https://github.com/ycooi/ChineseStockTicker/blob/master/test.conf

'''


import urllib, re
import urllib.request
import MySQLdb
import time
import threading
import configparser

class myDatabase():
    def __init__(self,tbname):
        self.user = 'root'
        self.passwd = 'P4ssword'
        self.dbname = 'bardata'
        self.tbname = tbname
        
        self.db = None
        self.connect()
        
    def connect(self):
        self.db = MySQLdb.connect(host='localhost', 
                             user=self.user, 
                             passwd=self.passwd,
                             db=self.dbname,
                             charset='utf8',
                             autocommit=True)
    
    def close(self):
        self.db.close()
    
    def create_table(self):
        cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        
        # check if the table exists
        sql = """SELECT count(*) FROM information_schema.tables 
                WHERE table_schema = 'stocktest' AND table_name = '{}'""".format(self.tbname)
        cursor.execute(sql)
        tables = cursor.fetchone()

        # create the table if not exists
        if tables.get('count(*)') == 0:
            print('create new  table')
            
            sql = """CREATE TABLE `{}` (
                    stock_code        CHAR(10) NOT NULL,
                    stock_name        CHAR(20) NOT NULL,
                    open_today        FLOAT,
                    close_yesterday   FLOAT,
                    price_now         FLOAT,
                    high_today        FLOAT,
                    low_today         FLOAT,
                    buy_one         FLOAT,
                    sell_one        FLOAT,
                    transaction_now   INT,
                    transvalue_now    FLOAT,
                    buy_one_qty       INT,
                    buy_one_price     FLOAT,
                    buy_two_qty       INT,    
                    buy_two_price     FLOAT,
                    buy_three_qty     INT,
                    buy_three_price   FLOAT,
                    buy_four_qty      INT,
                    buy_four_price    FLOAT,
                    buy_five_qty      INT,
                    buy_five_price    FLOAT,
                    sell_one_qty      INT,
                    sell_one_price    FLOAT,
                    sell_two_qty      INT, 
                    sell_two_price    FLOAT,
                    sell_three_qty    INT,
                    sell_three_price  FLOAT, 
                    sell_four_qty     INT,
                    sell_four_price   FLOAT,
                    sell_five_qty     INT,
                    sell_five_price   FLOAT,
                    quote_date        CHAR(20),
                    quote_time        CHAR(10)
                    )""".format(self.tbname) 
            cursor.execute(sql)
    
    def insert_data(self, data_list):
        cursor = self.db.cursor()         
        sql = """INSERT INTO `{}` (
                    stock_code, stock_name,
                    open_today, close_yesterday,
                    price_now,  high_today, low_today,
                    buy_one, sell_one,
                    transaction_now, transvalue_now,
                    buy_one_qty, buy_one_price,
                    buy_two_qty, buy_two_price,
                    buy_three_qty, buy_three_price,
                    buy_four_qty,  buy_four_price,
                    buy_five_qty, buy_five_price,
                    sell_one_qty, sell_one_price,
                    sell_two_qty, sell_two_price,
                    sell_three_qty, sell_three_price, 
                    sell_four_qty,  sell_four_price,
                    sell_five_qty,  sell_five_price,
                    quote_date, quote_time
            ) VALUES (%s,%s,
                    %s,%s,
                    %s,%s, %s,
                    %s,%s,
                    %s,%s,
                    %s,%s,
                    %s,%s,
                    %s,%s,
                    %s,%s,
                    %s,%s,
                    %s,%s,
                    %s,%s,
                    %s,%s, 
                    %s,%s,
                    %s,%s,
                    %s, %s)""".format(self.tbname)
        cursor.executemany(sql, data_list)
        

def get_data_from_url(stock_list):
    data_buf = []
    url = "http://hq.sinajs.cn/list="+','.join(stock_list)

    wp = urllib.request.urlopen(url).read().decode('gbk')       # open the urls
    #line = wp.readlines()
    lines = wp.splitlines(True)
    for  line in lines:
        #print(line)
        # get the stock code from the string
        stock_code = line[:line.index('=')]
        stock_code = stock_code[stock_code.rindex('_')+1:]
        # remove "" from the string
        data = re.sub('"','',line[line.index('=')+1:])
        # split the string
        data = data.split(',')
        # convert the stock name
        #data[0] = data[0].decode('gbk').encode('utf-8')
        # process the data, convert string to number
        if len(data)>32:        # >32 means it has the full infomation
            for i in range(1,30):
                val = data[i]
                if type(eval(val)) == int:
                    data[i] = int(val)
                elif type(eval(val)) == float:
                    data[i] = float(val)
            # insert the stock code into the begin of the array
            data.insert(0, stock_code)
            data_buf.append(tuple(data[:33]))


    
    return data_buf



def wait_to_start(tHour, tMinute):
    localtime = time.localtime()
    now_hour  = time.strftime("%H", localtime)
    now_minute = time.strftime("%M", localtime)
    print('current time: ', time.strftime("%H:%M:%S", localtime))
    
    if(now_hour>tHour) or \
        ((now_hour==tHour) and (now_minute>=tMinute)):
        return True
    else:
        return False

def process_data(tHour, tMinute, dbTable):
    localtime = time.localtime()
    now_hour  = time.strftime("%H", localtime)
    now_minute = time.strftime("%M", localtime)
    print('current time: ', time.strftime("%H:%M:%S", localtime))
    
    #stock_list = ('sh601006','sh601001', 'sh601002', 'sh601003', 'sh601005')
    global STOCK_LIST
    stock_list = STOCK_LIST
    data_list = get_data_from_url(stock_list)
    
    mydb = myDatabase(dbTable)
    mydb.insert_data(data_list)
    mydb.close()
    
    if (now_hour>tHour) or \
        ((now_hour==tHour) and (now_minute>=tMinute)):
        return True
    else:
        return False

def setup_database():
    localtime = time.localtime()
    table_name = time.strftime("%Y%m%d%H%M",localtime)
    
    mydb = myDatabase(table_name)
    mydb.create_table()
    mydb.close()
    return table_name    


DB_TABLE_NAME = None
STATE = 'processing_am'

AM_START_H = '9'
AM_START_M = '30'
AM_END_H = '11'
AM_END_M = '30'

PM_START_H = '13'
PM_START_M = '00'
PM_END_H = '20'
PM_END_M = '00'

STOCK_LIST = None

def main_loop():
    timer =  threading.Timer(5, main_loop)
    
    global STATE
    global DB_TABLE_NAME
    global AM_START_H, AM_START_M, AM_END_H, AM_END_M
    global PM_START_H, PM_START_M, PM_END_H, PM_END_M
    
    if STATE == 'wait_to_start_am':
        timer.start()
        startHour = AM_START_H        # target time hour
        startMinute = AM_START_M      # target time min

        print('wait to start AM:')
        ready = wait_to_start(startHour, startMinute)
        if ready:
            DB_TABLE_NAME = setup_database()
            STATE = 'processing_am'
    
    elif STATE == 'processing_am':
        timer.start()
        endHour = AM_END_H
        endMinute = AM_END_M
        print('processing_am')
        done = process_data(endHour, endMinute, DB_TABLE_NAME)
        if done:
            STATE = 'wait_to_start_pm'
        
    elif STATE == 'wait_to_start_pm':
        timer.start()
        startHour = PM_START_H       # target time hour
        startMinute = PM_START_M      # target time min

        print('wait to start PM:')
        ready = wait_to_start(startHour, startMinute)
        if ready:
            STATE = 'processing_pm'
            
    elif STATE == 'processing_pm':
        timer.start()
        endHour = PM_END_H
        endMinute = PM_END_M
        print('processing_pm')
        done = process_data(endHour, endMinute, DB_TABLE_NAME)
        if done:
            STATE = 'finish'
    else:
        print('process done for today')
         


if __name__ == '__main__':   
    cf = configparser.ConfigParser()
    cf.read("config.conf")

    AM_START_H = cf.get('am','start_hour')
    AM_START_M = cf.get('am','start_minute')
    AM_END_H = cf.get('am','end_hour')
    AM_END_M = cf.get('am','end_minute')

    PM_START_H = cf.get('pm','start_hour')
    PM_START_M = cf.get('pm','start_minute')
    PM_END_H = cf.get('pm','end_hour')
    PM_END_M = cf.get('pm','end_minute')
    
    stock_list = cf.get('stock', 'stocks')
    STOCK_LIST = tuple(stock_list.split(","))
    
    print("AM: start from {}:{} to {}:{}".format(AM_START_H, AM_START_M, AM_END_H, AM_END_M))
    print("PM: start from {}:{} to {}:{}".format(PM_START_H, PM_START_M, PM_END_H, PM_END_M))
    print("STOCKS : {}".format(stock_list))
    
    main_loop()