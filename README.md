# DART_Report

- **dart_report_crawler.ipy**

DART (전자공시) 에서 KOSPI 상장사의

사업보고서를 크롤링 하는 크롤러 제작

(분기 보고서 까지 크롤링 하는 코드는 별도)

보고서 항목은 10개로 분류


- **table_parser_CEO_CFO.py**

크롤링해서 저장된 보고서 내용 중

'임원 및 직원 등에 관한 사항' 항목에 접근하여,

대표이사가 누구인지 확인 및 비교 할 수 있도록

table parse 해서 pandas DataFrame 형태로 출력
