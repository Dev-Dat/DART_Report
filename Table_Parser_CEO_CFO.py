import pandas as pd
from bs4 import BeautifulSoup
import pickle
from tqdm import tqdm
#%%

# 775개 기업 사업보고서 (단어 토큰) LOAD -- Cosine 계산용
load_data_path = 'D:/2020/paper/8.text_data_pickled/content_corp_document_v2.txt'
with open (load_data_path, 'rb') as fp:
    content_doc = pickle.load(fp)

#%%
corp_name_list = pd.read_csv('D:/2020/paper/0.text_crawler/corp_names_v2.csv', sep=',') #사업보고서 없는 기업들 제거한 리스트
content_corp_total = [[] for _ in range(len(corp_name_list['name']))] # 빈 리스트 775개 생성용
for i in tqdm(range(len(content_corp_total))):
    for j in range(1, 11):
        content_corp_total[i].append(open(
            'D:/2020/paper/7.text_data_raw/' + corp_name_list['name'][i] + '_report/' + corp_name_list['name'][
                i] + '_content' + str(j) + '.txt', 'r', encoding='UTF-8').readlines())
#%%
'''
########################################################################################################################
#################################### 대표이사 변경사항 체크 가능한 Table Parser Function #################################### 
########################################################################################################################
'''
def table_parser(content_corp_raw, corp_num, doc_num=5):

    target = eval(content_corp_raw[corp_num][doc_num][0]) # 8번 기업(제이콘텐트리) raw text load # length = 21
    final_list = [[] for _ in range(len(target))]
    soup = BeautifulSoup(target[0][0], 'lxml')  # 8번 기업, 6번 임직원 항목, 첫번째(index = 0) 문서에 접근 [0]
    # 최종 DataFrame column 명으로 사용될 값들 추출
    col_name = []
    for i in range(len(soup.find('thead').find_all('th'))):
        col_name.append(soup.find('thead').find_all('th')[i].get_text())
    col_name = col_name[:8] + col_name[-2:] + col_name[9:12]

    rowList = []
    columnList = []
    for i in range(len(target)):
        soup = BeautifulSoup(target[i][0], 'lxml') # 8번 기업, 6번 임직원 항목, 첫번째(index = 0) 문서에 접근 [0]
        # 테이블에 접근해서 임원 정보 추출
        table = soup.find_all('tbody')[1] # 두번째 테이블 접근
        trData = table.find_all('tr')
        for j in range(len(trData)):
            tdData = trData[j].find_all('td')
            for k in range(len(tdData)):
                element = tdData[k].text
                columnList.append(element)
            rowList.append(columnList)
            columnList=[]
        final_list[i].append(pd.DataFrame(rowList, columns=[col_name]))
    rows_total = pd.DataFrame(rowList, columns=[col_name])
    print(rows_total)
    return final_list
#%%
# Function Check
# 카카오 임직원 항목 테이블에 접근 & DataFrame 형태로 출력
table_parse_test = table_parser(content_corp_total, 39, 5)