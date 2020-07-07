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
1. Install [Python](https://www.python.org/downloads/) if you haven't yet.
2. Download this repository, and unzip it.
3. (Optional) Create a virtual environment in the `MesaABM` folder(directory) using [`venv`](https://docs.python.org/3/library/venv.html), and activate the environment.
4. Run `pip3 install -r requirements.txt` in Command Prompt(Windows) or Terminal(MacOS/Linux).
5. Run `python3 visualize.py`.

## Extract Data / 데이터 추출하기
1. result 폴더를 완전히 비운다.
2. `run.py` 마직막 줄에서 do_experiment 함수를 목적에 따라 변형한 후 아래에서 호출한다.
3. 
