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
