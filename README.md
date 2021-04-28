# compiler
📠 2021-1 Compiler
## 과제 1: DFA Implementation

<details>
  <summary>요구 사항</summary>

  ### Hardwired method
  <img src="https://github.com/coding-Benny/compiler/blob/main/DFA/images/state-transition-diagram.png" alt="state-transition-diagram.png" width="400" height="150">

  ### Table-driven method
  <img src="https://github.com/coding-Benny/compiler/blob/main/DFA/images/state-transition-table.PNG" alt="state-transition-diagram.png" width="300" height="200">

  DFA를 Hardwired method와 Table-driven method로 구현하고 다음 2가지 상황을 테스트 하라.
  - <img src="https://latex.codecogs.com/gif.latex?\delta&space;(p,&space;1001)=\delta&space;(p,&space;001)=\delta&space;(q,&space;01)=\delta&space;(r,&space;1)=r\in&space;F" title="\delta (p, 1001)=\delta (p, 001)=\delta (q, 01)=\delta (r, 1)=r\in F" />
  - <img src="https://latex.codecogs.com/gif.latex?\delta&space;(p,&space;0110)=\delta&space;(p,&space;110)=\delta&space;(q,&space;10)=q\notin&space;F" title="\delta (p, 0110)=\delta (p, 110)=\delta (q, 10)=q\notin F" />
</details>
<details>
  <summary>실행 화면</summary>
  
  ### Hardwired method
  <img src="https://github.com/coding-Benny/compiler/blob/main/DFA/images/hardwired-dfa.PNG" alt="hardwired-dfa" width="600" height="200">
  
  ### Table-driven method
  <img src="https://github.com/coding-Benny/compiler/blob/main/DFA/images/table-driven-dfa.PNG" alt="table-driven-dfa" width="600" height="200">
</details>

## 과제 2: Lexical Analyzer
<details>
  <summary>요구 사항</summary>
  정의한 special form token과 general form token이 포함된 sample program을 작성하여 구현한 어휘 분석기를 실행하기
  <ul>
    <li>Sample program은 negative example도 포함하도록 하여 error를 출력하는 것을 확인할 수 있어야 함</li>
    <li>데모를 통해 token이 올바르게 인식되었음을 쉽게 확인할 수 있도록 하고, 인식 과정에서 생성한 symbol table과 literal table을 보여주어야 함</li>
    <li>처리 항목 - <b>Bold</b>: required, <i>Italic</i>: optional</li>
    <ul>
      <li>Special form tokens</li>
      <ul>
        <li><b>Keywords</b></li>
        <li><b>Special symbols</b></li>
      </ul>
      <li>General form tokens</li>
      <ul>
        <li><b>Identifier</b></li>
        <li>Literal/Constants</li>
        <ul>
          <li><b>Number</b></li>
          <ul>
            <li><b>Decimal</b>
            <li><i>Octal</i>
            <li><i>Hexdecimal</i>
          </ul>
          <li><i>String</i></li>
        </ul>
      </ul>
    </ul>
  </ul>
</details>
<details>
  <summary>실행 방법 및 화면</summary>
  <ul>
    <li>How to run this program
    
    LexicalAnalyzer.exe <input-file> <output-file>
   </li>
    <li>Sample program: input-file.py

    def foo(count):
      res = 0
      for i in range(1, count + 1):
          res += i
      print("{} times completed".format(count))
      return res
      
    # This is comment. ← Because # is not defined, it will cause error!
      foo(5)
  </li>
  <li>Analysis result: output-file.txt
  
    ==========================[ Token Table ]==========================
    (21, -) (Token.SPACE, -) (Token.ID, 1) (Token.LPAREN, -) (Token.ID, 2) (Token.RPAREN, -) (Token.COLON, -) (Token.NEWLINE, -)
    (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (Token.ID, 3) (Token.SPACE, -) (Token.ASSIGNMENT2, -) (Token.SPACE, -) (Token.ZERO, -)(Token.NEWLINE, -)
    (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (17, -) (Token.SPACE, -) (Token.ID, 4) (Token.SPACE, -) (8, -) (Token.SPACE, -)(Token.ID, 5) (Token.LPAREN, -) (Token.DECIMAL, -) (Token.COMMA, -) (Token.SPACE, -) (Token.ID, 2) (Token.SPACE, -) (Token.PLUS, -) (Token.SPACE, -)(Token.DECIMAL, -) (Token.RPAREN, -) (Token.COLON, -) (Token.NEWLINE, -)
    (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (Token.ID, 3) (Token.SPACE, -) (Token.ADD_ASSIGNMENT, -) (Token.SPACE, -) (Token.ID, 4) (Token.NEWLINE, -)
    (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (Token.ID, 6) (Token.LPAREN, -) (Token.STRING2, -) (Token.PERIOD, -) (Token.ID, 7) (Token.LPAREN, -) (Token.ID, 2) (Token.RPAREN, -) (Token.RPAREN, -) (Token.NEWLINE, -)
    (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (Token.SPACE, -) (14, -) (Token.SPACE, -) (Token.ID, 3) (Token.NEWLINE, -)
    (Token.NEWLINE, -)
    
    !!! Error occurred because of the symbol # !!!
    
    ==========================[ Symbol Table ]=========================
    (1) foo
    (2) count
    (3) res
    (4) i
    (5) range
    (6) print
    (7) format
    
    =========================[ Literal Table ]=========================
    (1) 0
    (2) 1
    (3) "{} times completed"
  <img src="https://github.com/coding-Benny/compiler/blob/main/LexicalAnalyzer/images/output.png" alt="Analysis Result">
  </li>
  <li>Run Lexical Analyzer in command line
    <img src="https://github.com/coding-Benny/compiler/blob/main/LexicalAnalyzer/images/cmd.png" alt="Run Lexical Analyzer in command line">
  </li>
  </ul>
</details>
