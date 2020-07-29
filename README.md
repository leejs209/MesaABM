# MesaABM

## 모델 실행 시각화
#### 대조군
![image](대조군.gif)
#### 가설 1번
교차개학 여부
![image](가설1번.gif)
#### 가설 2번
보충 및 야자 여부
![image](가설2번.gif)
#### 가설 3번
같은 학년의 학반 사이 이동 금지
![image](가설3번.gif)
#### 가설 4번
급식 순서를 반별로
![image](가설4번.gif)
![image](sir_basic_sim.gif)

## How to visualize / 모델 실행을 시각화하는 법
1. Release의 `v1.0.zip`파일을 다운로드한다.
2. 압축 해제 후 `gui.exe`를 실행한다.
3. 인자를 설정한다.
4. "시각화" 버튼을 누른다.

## Extract Data / 데이터 추출하기
1. result 폴더를 완전히 비운다.
2. `run.py` 마직막 줄에서 `do_experiment` 함수를 실험 목적에 맞게 변형한다.
3. `run.py` 가장 하단 부분에서 `do_experiment`를 적절히 호출한다.
4. `run.py` 가장 하단 부분에 
