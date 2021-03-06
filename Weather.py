#-*- coding:utf-8 -*-
# Discord.py 날씨 알리미 봇

import requests
import discord
import asyncio
import os


client = discord.Client()
@client.event
async def on_ready():
    print("="*20)
    print(client.user.name)
    print(client.user.id)
    print("="*20)
@client.event
async def on_message(message):
    global w #To Do: 전역 변수 말고 다른 방법은 없을까
    if message.content.startswith('!날씨'):
        requestCurrentWeather('강원', '원주시', '신림면')
        print("질문 '!날씨'를 요청받았다.")
        await client.send_message(message.channel, '현재 강원도 원주시 신림면의 날씨는\n' + w + '\n입니다.')
        #To Do: 입력받은 지역의 좌표나 이름을 통해 그 지역의 현재 날씨를 알려주는 기능



        
# 아래 소스코드의 원본은
# https://blog.naver.com/chandong83/221144142343
# 여기입니다.
            
# appKey는
# https://developers.sktelecom.com/
# 여기에서 받을 수 있다.
appKey = "(발급받은 appKey를 써주세요)"

# 현재 날씨(시간별) 요청 URL
url_hourly = "https://api2.sktelecom.com/weather/current/hourly"
# 현재 날씨(분별) 요청 URL 
# 소스코드를 그대로 퍼오느라 사실상 이건 그냥 장식
url_minutely = "http://api2.sktelecom.com/weather/current/minutely"

# 헤더
headers = {'Content-Type': 'application/json; charset=utf-8', 'appKey': appKey}


def hourly(weather):
    global w
    print("날씨")

    # 상대 습도
    humidity = weather['humidity']

    # 발표 시간
    timeRelease = weather['timeRelease']

    # 격자정보
    # 위도
    grid_la = weather['grid']['latitude']
    # 경도
    grid_lo = weather['grid']['longitude']
    # 시, 도
    grid_city = weather ['grid']['city']
    # 시, 군, 구
    grid_county = weather['grid']['county']
    # 읍, 면, 동
    grid_village = weather['grid']['village']

    # 기온 정보
    # 오늘의 최고기온
    temperature_tmax = weather['temperature']['tmax']
    # 1시간 현재기온
    temperature_tc  = weather ['temperature']['tc']
    # 오늘의 최저기온
    temperature_tmin = weather['temperature']['tmin']

    # 낙뢰 유뮤
    # - 0: 없음
    # - 1: 있음
    lightning = weather['lightning']
    
    # 강수량
    # 강수형태코드
    # - 0: 현상없음 → rain(sinceOntime) 사용
    # - 1: 비       → rain(sinceOntime) 사용
    # - 2: 비/눈 → precipitation(sinceOntime) 사용
    # - 3: 눈    → precipitation(sinceOntime) 사용
    precipitation_type = weather['precipitation']['type']

    # 1시간 누적 강수량
    # - if type=0/1/2 → 강우량 (mm)
    # - if type=3     → 적설량 (cm)
    precipitation_sinceOntime = weather['precipitation']['sinceOntime']

    # 바람정보
    # 풍향 (dgree)
    wind_wdir = weather['wind']['wdir']
    # 풍속 (m/s)
    wind_wspd = weather['wind']['wspd']

    # 하늘 상태 정보
    # 하늘상태코드명
    # - SKY_A01: 맑음
    # - SKY_A02: 구름조금
    # - SKY_A03: 구름많음
    # - SKY_A04: 구름많고 비
    # - SKY_A05: 구름많고 눈
    # - SKY_A06: 구름많고 비 또는 눈
    # - SKY_A07: 흐림
    # - SKY_A08: 흐리고 비
    # - SKY_A09: 흐리고 눈
    # - SKY_A10:  흐리고 비 또는 눈
    # - SKY_A11: 흐리고 낙뢰
    # - SKY_A12: 뇌우, 비
    # - SKY_A13: 뇌우, 눈
    # - SKY_A14: 뇌우, 비 또는 눈
    sky_name = weather['sky']['name']
    # 하늘상태코드
    sky_code = weather['sky']['code']
    w = '시간별 온도 ' + temperature_tc + '도, 최고 ' + temperature_tmax + '도, 최저 ' + temperature_tmin + '도, 하늘 ' + sky_name + ', 바람 ' + wind_wspd + 'm/s, 습도' + humidity + '%'
    print(w)

