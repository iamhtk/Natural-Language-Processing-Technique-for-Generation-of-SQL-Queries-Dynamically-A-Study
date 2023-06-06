from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import db_mgmt
import time
import datetime

def getQuery(word_list):
    sql=''
    word_set = set(word_list)
    print(word_set)
    if 'get' in word_set or 'select' in word_set or 'retrieve' in word_set or 'fetch' in word_set or 'show' in word_set:
        sql = 'select %1% from cities %2%'
        where = ''
        statelist = ''
        if 'capital' in word_set or 'capitals' in word_set:
            where =  "WHERE iscapital='1'"
        if 'Madhya Pradesh' in word_set or  'Madhya' in word_set:
            statelist = "'Madhya Pradesh'"
        if 'Delhi' in word_set:
            if statelist != '':
                statelist = statelist +", 'Delhi'"
            else:
                statelist = "'Delhi'"
        if statelist != '':
            statelist = " state in ("+statelist+")"
            
        if where != '' and statelist != "" :
            statelist = " and "+statelist
            where = where + statelist
        elif where == "" and statelist != "":
            where = "WHERE "+statelist+""

        column_list = ''
        if 'city' in word_set or  'cities' in word_set:
            column_list = 'city'
        if 'state' in word_set or 'states' in word_set:
            if column_list != '':
                column_list = column_list + ", state"
            else:
                column_list = 'state'
        if 'population' in word_set:
            if column_list != '':
                column_list = column_list + ", population"
            else:
                column_list = "population"
        if column_list == "":
            column_list ="*"
        sql = sql.replace("%1%", column_list)
        sql = sql.replace("%2%", where)
    return sql

def genquery():
    userquery = input("Enter Your Requirement in one Sentence :")
    #print("Original Query :", userquery)
    word_tokens = word_tokenize(userquery)
    stop_words = set(stopwords.words('english'))

    filtered_sentence = [w for w in word_tokens if not w in stop_words]  
      
    filtered_sentence = []  
      
    for w in word_tokens:  
        if w not in stop_words:  
            filtered_sentence.append(w)  

    #print("Word Tokens :", word_tokens)  
    #print("Filetered Tokens :", filtered_sentence)  

    filtered_sentence_tagged = pos_tag(filtered_sentence)
    #print("Tagged Tokens :", filtered_sentence_tagged)  

    sql = getQuery(filtered_sentence)
    return sql

def updatereadings(sql, execution_time1, execution_time2):
    file = open('time_readings.txt', 'a')
    file.writelines('{query:s}\n'.format(query = sql))
    file.writelines('{reading1:.2f},{reading2:.2f}\n'.format(reading1 = execution_time1, reading2 = execution_time2))
    file.close()

def main():
    start_time = datetime.datetime.now()
    sql = genquery()
    #print(sql)
    myresult = db_mgmt.readdata(sql)
    end_time1 = datetime.datetime.now()
    print(myresult)
    end_time2 = datetime.datetime.now()
    time_diff1 = (end_time1 - start_time)
    execution_time1 = time_diff1.total_seconds() * 1000
    time_diff2 = (end_time2 - start_time)
    execution_time2 = time_diff2.total_seconds() * 1000
    print(execution_time1, execution_time2)
    updatereadings(sql, execution_time1, execution_time2)

main()
