import time
# 정규식(regular expression) 쉽게 문자열에서 패턴에 해당하는 부분을 추출
import re
#동적크롤링(스크래핑)
from selenium import webdriver
from selenium.webdriver.common.by import By

#url연결
url = "https://www.weather.go.kr/w/index.do"
#Edge브라우저 및 get요청
browser = webdriver.Edge()
browser.get(url)

#20초동안 창을 켜둬서 내가 원하는지역검색후에 가만히 두면 크롤링됨(시간변경가능)
time.sleep(1)
#지역
area = browser.find_element(By.CSS_SELECTOR, 'a.serch-area-btn.accordionsecond-tit').text
#온도
#temperature
temp = browser.find_element(By.CSS_SELECTOR, "span.tmp").text
# temp_element = browser.find_element(By.CSS_SELECTOR, "span.tmp")
# temp_with_unit = temp_element.text
# temp_only = float(temp_with_unit.split("<small>")[0].strip())
# print(temp_only) # Output: 11.6




#최저온도
minTemp = browser.find_element(By.CSS_SELECTOR,'span.tmin').text

#최고온도
maxTemp = browser.find_element(By.CSS_SELECTOR,'span.tmax').text
#체감온도
actualTemp = browser.find_element(By.CLASS_NAME, 'chill').text.replace("체감", "").replace("(", "").replace(")", "")
#어제보다 몇도높은지 부분 스크래핑
temp_diff = browser.find_element(By.CSS_SELECTOR, '.wrap-1>.w-txt').text

#wrap-2>li>val이 3개여서 items에담음
items = browser.find_elements(By.CSS_SELECTOR, '.wrap-2.no-underline li')

#습도
humidity_str = items[0].find_element(By.CLASS_NAME, 'val').text
humidity = float(re.findall('\d+', humidity_str)[0])

#바람
wind_str = items[1].find_element(By.CLASS_NAME, 'val').text
wind = float(re.findall('\d+', wind_str)[0])

#강수량
rainfall_str = items[2].find_element(By.CLASS_NAME, 'val').text
rainfall = float(re.findall('\d+', rainfall_str)[0])

#초미세먼지
ultraDust = int(browser.find_element(By.CSS_SELECTOR, 'span.air-lvv').get_attribute('textContent'))
#미세먼지
dust =  float(browser.find_element(By.CSS_SELECTOR, 'span.air-lvv-wrap.air-lvv-2 span.air-lvv').get_attribute('textContent'))

# 온도를 실수형으로 전환
temp = float(temp[:-1])


# 현재 온도 정보에 따른 출력
def fTemp() :
  if temp > 30:
    print("오늘은 매우 더워요! 더위 조심하세요.")
  elif temp > 25:
    print("오늘은 더운 날씨예요. 물 많이 마시고 적당히 움직이세요.")
  elif temp > 20:
    print("오늘은 날씨가 쾌적해요. 산책하기 좋은 날씨네요.")
  else:
    print("오늘은 날씨가 조금 쌀쌀해요. 따뜻하게 입고 다니세요.")
    
# 현재 습도 정보에 따른 출력
def fhumidity() :
  if humidity >= 30 and humidity <= 60:
    print("습도가 적정합니다.")
  elif humidity < 30:
    print("습도가 너무 낮습니다. 가습기를 사용하는 것이 좋습니다.")
  elif humidity > 60:
    print("습도가 너무 높습니다. 제습기를 사용하는 것이 좋습니다.")
  else :
    print("자료없음")

# 현재 바람 정보에 따른 출력
def fwind() :
  if wind < 0.3 :
    print("이정도면 바람이 안부네요!")
  elif wind >= 0.3 and wind <= 1.5 :
    print("실바람이 불어요!")
  elif wind >= 1.6 and wind <= 3.3 :
    print("남실바람이 불어요!")
  elif wind >= 3.4 and wind <= 5.4 :
    print("산들바람이 불어요!")
  else :
    print("바람이 강하니 외출을 자제해주세요!")
    
# 현재 강수량 정보에 따른 출력
def frainfall() :
    if rainfall == 0 :
      print("오늘은 비가 안와요!")
    elif rainfall < 3.0:
      print("약한 비가 와요!")
    elif rainfall >= 3.0 and rainfall < 15.0:
      print("적당한 비가 내려요!")
    elif rainfall >= 15.0 :
      print("강한 비가 내리니 외출을 자제하세요!")
    elif rainfall >= 30.0 :
      print("매우 강한 비가 내리니 외출하지마세요!")
      
# 현재 초미세먼지 정보에 따른 출력
def fUltra() : 
  if ultraDust >= 0 :
    print("좋음")
  elif ultraDust >=16 :
    print("보통")
  elif ultraDust >= 36 :
    print("나쁨")
  elif ultraDust >= 76 :
    print("매우 나쁨")
  else :
    print("자료없음")
  
# 현재 미세먼지 정보에 따라 출력
def fDust() :
  if dust >= 0 :
    print("좋음")
  elif dust >= 31 :
    print("보통")
  elif dust >= 81 :
    print("나쁨")
  elif dust >= 151 :
    print("매우나쁨")
  else :
    print("자료없음")
    
#출력
print(f"선택지역:{area}")
print(f"온도:{temp}", end=' / ')
fTemp()
print(f"{maxTemp}")
print(f"{minTemp}")
print(f"체감온도:{actualTemp}")
print(f"{temp_diff}")
print(f"습도: {humidity} %", end=' / ')
fhumidity()
print(f"바람: {wind} m/s", end=' / ')
fwind()
print(f"강수량: {rainfall} mm", end=' / ')
frainfall()
print(f"초미세먼지:{ultraDust}㎍/m³", end=' / ')
fUltra()
print(f"미세먼지:{dust}ppm³", end=' / ')
fDust()

browser.quit()

"""
<ul>
  <li>
  <strong class="air-level val">
    <span class="air-lvv-wrap air-lvv-2">
      <small class="air-lvv">31</span>
      <small class="unit">m3</small>
  </strong>
  </li>
<ul/>
"""

"""
<div class="serch-area accordionsecond-wrap acco-on">
<a href="#" class="serch-area-btn accordionsecond-tit on" data-role="bookmark-selected" title="펼쳐짐" data-wide-code="4600000000" data-wide-name="전남" data-city-code="4682000000" data-city-name="해남군" data-dong-code="4682034000" data-dong-name="송지면" data-x="53" data-y="55" data-lat="34.2972777904718" data-lon="126.525759259436">전남 해남군 송지면</a>
  <div class="accordionsecond-con serch-con" style="display: block;">
      <div>
        <ul data-role="bookmark-holder"></ul>
      </div>
  </div>
</div>
"""