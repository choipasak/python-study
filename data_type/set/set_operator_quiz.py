
'''
- 서로 다른 정수가 담긴 두 개의 리스트를 비교하여
li 안에 있는 정수가 li2에도 담겨 있다면 그 정수를 배제하시고
서로 겹치지 않는 정수만 담긴 새로운 리스트를 생성해 보세요.
'''
li = [1, 2, 3, 4, 5, 6, 7]
li2 = [1, 3, 8, 4, 5, 7, 101]


li = set(li)
li2 = set(li2)
# print(li, li2)
print('='*40)
print(list(sorted(li - li2 | li2 - li)))
# print(li2 - li)

# li = (li - li2)
# print(li)
# li2 = (li2 - li)
# print('='*40)
# print(sorted(li | li2))
# print(li2)
# print(li, li2)
# print((li - li2) | (li2 - li))



# print(input(li2-li))

# 선생님 버전
print(list(set(li)))