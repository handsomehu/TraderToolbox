'''
Created on Dec 28, 2018

@author: I038825 Leon For automatic apply new stock
Reference is zhihu post
I will not use it since it need the client to run and not real auto trade.
Just create for reference
'''
import easytrader

user = easytrader.use('ht_client',debug=False)
user.prepare(user='518518518', password='123456',comm_password='123456')
res = user.auto_ipo()
print(res)
