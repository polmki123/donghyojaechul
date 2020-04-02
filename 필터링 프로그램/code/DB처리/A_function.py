
class A_beta():
  def __init__(X):
    self.a = 10

  # def a_get():
  #   return self.a

  def _a_set( X, input):
    self.a = input
    print(A_beta.a)

def a_get():
  return A_beta.a

def _Pirntall():
  print("coca")

if __name__ == '__main__' :
  print('hello 모듈 시작')
  print('hello.py __name__:', __name__)    # __name__ 변수 출력
  print('hello 모듈 끝')