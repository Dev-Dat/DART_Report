#######################################################################################################################
#####################################   텍스트 별도 정제 없이... 있는 그대로 받아서 저장하는 코드 ##############################
import webbrowser
from urllib.request import urlopen
import time
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import datetime
from tqdm import tqdm
import time

#%%
#콘솔창 넓게 보기
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)
#%%
# company_code = '051910' #lg화학 기업코드
# KOSPI 10-K(사업보고서) 1~10번 항목 전체 내용 크롤러
def year_get_rcp(company_code, date):
    import time
    API_Key = '4800bd6ebc56177df6597027270cb71a1ccab416'
    from dateutil.parser import parse as p

    if len(str(company_code)) == 7: company_code = company_code[1:]
    print('Company Code :', company_code)
    if type(date) == str: date = p(date)
    print('Today :', date)

    url = "http://opendart.fss.or.kr/api/list.xml?crtfc_key=" + API_Key + "&corp_code=" + company_code + "&bgn_de=19900101&pblntf_detail_ty=A001&corp_cls=Y&page_count=60" + "&last_reprt_at=Y"

    xmlsoup = BeautifulSoup(urlopen(url).read(), 'html.parser')

    te = xmlsoup.findAll("list")

    data = pd.DataFrame()
    for t in te:
        time.sleep(0.5)
        if '사업보고서' in str(te[0]) :
            temp = pd.DataFrame(([
                [t.corp_cls.string, t.corp_name.string, t.stock_code.string, t.report_nm.string, t.rcept_no.string,
                 t.flr_nm.string, t.rcept_dt.string, t.rm.string]]),
                                columns=["corp_cls", "corp_nm", "corp_code", "report_nm", "rcept_no", "flr_nm", "rcept_dt", "rmk"])
            data = pd.concat([data, temp])

    #time.sleep(1)

    if len(data) != 0 :
        #data['rcept_dt'] = data['rcept_dt'].apply(lambda x: p(x))
        #data = data.drop_duplicates('rcept_dt')
        #data = data[data['rmk']!='정연']
        #data = data[data['rcept_dt'] < date]
        data = data.reset_index(drop=True)
        data['y_sort'] = data['report_nm'].apply(lambda x: str(x[-8:]).split('.')[0])
        data = data.sort_values('y_sort', ascending=False)

    return data

#%%
# 첨부정정 포함된 리포트 필터링
# redown_list = []
# for i in range(len(corp_codes)):
#     time.sleep(2)
#     report_checker = year_get_rcp(str(corp_codes[i]).zfill(6), today)
#     time.sleep(4)
#     if len(report_checker) != 0:
#         if (len(report_checker['report_nm']) > 0) and ('[첨부정정]' in str(report_checker['report_nm'])):
#             time.sleep(4)
#             redown_list.append(str(report_checker['corp_code'][0]))
#             time.sleep(2)
#%%
# 첨부정정 리포트까지 접근 & 저장

