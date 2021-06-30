from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.webdriver import WebDriver 
chromedriver = r'C:\Users\jym83\Downloads\python project\chromedriver'
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
#options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headlss chrome 옵션 적용   일단 코드 실행확인할때까지는 비활성화
options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR')    # 언어 설정

def stx_t(TL) : #형식에서 시간제한:, 메모리 제한:과 같은 단어 제외하고 sec 앞에 숫자만 추출
    TL = str(TL)
    TL = TL.replace("시간 제한: ","")
    TL = TL.replace("메모리 제한: ","")
    TL = TL.replace("Sec","")
    TL = TL.replace(" MB","")
    TL = TL.replace("  ","")
    TL = int(TL.split()[0])
    return TL


def rating_R(T,L) :  #성과
    T /= 1000
    R = (1-T/L)**2 
    return R


def rating_D(C,S) :  #난이도
    C = str(C)
    S = str(S)
    C = int(C.replace(",",""))
    S = int(S.replace(",",""))
    D = 9*(1 - ((C/(S+1)) ** 2) ) #(1-A)더해야하는데 일단 생략
    return D


def Rating(R,D) :  #레이팅
    Rk = R + D
    return Rk


def crawling(url) :  #크롤링 드라이버를 열어주는 함수
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def page() : #html만 가져오는 함수
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def check_num (problem_number) :  #데이터 저장이 끝난 문제를 확인하는 함수 endproblem파일은 사전에 미리 만들어두어야 함.
    ef = open(r'C:\Users\jym83\Downloads\python project\end_problem', 'r+', encoding='utf-8') 
    lines = ef.readlines()  #불러온 데이터를 \n로 구분하여 리스트 형태로 반환
    ef.close()
    for l in lines : 
        l = str(l)
        l = l.replace('\n',"")  #개행문자 제거
        if l == problem_number :
            print("이미 데이터가 수집된 문제입니다.")
            return True
    return False


def write_file(problem_number) :  #데이터 저장이 완료된 문제를 저장하는 함수
        ef = open(r'C:\Users\jym83\Downloads\python project\end_problem', 'a', encoding='utf-8') 
        ef.write(problem_number)  #데이터 저장이 완료된 문제이름 저장
        ef.write('\n')
        ef.close()
        print(problem_number + '번 파일 작성 완료!\n')


driver = webdriver.Chrome(chromedriver, options=options) #드라이버 생성
driver.get('https://codeup.kr/loginpage.php') #크롤링할 사이트 호출, 로그인 페이지

driver.implicitly_wait(3)

login_x_path='/html/body/div[2]/form/input'
driver.find_element_by_name('user_id').send_keys('jym8391')
driver.find_element_by_name('password').send_keys('ym120100@')
driver.find_element_by_xpath(login_x_path).click()

time.sleep(1)


for i in range(19,0,-1) :

    problem_set_url = 'https://codeup.kr/problemset.php?page=' + str(i)  #1~19페이지 반복
    problem_set_table = crawling(problem_set_url).find('table',{'id':'problemset'})
    problem_set_tr = problem_set_table.find_all('tr')

    for problem_set_t in problem_set_tr :  #한페이지당 한문제씩

        problem_set_td = problem_set_t.find_all('td')

        if len(problem_set_td) > 0 : 

            problem_number = str(problem_set_td[1].text)  #문제 번호

            if check_num(problem_number) :  #이미 데이터 수집이 완료된 문제라면, 스킵
                continue

            problem_name = str(problem_set_td[2].find("a").text)  #문제 이름
            problem_set_pass = problem_set_td[4].find("a").text  #정답자 수
            
            if int(str(problem_set_pass).replace(',',"")) == 0 :  #정답자가 0명인 경우 
                write_file(problem_number) 
                continue 

            problem_set_submit = problem_set_td[5].find("a").text  #제출자 수

            problem_D = rating_D(problem_set_pass, problem_set_submit)  #문제 난이도

            problem_limit_url = "https://codeup.kr/" + problem_set_td[2].find("a")["href"] #문제 링크
            
            try :
                problem_set_timememory = crawling(problem_limit_url).find('div',{'class':'text-center'}).text  #시간제한과 메모리 제한, 만약 문제를 열 수 없다면 여기서 문제
            
            except : 
                write_file(problem_number)  #존재하지 않는 페이지도 한 번 거쳤다면 파일에 저장해놓고 방문하지 않음
                continue

            problem_L = stx_t(problem_set_timememory) #시간제한만 따로 분리
            
            f = open(r'C:\Users\jym83\Downloads\python project\python_problem\problem number[' + problem_number + ']', 'w', encoding='utf-8')  #해당 문제의 레이팅 저장하는 파일 생성

            problem_url = "https://codeup.kr/" + problem_set_td[4].find("a")["href"]  #원하는 문제 정답자 링크로 접근, 처음 이동할 때
            driver.get(problem_url)
            
            pre_submitnumber = "제출번호중복화인"
            pre_url = "링크중복확인"
            t = True
            while t : #한 문제당 정답자 페이지를 계속 이동
                user_table = page().find('table',{'id':'result-tab'})  
                user_tr = user_table.find_all('tr')

                for user_t in user_tr : #유저별 정보
                    user_td = user_t.find_all('td')

                    if len(user_td) > 0 : 

                        if str(driver.current_url) != pre_url : 
                            pre_url = str(driver.current_url)  #url 중복 확인, 중복이면 해당 문제 페이지 반복 종료

                            if pre_submitnumber != str(user_td[0].text) : #제출 번호 중복 확인, 중복이면 기록하지 않음
                                pre_submitnumber = str(user_td[0].text)
                                user_language = str(user_td[6].text)  #유저가 사용하는 언어

                                if user_language == "C" or user_language == "C++" :  #사용언어가 C,C++일 경우에만 레이팅에 필요한 정보 수집 

                                    user_time = int(str(user_td[5].text))  #유저가 실행한 시간
                                    user_R = rating_R(user_time, problem_L)  #유저의 성과
                                    user_Rating = Rating(user_R, problem_D)  #유저의 각 제출 
                                    
                                    f.write(str(user_Rating)) #파일 작성
                                    f.write('\n') 
                                    """user_url = "https://codeup.kr/" + user_td[1].find("a")["href"]#사용자 정보 링크로 접근
                                    driver.get(user_url)"""  # 유저 링크로 접속하는 부분인데 레이팅 계산에는 당장 필요하진 않으니깐 제외함.

                        else :  #url이 중복일 경우
                            t = False
                            print("중복이므로 해당 페이지를 종료합니다.")
                            break
                        
                    if t : 
                        Next_x_path = "/html/body/main/div/ul/li[3]/a"  #다음페이지 링크
                        driver.find_element_by_xpath(Next_x_path).click()  #다음페이지로 이동
                        time.sleep(1)

            f.close() #한문제에 있는 파일 작성 종료

            write_file(problem_number)  #데이터 저장이 완료된 문제이름을 저장
                
            
    
                
time.sleep(10000)
#driver.quit() #크롬 브라우저 닫기'''
#http://koistudy.net/?mid=rating