#현재 날씨(분별)
def minutely(weather):
    #print(weather)
    # 상대 습도
    humidity     = weather['humidity']

    # 기압정보
    # 현지기압(Ps)
    pressure_surface  = weather['pressure']['surface']
    # 해면기압(SLP)
    pressure_seaLevel  = weather['pressure']['seaLevel']

    # 관측소
    # 관측소명
    station_name      = weather['station']['name']
    # 관측소 지점번호(stnid)
    station_id      = weather['station']['id']
    # 관측소 유형
    #- KMA: 기상청 관측소
    #- BTN: SKP 관측소
    station_type  = weather['station']['type']
    # 위도
    station_latitude  = weather['station']['latitude']
    # 경도
    station_longitude = weather['station']['longitude']

    # 기온 정보
    # 오늘의 최고기온
    temperature_tmax = weather['temperature']['tmax']
    # 1시간 현재기온
    temperature_tc = weather['temperature']['tc']
    # 오늘의 최저기온
    temperature_tmin = weather['temperature']['tmin']

    # 낙뢰유무(해당 격자 내)
    # - 0: 없음
    # - 1: 있음
    lightning = weather['lightning']

    # 강수량
    # 강수형태코드
    # - 0: 현상없음 → rain(sinceOntime) 사용
    # - 1: 비       → rain(sinceOntime) 사용
    # - 2: 비/눈 → precipitation(sinceOntime) 사용
    # - 3: 눈    → precipitation(sinceOntime) 사용
    precipitation_type = weather['precipitation']['type']
    # 1시간 누적 강수량
    # - if type=0/1/2 → 강우량 (mm)
    # - if type=3     → 적설량 (cm)
    precipitation_sinceOntime = weather['precipitation']['sinceOntime']

    # 바람정보
    # 풍향 (dgree)
    wind_wdir = weather['wind']['wdir']
    # 풍속 (m/s)
    wind_wspd = weather['wind']['wspd']

    # 하늘 상태 정보
    # 하늘상태코드명
    # - SKY_A01: 맑음
    # - SKY_A02: 구름조금
    # - SKY_A03: 구름많음
    # - SKY_A04: 구름많고 비
    # - SKY_A05: 구름많고 눈
    # - SKY_A06: 구름많고 비 또는 눈
    # - SKY_A07: 흐림
    # - SKY_A08: 흐리고 비
    # - SKY_A09: 흐리고 눈
    # - SKY_A10:  흐리고 비 또는 눈
    # - SKY_A11: 흐리고 낙뢰
    # - SKY_A12: 뇌우, 비
    # - SKY_A13: 뇌우, 눈
    # - SKY_A14: 뇌우, 비 또는 눈
    sky_name = weather['sky']['name']
    # 하늘상태코드
    sky_code = weather['sky']['code']

    # 강우정보
    # 1시간 누적 강우량
    rain_sinceOntime   = weather['rain']['sinceOntime']
    # 일 누적 강우량
    rain_sinceMidnight = weather['rain']['sinceMidnight']
    # 10분 이동누적 강우량
    rain_last10min     = weather['rain']['last10min']
    # 15분 이동누적 강우량
    rain_last15min     = weather['rain']['last15min']
    # 30분 이동누적 강우량
    rain_last30min     = weather['rain']['last30min']
    # 1시간 이동누적 강우량
    rain_last1hour     = weather['rain']['last1hour']
    # 6시간 이동누적 강우량
    rain_last6hour     = weather['rain']['last6hour']
    # 12시간 이동누적 강우량
    rain_last12hour    = weather['rain']['last12hour']
    # 24시간 이동누적 강우량
    rain_last24hour    = weather['rain']['last24hour']

    str = '분별 온도 ' + temperature_tc + ', 최고 ' + temperature_tmax + ', 최저 ' + temperature_tmin + ', 하늘 ' + sky_name + ', 바람 ' + wind_wspd + ', 습도' + humidity
    print(str)

def requestCurrentWeather(city, county, village, isHourly = True):
    params = { "version": "1",
                "city": city,
                "county": county,
                "village": village }
    if isHourly:
        print("요청")
        response = requests.get(url_hourly, params=params, headers=headers)
    else:
        response = requests.get(url_minutely, params=params, headers=headers)

    if response.status_code == 200:
        print(response.status_code)
        print("변경")
        # json을 딕셔너리로 변경 
        response_body = response.json()
        print(response.json())
       
        #날씨 정보
        try:
            print("시도")
            if isHourly:
                print("시간별")
                weather_data = response_body['weather']['hourly'][0]
            else:
                print("분별")
                weather_data = response_body['weather']['minutely'][0]

            if isHourly:
                print("시간별2")
                
                hourly(weather_data)
                
            else:
                print("분별2")
                minutely(weather_data)
        except:
            print("except")
            pass

    else:
        print("에러")
        pass
        #에러


        



client.run('(발급받은 디스코드 봇 토큰을 입력해주세요)')
