import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram  # python-telegram-bot 라이브러리
import asyncio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Chrome 웹 드라이버 경로 설정
webdriver_path = 'C:\\Users\\gee\\Desktop\\study\\chromedriver\\chromedriver.exe'

# Chrome 웹 드라이버 서비스 생성
service = Service(webdriver_path)

# Chrome 옵션 설정
options = Options()
options.add_argument('--headless')  # GUI 없이 실행하려면 주석 처리
options.add_argument('--disable-gpu')  # GPU 가속 비활성화

# Chrome 드라이버 생성
driver = webdriver.Chrome(service=service, options=options)

# 웹 페이지 로드
url = "https://www.bac.or.kr/product/ko/performance/252714?q=MWJhNmY3NmRjZTVlNDdmM2JiOTZlZTRkZjVhYjFiYzE%3d#none"
driver.get(url)

wait = WebDriverWait(driver, 10)  # 최대 10초까지 대기
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".remain_seat_wrap > div")))

# 정보 가져오기
elements = driver.find_elements(By.CSS_SELECTOR, ".remain_seat_wrap > div")
result = []
for element in elements:
    print(element.get_attribute('textContent'))
    text = element.get_attribute('textContent')
    result.append(text)

# 드라이버 종료
driver.quit()

file_path = os.path.join(BASE_DIR, 'result.txt')
with open(file_path, 'w', encoding='utf-8') as f:
    for text in result:
        f.write(text + '\n')

# 텔레그램 봇 설정
bot_token = '5880381166:AAE9WRUfRZ-UcRm85NdPOLh12ipEVccKCMg'  # 텔레그램 봇 토큰
chat_id = '-886537632'  # 채팅 ID
bot = telegram.Bot(token=bot_token)

# 이전 결과 파일 읽기
prev_file_path = os.path.join(BASE_DIR, 'prev_result.txt')
prev_result = []
if os.path.exists(prev_file_path):
    with open(prev_file_path, 'r', encoding='utf-8') as f:
        prev_result = f.read().splitlines()

# 이전 결과와 현재 결과 비교
is_same_result = False
if prev_result:
    with open(file_path, 'r', encoding='utf-8') as f:
        current_result = f.read().splitlines()
    if current_result == prev_result:
        is_same_result = True

if not is_same_result:
    async def send_telegram_message():
        # 메시지 보내기
        message = '아마도 조수미 공연 취소표가 생긴 것 같으니 소연이를 위해 어서 예매하러 가보자!\nhttps://www.bac.or.kr/product/ko/performance/252714?q=MWJhNmY3NmRjZTVlNDdmM2JiOTZlZTRkZjVhYjFiYzE%3d#none\n\n'
        for text in result:
            message += text + '\n'
        print("Send the message")
        await bot.send_message(chat_id=chat_id, text=message)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_telegram_message())

# 현재 결과 저장
with open(prev_file_path, 'w', encoding='utf-8') as f:
    for text in result:
        f.write(text + '\n')

print("complete")
