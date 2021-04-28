import re
import spacy
import nltk
from nltk.corpus import stopwords
import pymorphy2
nltk.download('stopwords')
nltk.download('punkt')

stop_words = stopwords.words('russian')
morph = pymorphy2.MorphAnalyzer()

"""Очистка строки
input: строка с "грязными" данными
output: "чистая" строка
"""

def clean_string(string):
    dirt_patterns = [r'\'', r'\\n', r'\n', r'Б\\\\/Н', r'\\\\/\d+',r'\\\\/', r'\\{1,}',r'\(.*\)',r'c\.$',r'ул\.$',r'-\d+',r'пер\.$', r'д\.']
    for pattern in dirt_patterns:
        string = re.sub(pattern,'',string)
    return string


"""Поиск темы
input: строка для поиска темы
output: тема
"""

def search_theme(string):
    res = re.findall(r'«.*»',string)
    return res[0] if len(res)>0 else ""


"""Поиск адреса
input: строка для поиска адреса
output: адрес объекта
"""
def search_address(string):
    res = re.findall(r'по адресу\s?(.*$)',string)
    return res[0] if len(res)>0 else ""


"""Производит предварительную обработку текста
input: текст для обработки
output: ообработанный текс (без пунктуации, слова приведены к нормальной форме, числовые данные удалены)
"""

def preprocessingText(line):
    line = line.lower()
    line = re.sub(r'\d+','',line,flags=re.UNICODE)#delete numbers
    line = re.sub(r'[^\w\s]',' ',line,flags=re.UNICODE)
    tl = nltk.word_tokenize(line) #tl - tokenize line
    nft = [morph.parse(token)[0].normal_form for token in tl if len(token)>1]#nft - normal form token
    clean_words_list = [normalToken for normalToken in nft if normalToken not in stop_words and len(normalToken)>1]#преобразованный список
    return ' '.join(clean_words_list)


"""Приведение даты в необходимый формат
input:строка, содержащая дату
output: строка даты в формате dd.MM.yyyy hh:mm:ss
"""

def prepare_date(date_string):
    months = {'Января':'01','Февраля':'02','Марта':'03','Апреля':'04',
                'Мая':'05','Июня':'06','Июля':'07','Августа':'08',
                'Сентября':'09','Октября':'10','Ноября':'11','Декабря':'12'}
    date_string = re.sub(r'\s{2,}',' ',str(date_string.strip()))
    try:   
        split_date_string = date_string.split(' ')
        day = split_date_string[0]
        month = months[split_date_string[1]]
        year = split_date_string[2]
        time = split_date_string[4]
        full_date_string = "{0}.{1}.{2} {3}:00".format(day,month,year,time)      
    except Exception as error:
        full_date_string = date_string
    return full_date_string


"""Поиск округа
input: строка, в которой может содержаться округ
output: округ или строка, подававшаяся на вход, в зависимости от результата поиска
"""

def search_district(full_address):
    searched = re.findall(r'округ\s+?(.+?),',full_address)
    result = full_address if len(searched)==0 else searched[0]
    return result