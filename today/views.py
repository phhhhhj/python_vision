import requests
from django.shortcuts import render, redirect
import pymysql as my
from collections import Counter
import argparse


def select_rand(request):
    # 1. connector를 통해 db 연결
    con = my.connect(host='localhost', port=3708, user='root', password='1234', db='todayhouse')
    cursor = con.cursor()

    # sql문
    sql = "select * from images order by rand() limit 5"

    # print('sql문 실행 요청됨!!')
    result = cursor.execute(sql)
    # print('실행결과: ', result)

    # 스트림에서 데이터 꺼내오기
    records = cursor.fetchall()
    # print(type(records))

    con.commit()
    con.close()

    return render(request, 'today/random5.html', {'records': records})


def click_style(request, id):
    # 이전에 세션 잡힌 내용이 있다면 빼서 저장해두고
    # 새로 클릭된 style id와 함께 다시 세션 추가
    if request.session.get('style', None) != None:
        before = request.session['style']
        id = before + ',' + id
    request.session['style'] = id

    # 사진을 몇번 클릭했는지 세션으로 체크
    if request.session.get('cnt', None) != None:
        cnt = int(request.session['cnt'])
        request.session['cnt'] = str(cnt + 1)
    else:
        request.session['cnt'] = '1'

    # 5번 이하로 클릭되었으면 다시 사진 선택 페이지로 이동
    # 5번 클릭되었으면 결과 페이지로 이동
    if int(request.session['cnt']) < 5:
        return redirect('random5')
    else:
        # 3개의 이미지 링크, 가장 많이 선택한 스타일 반환 받음
        records, best = recommend(request)
        # 추천 스타일의 이미지 3개 비전 분석
        API_URL = 'https://kapi.kakao.com/v1/vision/multitag/generate'
        MYAPP_KEY = 'd2e5e757409558364083cf81b1409afe'  # 카카오 비전 rest api key
        sites = records

        label_list = []
        for site in sites:
            parser = argparse.ArgumentParser(description='')
            parser.add_argument('image_url', type=str, nargs='?', default=site)
            args = parser.parse_args()
            head = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}
            data = {'image_url': site}

            result = requests.post(API_URL, headers=head, data=data)
            json = result.json()
            result_json = json['result']

            for x in result_json['label_kr']:
                label_list.append(x)

        cnt = Counter(label_list).most_common(1)

        return render(request, 'today/result.html',
                      {'records': records, 'best': best, 'word': cnt})


def recommend(request):
    # 스타일 콤마 기준으로 분해
    choice = request.session['style'].split(',')
    # 가장 많이 등장한 스타일 추출
    best = Counter(choice).most_common(1)
    # 해당 스타일의 이미지 링크 3개 반환 받음
    records = select_one(best[0][0])

    # 세션 끊기
    del request.session['style']
    del request.session['cnt']

    return records, best[0][0]


def select_one(best):
    # 1. connector를 통해 db 연결
    con = my.connect(host='localhost', port=3708, user='root', password='1234', db='todayhouse')
    cursor = con.cursor()

    # 2. sql문 결정
    sql = "select img from images where style = %s order by rand() limit 3"
    result = cursor.execute(sql, best)

    #print('sql문 실행 요청됨!!')
    #print('실행결과: ', result)

    # 스트림에서 데이터 꺼내오기
    records = cursor.fetchall()
    #print(records)

    con.commit()
    con.close()

    return records
