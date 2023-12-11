
'''
* 표준 입력함수 input()

- 함수 괄호 안에 사용자에게 질문할 내용을 문자열 형태로
작성합니다.

- input()과 함께 항상 변수를 선언해서 입력값을 받아주셔야 하며
입력받은 데이터의 타입은 str로 리턴됩니다.
'''

nick = input('너 별명이 뭐야?')
print('내 별명은 ' + nick + ' 입니다.') # 결과: 너 별명이 뭐야?python -u "c:\MyWork\pyhthon-study\basic\input_ex.py"

print('==================================================')

# 입력값이 만약 정수, 실수라면
# input 함수 자체를 int(), float()함수로 감싸주시면 됩니다. -> 파이썬의 내장함수들임
# input 함수의 리턴값이 문자열이라고 했으니까, 변환해서 대입하면 끝.

price = int(input('음식의 가격: '))
people = int(input('사람 수: '))

print('지불 할 가격: ' , price * people , '원') # 결과: ERROR -> TypeError: can't multiply sequence by non-int of type 'str' : 왜 문자열끼리 곱하냐
