# naive-MBA-Deobfuscator
한양대학교 컴퓨터학부 프로그래밍 시스템 연구실에서 진행한 프로잭트 입니다.

과제: Python으로 naive MBA Deobfuscator 만들기

    Python의 ast 라이브러리를 활용하여 임의의 난독화된 MBA 표현식을 받는다. ex: (((x + 3) | y) + 23)
    
      - 대수연산자 (+, -, *, /, %, Unary -), 논리연산자 (|, &, ^, <<, >>, ~) 그리고 10진수 자연수를 포함해야한다.
      
      - 모든 연산은 괄호로 감싸져 있어야한다.
      
    라는 위와 같은 조건으로 MBA 표현식을 입력으로 받아서, 이 표현식과 의미적으로 같고, AST Node 크기 기준으로 더 작거나 같은 표현식을 찾는 SyGuS 파일을 생성해주는 프로그램 구현하여라. 
    
    합성 제한 시간은 20초이여야한다.

```
예제 입력 :
python3 [hw.py](http://hw.py/) "(((x + 3) | y) + 2)"

예제 출력 :
Size of input expr : 7
SyGuS File written to : [Path]/hw.sl
[ 합성기가 시간 제한을 넘겼을 때 ]
Synthesizer Timed out.
[ 합성이 성공했을 때 ]
Synthesis Successful.
Size of deobfuscated expr : 6
```
