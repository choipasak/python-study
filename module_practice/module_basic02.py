
# 모듈 내에 존재하는 변수, 함수, 클래스 등을 직접 임포트 하는 방법
from math import factorial, gcd

print(factorial(5))
print(factorial(10))

print(gcd(12,18))

# 임포트할 모듈에 별칭을 지정하여 사용하기
import statistics as st
li = [34,35,55,12,33,88,66]

print(f'평균: {st.mean(li)}')
print(f'분산: {st.variance(li)}')
print(f'표준편차: {st.stdev(li)}')

# 위에서 알려드린 두 가지 개념을 합쳐서도 사용이 가능합니다.
from math import factorial as fac
print(fac(5))