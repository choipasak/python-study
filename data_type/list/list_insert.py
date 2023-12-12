
'''
* 리스트에 데이터를 추가하는 메서드

1. append(): 요소를 리스트의 맨 마지막에 추가.
2. insert(): 요소를 리스트의 특정 위치에 삽입.
'''

nums = [1,3,5,7]
nums.append(9) # 추가
print(nums)

nums.append('뵤뵤뵹')
print(nums)

# insert(index, value)
nums.insert(3, 4)
print(nums)

'''
* 리스트의 탐색과 정렬

1. index(): 리스트에서 특정 값이 저장된 인덱스를 반환.
2. count(): 리스트 내부에 저장된 특정 요소의 개수를 반환.
3. sort(): 리스트를 오름차 정렬.
4. reverse(): 리스트 데이터를 역순으로 배치
'''

points = [100, 55, 65, 73, 55, 12, 35, 46, 89, 98, 100, 46, 100]
perfect = points.count(100)
print(f'만점자는 {perfect}명 입니다.')
print(f'89점을 획득한 학생은 {points.index(89) + 1}명 입니다.')

# 내장함수 len(), max(), min()
print(f'학생 수는 {len(points)}명 입니다.')
print(f'학생 수는 {max(points)}명 입니다.')
print(f'학생 수는 {min(points)}명 입니다.')

# 오름차 정렬 sort()
print('=' * 40)
print(points)
points.sort(reverse=True)
# points.reverse() # reverse() -> 정렬이 아니라 단순 역순 배치

print(points)

# 리스트 내의 요소의 단순 존재 유무를 검사하려면 in 키워드를 사용합니다.
food_menu = ['참치마요김밥', '닭강정', '계란말이', '라면']
name = input('음식명을 입력하세요: ')

if name in food_menu:
    print(f'{name} 음식이 주문되었습니다.')
else:
    print(f'{name}은(는) 없는 음식입니다.')
