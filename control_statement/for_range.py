
'''
* 내장함수 range()

- 순차적으로 증가하는 정수의 순차적 자료형을 만들 때
대괄호 안에 데이터들을 콤마로 일일히 나열하는 것은
한계가 있기 때문에, range()함수를 통해 보다 쉽게
순차형 반복 범위를 지정할 수 있습니다.

ex) range(begin, end, step)
- begin은 값이 포함되지만(이상), end는 값이 포함되지 않습니다. (미만)
- 범위가 이상 미만이다!
'''

list1 = [1,2,3,4,5,6,7,8,9,10]
print(list1)

print('=' * 40)

list2 = list(range(1, 11, 1))
print(list2)

print('=' * 40)

# step 생략 -> 자동으로 1로 처리
list3 = list(range(4, 15))
print(list3)

print('=' * 40)

# range 함수 괄호 안에 값을 1개만 주면 end의 값으로 처리하고
# begin의 값을 자동으로 0으로 처리합니다. 
# 그래서 인덱스 잡고 싶을 때 자주 사용하는 방법이다!
list4 = list(range(5)) # range(0,5,1) -> [0,1,2,3,4]
print(list4)

print('=' * 40)

# 1 ~ 100까지의 누적합
total = 0
for n in range(1, 101):
    total += n

print('1~100까지의 누적합: ', total)