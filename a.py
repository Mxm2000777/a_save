from re_selfdb import SQLITE
import json
from datetime import datetime
db = SQLITE('a_save/db_asave.sqlite3')
"""      
что надо сделать:
новости
"""
idorder = '2023-10-13T11:50:24.410166' # sasha reselfdb > поменятб
username = "MetraMax"
db.create("username")
# {idnews: [author, zag, desk, created_time, viewscount] 
# admin + chat_id = {admin: admincreated_at: date, avatar: image, users: [users], messages: [[datetime, msg, author, changed], [datetime, msg, author,changed]]}