def Year_Report_Crawler_v2(company_code, today):
    # company_code = '035420'
    # company_code = '051910'

    data = year_get_rcp(company_code, today)

    if len(data) != 0 :
        urls = []
        pages = []

        for i in range(len(data['rcept_no'])):
            if '[첨부정정]' in str(data['report_nm'][i]):
                data['rcept_no'][i] = str(BeautifulSoup(urlopen("http://dart.fss.or.kr/dsaf001/main.do?rcpNo=" +
                                                                     data['rcept_no'][i]).read(), 'html.parser').find('select').find_all('option')[1]).split("value=")[1].split(">")[0].split("rcpNo=")[1].split('"')[0]

        #time.sleep(1)
        for i in range(len(data['rcept_no'])):
            urls.append(
                "http://dart.fss.or.kr/dsaf001/main.do?rcpNo=" + data['rcept_no'][i])  # 보고서 발행일자별로 link 생성해줌

        #time.sleep(1)
        for i in range(len(urls)):
            pages.append(BeautifulSoup(urlopen(urls[i]).read(), 'html.parser'))


        # pages1 = pages

        body1 = []
        body2 = []
        body3 = []
        body4 = []
        body5 = []
        body6 = []
        body7 = []
        body8 = []
        body9 = []
        body10 = []
        #body11 = []

        # 20년치
        for i in tqdm(range(len(pages))):

            time.sleep(1)
            if 'I. 회사의 개요"' in str(pages[i].find('head')):
                body1.append(
                    str(pages[i].find('head')).split('I. 회사의 개요",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            if 'I. 회사의 개황"' in str(pages[i].find('head')):
                body1.append(
                    str(pages[i].find('head')).split('I. 회사의 개황",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[
                        0].split(', ')
                )

            time.sleep(1)
            if ('II. 사업의 내용("' not in str(pages[i].find('head'))) and ('II. 사업의 내용"' in str(pages[i].find('head'))):
                body2.append(
                    str(pages[i].find('head')).split('II. 사업의 내용",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )

            if 'II. 사업의 내용(제조업)"' in str(pages[i].find('head')):
                body2.append(
                    str(pages[i].find('head')).split('II. 사업의 내용(제조업)",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            #time.sleep(1)
            if 'II. 사업의 내용(은행업)"' in str(pages[i].find('head')):
                body2.append(
                    str(pages[i].find('head')).split('II. 사업의 내용(은행업)",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )

            if 'II. 사업의 내용(보험업)"' in str(pages[i].find('head')):
                body2.append(
                    str(pages[i].find('head')).split('II. 사업의 내용(보험업)",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            #time.sleep(1)

            if 'II. 사업의 내용(증권업)"' in str(pages[i].find('head')):
                body2.append(
                    str(pages[i].find('head')).split('II. 사업의 내용(증권업)",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )


            if 'II. 사업의 내용(도소매업)"' in str(pages[i].find('head')):
                body2.append(
                    str(pages[i].find('head')).split('II. 사업의 내용(도소매업)",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            #time.sleep(1)

            if 'II. 사업의 내용(건설업)"' in str(pages[i].find('head')):
                body2.append(
                    str(pages[i].find('head')).split('II. 사업의 내용(건설업)",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )

            time.sleep(1)

            if 'III. 재무에 관한 사항"' in str(pages[i].find('head')):
                body3.append(
                    str(pages[i].find('head')).split('III. 재무에 관한 사항",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )

            time.sleep(1)

            if 'IV. 감사인의 감사의견 등"' in str(pages[i].find('head')):
                body4.append(
                    str(pages[i].find('head')).split('IV. 감사인의 감사의견 등",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            #time.sleep(1)

            if 'IV. 감사인의 감사의견 등"' not in str(pages[i].find('head')) and 'V. 감사인의 감사의견 등"' in str(pages[i].find('head')):
                body4.append(
                    str(pages[i].find('head')).split('V. 감사인의 감사의견 등",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )

            time.sleep(1)
            if 'VII. 주주에 관한 사항"' in str(pages[i].find('head')):
                body5.append(
                    str(pages[i].find('head')).split('VII. 주주에 관한 사항",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            #time.sleep(1)
            if 'VII. 주주에 관한 사항"' not in str(pages[i].find('head')) and 'VI. 주식에 관한 사항"' in str(pages[i].find('head')):
                body5.append(
                    str(pages[i].find('head')).split('VI. 주식에 관한 사항",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            #time.sleep(1)
            if ('VII. 주주에 관한 사항"' not in str(pages[i].find('head')) and 'VI. 주식에 관한 사항"' not in str(pages[i].find('head'))) and 'VI. 주주에 관한 사항"' in str(pages[i].find('head')):
                body5.append(
                    str(pages[i].find('head')).split('VI. 주주에 관한 사항",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            #time.sleep(1)
            if ('VII. 주주에 관한 사항"' not in str(pages[i].find('head')) and 'VI. 주식에 관한 사항"' not in str(pages[i].find('head')) and 'VI. 주주에 관한 사항"' not in str(pages[i].find('head'))) and 'V. 주주에 관한 사항"' in str(pages[i].find('head')):
                body5.append(
                    str(pages[i].find('head')).split('V. 주주에 관한 사항",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            time.sleep(1)
            if 'VIII. 임원 및 직원 등에 관한 사항"' in str(pages[i].find('head')):
                body6.append(
                    str(pages[i].find('head')).split('VIII. 임원 및 직원 등에 관한 사항",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            #time.sleep(1)
            if 'VIII. 임원 및 직원 등에 관한 사항"' not in str(pages[i].find('head')) and 'VII. 임원 및 직원 등에 관한 사항"' in str(pages[i].find('head')):
                body6.append(
                    str(pages[i].find('head')).split('VII. 임원 및 직원 등에 관한 사항",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )

            time.sleep(1)
            if 'X. 이해관계자와의 거래내용"' in str(pages[i].find('head')):
                body7.append(
                    str(pages[i].find('head')).split('X. 이해관계자와의 거래내용",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            #time.sleep(1)
            if 'X. 이해관계자와의 거래내용"' not in str(pages[i].find('head')) and 'IX. 이해관계자와의 거래내용"' in str(pages[i].find('head')):
                body7.append(
                    str(pages[i].find('head')).split('IX. 이해관계자와의 거래내용",')[1].split('cnt++')[0].split('viewDoc(')[1].split(
                        ')')[0].split(', ')
                )
            #time.sleep(1)
            if ('X. 이해관계자와의 거래내용"' not in str(pages[i].find('head'))) and ('IX. 이해관계자와의 거래내용"' not in str(pages[i].find('head'))) and 'VIII. 이해관계자와의 거래내용"' in str(pages[i].find('head')):
                body7.append(
                    str(pages[i].find('head')).split('VIII. 이해관계자와의 거래내용",')[1].split('cnt++')[0].split('viewDoc(')[1].split(
                        ')')[0].split(', ')
                )
            time.sleep(1)

            if 'VI. 이사회 등 회사의 기관에 관한 사항"' in str(pages[i].find('head')):
                body8.append(
                    str(pages[i].find('head')).split('VI. 이사회 등 회사의 기관에 관한 사항",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            #time.sleep(1)
            if 'VI. 이사회 등 회사의 기관에 관한 사항"' not in str(pages[i].find('head')) and 'VI. 이사회 등 회사의 기관 및 계열회사에 관한 사항"' in str(pages[i].find('head')):
                body8.append(
                    str(pages[i].find('head')).split('VI. 이사회 등 회사의 기관 및 계열회사에 관한 사항",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            #time.sleep(1)
            if 'V. 이사회 등 회사의 기관 및 계열회사에 관한 사항"' in str(pages[i].find('head')):
                body8.append(
                    str(pages[i].find('head')).split('V. 이사회 등 회사의 기관 및 계열회사에 관한 사항",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            time.sleep(1)
            if 'IX. 계열회사 등에 관한 사항"' in str(pages[i].find('head')):
                body8.append(
                    str(pages[i].find('head')).split('IX. 계열회사 등에 관한 사항",')[1].split('cnt++')[0].split('viewDoc(')[
                        1].split(')')[0].split(', ')
                )
            #time.sleep(1)
            if 'V. 지배구조 및 관계회사 등의 현황"' in str(pages[i].find('head')):
                body8.append(
                    str(pages[i].find('head')).split('V. 지배구조 및 관계회사 등의 현황",')[1].split('cnt++')[0].split('viewDoc(')[
                        1].split(')')[0].split(', ')
                )
            #time.sleep(1)
            if 'V. 지배구조 및 관계회사 등의 현황"' not in str(pages[i].find('head')) and 'V. 지배구조 및 관계회사등의 현황"' in str(pages[i].find('head')):
                body8.append(
                    str(pages[i].find('head')).split('V. 지배구조 및 관계회사등의 현황",')[1].split('cnt++')[0].split('viewDoc(')[
                        1].split(')')[0].split(', ')
                )

            time.sleep(1)
            if 'XI. 그 밖에 투자자 보호를 위하여 필요한 사항"' in str(pages[i].find('head')):
                body9.append(
                    str(pages[i].find('head')).split('XI. 그 밖에 투자자 보호를 위하여 필요한 사항",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            #time.sleep(1)
            if 'XI. 그 밖에 투자자 보호를 위하여 필요한 사항"' not in str(pages[i].find('head')) and 'X. 그 밖에 투자자 보호를 위하여 필요한 사항"' in str(pages[i].find('head')):
                body9.append(
                    str(pages[i].find('head')).split('X. 그 밖에 투자자 보호를 위하여 필요한 사항",')[1].split('cnt++')[0].split('viewDoc(')[1].split(
                        ')')[0].split(', ')
                )
            #time.sleep(1)
            if 'X. 기타 필요한 사항"' in str(pages[i].find('head')):
                body9.append(
                    str(pages[i].find('head')).split('X. 기타 필요한 사항",')[1].split('cnt++')[0].split('viewDoc(')[
                        1].split(')')[0].split(', ')
                )

            # if 'XII. 부속명세서"' in str(pages1[i].find('head')) :
            #     body9.append(
            #         str(pages1[i].find('head')).split('XII. 부속명세서",')[1].split('cnt++')[0].split('viewDoc(')[1].split(
            #             ')')[0].split(', ')
            #     )
            #
            # if 'IX. 부속명세서"' in str(pages1[i].find('head')) :
            #     body9.append(
            #         str(pages1[i].find('head')).split('IX. 부속명세서",')[1].split('cnt++')[0].split('viewDoc(')[1].split(
            #             ')')[0].split(', ')
            #     )
            time.sleep(1)
            if 'IV. 이사의 경영진단 및 분석의견"' in str(pages[i].find('head')):
                body10.append(
                    str(pages[i].find('head')).split('IV. 이사의 경영진단 및 분석의견",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            if 'IV. 이사의 경영진단 및 분석의견"' not in str(pages[i].find('head')) and 'V. 이사의 경영진단 및 분석의견"' in str(pages[i].find('head')):
                body10.append(
                    str(pages[i].find('head')).split('V. 이사의 경영진단 및 분석의견",')[1].split('cnt++')[0].split('viewDoc(')[1].split(')')[0].split(', ')
                )
            if ('IV. 이사의 경영진단 및 분석의견"' and 'V. 이사의 경영진단 및 분석의견"') not in str(pages[i].find('head')):
                pass

        bodies1 = [body1[i][0:-1] for i in range(len(body1))]
        bodies2 = [body2[i][0:-1] for i in range(len(body2))]
        bodies3 = [body3[i][0:-1] for i in range(len(body3))]
        bodies4 = [body4[i][0:-1] for i in range(len(body4))]
        bodies5 = [body5[i][0:-1] for i in range(len(body5))]
        bodies6 = [body6[i][0:-1] for i in range(len(body6))]
        bodies7 = [body7[i][0:-1] for i in range(len(body7))]
        bodies8 = [body8[i][0:-1] for i in range(len(body8))]
        bodies9 = [body9[i][0:-1] for i in range(len(body9))]
        bodies10 = [body10[i][0:-1] for i in range(len(body10))]


            # final url 만들기

        urls_final1 = []
        urls_final2 = []
        urls_final3 = []
        urls_final4 = []
        urls_final5 = []
        urls_final6 = []
        urls_final7 = []
        urls_final8 = []
        urls_final9 = []
        urls_final10 = []


    # 사업보고서 부문별 텍스트 최종 링크 생성

        for i in range(len(bodies1)):
            urls_final1.append(
                'http://dart.fss.or.kr/report/viewer.do?rcpNo=' + bodies1[i][0].strip("''") + '&dcmNo=' + bodies1[i][
                    1].strip("''") + '&eleId=' + bodies1[i][2].strip("''") + '&offset=' + bodies1[i][3].strip(
                    "''") + '&length=' + bodies1[i][4].strip("''") + '&dtd=dart3.xsd')

        for i in range(len(bodies2)):
            urls_final2.append(
                'http://dart.fss.or.kr/report/viewer.do?rcpNo=' + bodies2[i][0].strip("''") + '&dcmNo=' + bodies2[i][
                    1].strip("''") + '&eleId=' + bodies2[i][2].strip("''") + '&offset=' + bodies2[i][3].strip(
                    "''") + '&length=' + bodies2[i][4].strip("''") + '&dtd=dart3.xsd')

        for i in range(len(bodies3)):
            urls_final3.append(
                'http://dart.fss.or.kr/report/viewer.do?rcpNo=' + bodies3[i][0].strip("''") + '&dcmNo=' + bodies3[i][
                    1].strip("''") + '&eleId=' + bodies3[i][2].strip("''") + '&offset=' + bodies3[i][3].strip(
                    "''") + '&length=' + bodies3[i][4].strip("''") + '&dtd=dart3.xsd')

        for i in range(len(bodies4)):
            urls_final4.append(
                'http://dart.fss.or.kr/report/viewer.do?rcpNo=' + bodies4[i][0].strip("''") + '&dcmNo=' + bodies4[i][
                    1].strip("''") + '&eleId=' + bodies4[i][2].strip("''") + '&offset=' + bodies4[i][3].strip(
                    "''") + '&length=' + bodies4[i][4].strip("''") + '&dtd=dart3.xsd')

        for i in range(len(bodies5)):
            urls_final5.append(
                'http://dart.fss.or.kr/report/viewer.do?rcpNo=' + bodies5[i][0].strip("''") + '&dcmNo=' + bodies5[i][
                    1].strip("''") + '&eleId=' + bodies5[i][2].strip("''") + '&offset=' + bodies5[i][3].strip(
                    "''") + '&length=' + bodies5[i][4].strip("''") + '&dtd=dart3.xsd')

        for i in range(len(bodies6)):
            urls_final6.append(
                'http://dart.fss.or.kr/report/viewer.do?rcpNo=' + bodies6[i][0].strip("''") + '&dcmNo=' + bodies6[i][
                    1].strip("''") + '&eleId=' + bodies6[i][2].strip("''") + '&offset=' + bodies6[i][3].strip(
                    "''") + '&length=' + bodies6[i][4].strip("''") + '&dtd=dart3.xsd')

        for i in range(len(bodies7)):
            urls_final7.append(
                'http://dart.fss.or.kr/report/viewer.do?rcpNo=' + bodies7[i][0].strip("''") + '&dcmNo=' + bodies7[i][
                    1].strip("''") + '&eleId=' + bodies7[i][2].strip("''") + '&offset=' + bodies7[i][3].strip(
                    "''") + '&length=' + bodies7[i][4].strip("''") + '&dtd=dart3.xsd')

        for i in range(len(bodies8)):
            urls_final8.append(
                'http://dart.fss.or.kr/report/viewer.do?rcpNo=' + bodies8[i][0].strip("''") + '&dcmNo=' + bodies8[i][
                    1].strip("''") + '&eleId=' + bodies8[i][2].strip("''") + '&offset=' + bodies8[i][3].strip(
                    "''") + '&length=' + bodies8[i][4].strip("''") + '&dtd=dart3.xsd')

        for i in range(len(bodies9)):
            urls_final9.append(
                'http://dart.fss.or.kr/report/viewer.do?rcpNo=' + bodies9[i][0].strip("''") + '&dcmNo=' + bodies9[i][
                    1].strip("''") + '&eleId=' + bodies9[i][2].strip("''") + '&offset=' + bodies9[i][3].strip(
                    "''") + '&length=' + bodies9[i][4].strip("''") + '&dtd=dart3.xsd')

        for i in range(len(bodies10)):
            urls_final10.append(
                'http://dart.fss.or.kr/report/viewer.do?rcpNo=' + bodies10[i][0].strip("''") + '&dcmNo=' + bodies10[i][
                    1].strip("''") + '&eleId=' + bodies10[i][2].strip("''") + '&offset=' + bodies10[i][3].strip(
                    "''") + '&length=' + bodies10[i][4].strip("''") + '&dtd=dart3.xsd')

        # for i in range(len(bodies11)):
        #     urls_final11.append(
        #         'http://dart.fss.or.kr/report/viewer.do?rcpNo=' + bodies11[i][0].strip("''") + '&dcmNo=' + bodies11[i][
        #             1].strip("''") + '&eleId=' + bodies11[i][2].strip("''") + '&offset=' + bodies11[i][3].strip(
        #             "''") + '&length=' + bodies11[i][4].strip("''") + '&dtd=dart3.xsd')


        # 최종 URL 링크로 들어가 텍스트 가져오기

        body_final1 = []
        body_final2 = []
        body_final3 = []
        body_final4 = []
        body_final5 = []
        body_final6 = []
        body_final7 = []
        body_final8 = []
        body_final9 = []
        body_final10 = []
        #body_final11 = []


        data_folder_path = "D:/2020/paper/data_folder_alltag_newversion/"  + data['corp_nm'][0] + "_Report"
        Path(data_folder_path).mkdir(parents=True, exist_ok=True)

        content_list = ['content1', 'content2', 'content3', 'content4', 'content5', 'content6', 'content7', 'content8', 'content9', 'content10']

        data_file_path1 = data_folder_path + '/' + data['corp_nm'][0] + "_" + content_list[0] + ".txt"
        data_file_path2 = data_folder_path + '/' + data['corp_nm'][0] + "_" + content_list[1] + ".txt"
        data_file_path3 = data_folder_path + '/' + data['corp_nm'][0] + "_" + content_list[2] + ".txt"
        data_file_path4 = data_folder_path + '/' + data['corp_nm'][0] + "_" + content_list[3] + ".txt"
        data_file_path5 = data_folder_path + '/' + data['corp_nm'][0] + "_" + content_list[4] + ".txt"
        data_file_path6 = data_folder_path + '/' + data['corp_nm'][0] + "_" + content_list[5] + ".txt"
        data_file_path7 = data_folder_path + '/' + data['corp_nm'][0] + "_" + content_list[6] + ".txt"
        data_file_path8 = data_folder_path + '/' + data['corp_nm'][0] + "_" + content_list[7] + ".txt"
        data_file_path9 = data_folder_path + '/' + data['corp_nm'][0] + "_" + content_list[8] + ".txt"
        data_file_path10 = data_folder_path + '/' + data['corp_nm'][0] + "_" + content_list[9] + ".txt"
        #data_file_path11 = data_folder_path + '/' + data['corp_nm'][0] + "_" + content_list[10] + ".txt"


        for i in range(len(urls_final1)):
            time.sleep(0.5)
            body_final1.append([BeautifulSoup(urlopen(urls_final1[i]).read(), 'html.parser')])

        texts_final1 = []
        for i in tqdm(range(len(body_final1))):
            for j in range(len(body_final1[i])):
                time.sleep(0.5)
                texts_final1.append([str(body_final1[i][j].find_all('body'))])


        with open(data_file_path1, "w", encoding='UTF-8') as test_output1:
            text_output1 = test_output1.write(str(texts_final1))

        #time.sleep(10)

        for i in range(len(urls_final2)):
            time.sleep(0.5)
            body_final2.append([BeautifulSoup(urlopen(urls_final2[i]).read(), 'html.parser')])

        texts_final2 = []
        for i in tqdm(range(len(body_final2))):
            for j in range(len(body_final2[i])):
                time.sleep(0.5)
                texts_final2.append([str(body_final2[i][j].find_all('body'))])

        with open(data_file_path2, "w", encoding='UTF-8') as test_output2:
            text_output2 = test_output2.write(str(texts_final2))

        #time.sleep(10)


        for i in range(len(urls_final3)):
            time.sleep(0.5)
            body_final3.append([BeautifulSoup(urlopen(urls_final3[i]).read(), 'html.parser')])

        texts_final3 = []
        for i in tqdm(range(len(body_final3))):
            for j in range(len(body_final3[i])):
                time.sleep(0.5)
                texts_final3.append([str(body_final3[i][j].find_all('body'))])

        with open(data_file_path3, "w", encoding='UTF-8') as test_output3:
            text_output3 = test_output3.write(str(texts_final3))

        #time.sleep(10)

        for i in range(len(urls_final4)):
            time.sleep(0.5)
            body_final4.append([BeautifulSoup(urlopen(urls_final4[i]).read(), 'html.parser')])

        texts_final4 = []
        for i in tqdm(range(len(body_final4))):
            for j in range(len(body_final4[i])):
                time.sleep(0.5)
                texts_final4.append([str(body_final4[i][j].find_all('body'))])

        with open(data_file_path4, "w", encoding='UTF-8') as test_output4:
            text_output4 = test_output4.write(str(texts_final4))

        #time.sleep(10)


        for i in range(len(urls_final5)):
            time.sleep(0.5)
            body_final5.append([BeautifulSoup(urlopen(urls_final5[i]).read(), 'html.parser')])

        texts_final5 = []
        for i in tqdm(range(len(body_final5))):
            for j in range(len(body_final5[i])):
                time.sleep(0.5)
                texts_final5.append([str(body_final5[i][j].find_all('body'))])

        with open(data_file_path5, "w", encoding='UTF-8') as test_output5:
            text_output5 = test_output5.write(str(texts_final5))

        #time.sleep(10)


        for i in range(len(urls_final6)):
            time.sleep(0.5)
            body_final6.append([BeautifulSoup(urlopen(urls_final6[i]).read(), 'html.parser')])

        texts_final6 = []
        for i in tqdm(range(len(body_final6))):
            for j in range(len(body_final6[i])):
                time.sleep(0.5)
                texts_final6.append([str(body_final6[i][j].find_all('body'))])

        with open(data_file_path6, "w", encoding='UTF-8') as test_output6:
            text_output6 = test_output6.write(str(texts_final6))

        #time.sleep(10)


        for i in range(len(urls_final7)):
            time.sleep(0.5)
            body_final7.append([BeautifulSoup(urlopen(urls_final7[i]).read(), 'html.parser')])

        texts_final7 = []
        for i in tqdm(range(len(body_final7))):
            for j in range(len(body_final7[i])):
                time.sleep(0.5)
                texts_final7.append([str(body_final7[i][j].find_all('body'))])

        with open(data_file_path7, "w", encoding='UTF-8') as test_output7:
            text_output7 = test_output7.write(str(texts_final7))

        #time.sleep(10)


        for i in range(len(urls_final8)):
            time.sleep(0.5)
            body_final8.append([BeautifulSoup(urlopen(urls_final8[i]).read(), 'html.parser')])

        # 01 / 23 / 45 / 67 / 89 / 1011
        year = datetime.date.today().year
        texts_final8 = []
        try:
            for i in tqdm(range(0, (year - 2014)*2, 2)):
                time.sleep(0.5)
                texts_final8.append([str(body_final8[i][0].find_all('body')) + str(body_final8[i + 1][0].find_all('body'))])
            for i in tqdm(range((year - 2014)*2, len(body_final8), 1)):
                time.sleep(0.5)
                texts_final8.append([str(body_final8[i][0].find_all('body'))])
        except:
            for i in tqdm(range(len(body_final8))):
                for j in range(len(body_final8[i])):
                    time.sleep(0.5)
                    texts_final8.append([str(body_final8[i][j].find_all('body'))])

        with open(data_file_path8, "w", encoding='UTF-8') as test_output8:
            text_output8 = test_output8.write(str(texts_final8))

        #time.sleep(10)

        for i in range(len(urls_final9)):
            time.sleep(0.5)
            body_final9.append([BeautifulSoup(urlopen(urls_final9[i]).read(), 'html.parser')])

        texts_final9 = []
        for i in tqdm(range(len(body_final9))):
            for j in range(len(body_final9[i])):
                time.sleep(0.5)
                texts_final9.append([str(body_final9[i][j].find_all('body'))])

        with open(data_file_path9, "w", encoding='UTF-8') as test_output9:
            text_output9 = test_output9.write(str(texts_final9))

        #time.sleep(10)


        for i in range(len(urls_final10)):
            time.sleep(0.5)
            body_final10.append([BeautifulSoup(urlopen(urls_final10[i]).read(), 'html.parser')])

        texts_final10 = []
        for i in tqdm(range(len(body_final10))):
            for j in range(len(body_final10[i])):
                time.sleep(0.5)
                texts_final10.append([str(body_final10[i][j].find_all('body'))])

        with open(data_file_path10, "w", encoding='UTF-8') as test_output10:
            text_output10 = test_output10.write(str(texts_final10))

        #time.sleep(10)

        end = 'company report, export to txt complete'

        return end

#%%

# KOSPI 상장기업 코드 Load
############ Original Code ############
corp_codes = pd.read_csv('D:/2020/paper/DART_crawler/corp_codes_new_v4_woempty.csv')
corp_codes = corp_codes['codes'][478:]
corp_codes = corp_codes.reset_index()
corp_codes = corp_codes.drop('index', axis=1)

corp_name_list = pd.read_csv('D:/2020/paper/DART_crawler/corp_names_v2.csv', sep='/')
corp_name_list = corp_name_list['name'][478:]
corp_name_list = corp_name_list.reset_index()
corp_name_list = corp_name_list.drop('index', axis=1)

# RESUME LIST CHECK
str(corp_codes['codes'][0]).zfill(6)
str(corp_name_list['name'][0])

#%%

today = datetime.datetime.today()
start_time = time.time()
#corp_codes_temp = ['023530','068270','051900']

for i in range(len(corp_codes)):

    start_time_inner = time.time()

    Year_Report_Crawler_v2(str(corp_codes['codes'][i]).zfill(6), today)

    #Year_Report_Crawler_v2('035420', today)

    print(corp_name_list['name'][i]+"(기업코드 : A" + str(corp_codes['codes'][i]).zfill(6) + ") 의 사업보고서.. 10개 항목 전체기간 텍스트 데이터 크롤링에 소요된 시간.." + str(round((time.time() - start_time_inner),2) / 60) + "분")
    #print("삼성중공업의 사업보고서.. 10개 항목 전체기간 텍스트 데이터 크롤링에 소요된 시간.." + str(round((time.time() - start_time_inner), 2) / 60) + "분")

print(str(len(corp_codes['codes'])) + " 개 기업, 사업보고서 텍스트 데이터 크롤링에 소요한 총 시간: " + str(round(float(time.time() - start_time_inner),2) / 60) + "분")
#%%
# 023530 / 068270 / 051900
# SKv, GSv / 네이버v, 엔씨소프트v / 삼성전자v, 하이닉스v / 한국조선해양v, 삼성중공업v / 현대건설v, GS건설v / LG화학v, S-OILv / 하나투어v, 호텔신라v / 포스코v, 고려아연v / 현대차v, 기아차v / 이마트v, 롯데쇼핑 / 셀트리온, LG생활건강