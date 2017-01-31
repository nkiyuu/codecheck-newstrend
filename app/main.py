#!/usr/bin/env python3

import math
import urllib.request
import datetime
import xml.etree.ElementTree as ET
from goolabs import GoolabsAPI

def get_coefficients(list1, list2):
    """
    ２つのリストのピアソンの積率相関係数を求める
    """
    average_list1 = sum(list1)/len(list1)
    average_list2 = sum(list2)/len(list2)
    covariance = 0
    for i in range(len(list1)):
        covariance += (list1[i] - average_list1) * (list2[i] - average_list2)
    coefficients = covariance / get_standard_deviation(list1)
    coefficients /= get_standard_deviation(list2)
    coefficients = round(coefficients, 3)
    if coefficients == 1.0:
        return 1
    return coefficients
    
def get_standard_deviation(data_list):
    """
    データリストの標準偏差を求める
    """
    standard_deviation = 0
    average_data_list = sum(data_list) / len(data_list)
    for i in data_list:
        standard_deviation += math.pow((i - average_data_list), 2)
    standard_deviation = math.sqrt(standard_deviation)
    return standard_deviation

def get_term_numFound(keyword, start_day, end_day):
    """
    指定期間のあるキーワードのnumFoundの値を持ってくる
    """
    _quote = urllib.parse.quote_plus(keyword)
    ACCESS_KEY = "869388c0968ae503614699f99e09d960f9ad3e12"
    url = "http://54.92.123.84/search?q=Body:" + _quote + "%20AND%20ReleaseDate:[" + str(start_day.isoformat().split("T")[0]) + "%20TO%20" + str(end_day.isoformat().split("T")[0]) + "]&ackey=" + ACCESS_KEY
    response = urllib.request.urlopen(url)
    tree = ET.parse(response)
    root = tree.getroot()
    return int(root.find(".//result").attrib['numFound'])

def get_posChecker(keyword_list):
    app_id = "72557413b523d38db2d1de26f8095928d43d6d0882707ed41249f9edb643db45"
    api = GoolabsAPI(app_id)
    check_list = []
    for keyword in keyword_list:
        check_list.append(str(api.morph(sentence=keyword)["word_list"][0][0][1]))
    if len(list(set(check_list))):
        return True
    else:
        return False

def main(argv):

  start_date = datetime.datetime.strptime(argv[1] , '%Y-%m-%d')
  end_date = datetime.datetime.strptime(argv[2] , '%Y-%m-%d')
  term_start_date = start_date
  term_end_date = start_date + datetime.timedelta(days=6)
  keywords = argv[0]
  keyword_numFound_dict = {}
  for keyword in keywords:
      keyword_numFound_dict[keyword] = []
  while term_end_date < end_date:
      for keyword in keywords:    
          keyword_numFound_dict[keyword].append(get_term_numFound(keyword, term_start_date, term_end_date))
      term_start_date += datetime.timedelta(days=7)
      term_end_date += datetime.timedelta(days=7)
  coefficients = []
  for keyword1 in keywords:
      row = []
      for keyword2 in keywords:
          row.append(get_coefficients(keyword_numFound_dict[keyword1], keyword_numFound_dict[keyword2]))
      coefficients.append(row)
  answer = {"coefficients":coefficients, "posChecker": get_posChecker(keywords)}
  print(answer)
