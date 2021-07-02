rating_file = open(r'C:\Users\jym83\Downloads\python project\result_rating', 'w', encoding='utf-8')  #파일 쓰기

for i in range(1001,5000) :
    try : 
        f = open(r'C:\Users\jym83\Downloads\python project\python_problem\problem number[' + str(i) + ']', 'r', encoding='utf-8')  #파일 열기
    
    except : 
        continue

    lines = f.readlines()  #불러온 데이터를 \n로 구분하여 리스트 형태로 반환
    f.close()

    lines = list(map(float,lines))
    lines.sort(reverse=True)  #원소들을 내림차순 정렬
    a = 1
    result = 0
    
    for k in range (0,len(lines)) :  #해당 리스트의 원소의 개수만큼 반복실행
        result += (a*lines[k])  #레이팅 계산
        a *= 0.72
    
    rating = (7/25) * result
    rating_file.write('problem_number[' + str(i) + '] : ')
    rating_file.write(str(rating))
    rating_file.write('\n')

rating_file.close() #파일 작성 종료