import PySimpleGUI as sg
from mesa.visualization.ModularVisualization import ModularServer
from MesaABM.model import SchoolModel
from MesaABM.visualization import grid, s_chart
import asyncio
import datetime
import os
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

timetable_normal = [
    'recess',
    'recess_cont',
    'recess',
    'recess_cont',
    'recess',
    'recess_cont',
    'recess',
    'recess_cont',
    'recess',
    'recess_cont',
    'recess',
    'recess_cont',
    'meal',
    'meal_cont',
    'meal_cont',
    'recess',
    'recess_cont',
    'recess_cont',
    'recess_cont',
    'recess_cont',
    'recess_cont',
    'recess',
    'recess_cont',
    'recess',
    'recess_cont'
]

timetable_extra = timetable_normal + [
    'recess',
    'recess_cont',
    'recess',
    'recess_cont',
    'dinner',
    'dinner_cont',
    'dinner_cont',
    'recess',
    'recess_cont',
    'recess_cont',
    'recess_cont',
    'recess_cont',
    'recess_cont',
    'recess_cont'
]


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Windows 서버 실행오류 해결

sg.theme('LightGrey1')
parameter_list = [('N', 1050), ('N_per_group', 25), ('width', 140), ('height', 61), ('initial_num_infected', 1),
                  ('infection_duration', 7), ('exposed_duration', 5),
                  ('infection_prob_per_contact', 0.2), ('exposed_infection_prob_per_contact', 0.05),
                  ('restaurant_multiplier', 3), ('visit_prob_per_person', 0.1),
                  ('meal_random', True), ('meal_distanced', False), ('dinner_percentage', 0.3),
                  ('timetable', True), ('split_opening', False)
                  ]

layout = [[sg.Text('변인설정', text_color='blue')]]
layout += [[sg.Text(a), sg.InputText(str(b), key=a)] for a, b in parameter_list if type(b) != bool]
layout += [[sg.Text(a), sg.Checkbox('', key=a, default=b)] for a, b in parameter_list if type(b) == bool]
layout += [[sg.VerticalSeparator()]]
layout += [[sg.Button('시각화'), sg.Button('닫기')]]
layout += [[sg.Text("데이터 추출하기", text_color="blue")]]
layout += [[sg.Text("저장 폴더"), sg.InputText(key="save_dir"), sg.FolderBrowse("찾아보기..", target="save_dir", key="save_dir_btn")]]
layout += [[sg.Text("가설 이름"), sg.InputText("", key="hypothesis_name")]]
layout += [[sg.InputText('3', key="run_repeat_no"), sg.Text("회 반복하기"), sg.Button("시작", key="extract_data")]]
layout += [[sg.Output(size=(80, 10))]]
window = sg.Window('Python을 이용한 감염병 시뮬레이션', layout)

while True:
    event, read_values = window.read()

    if event == sg.WIN_CLOSED or event == '취소':
        break
    elif event == '시각화':

        values = read_values
        values.pop("hypothesis_name")
        values.pop("run_repeat_no")
        values.pop("save_dir")
        values.pop("save_dir_btn")
        for x in values.keys():
            if type(values[x]) != bool:
                try:
                    values[x] = int(values[x])
                except ValueError:
                    values[x] = float(values[x])
        values['timetable'] = timetable_extra if values['timetable'] else timetable_normal

        print("인자:", values)
        server = ModularServer(SchoolModel, [grid, s_chart], "감염병 모델 시각화", values)

        server.port = 8081

        window.close()
        server.launch()

    elif event == "extract_data":
        print("데이터 추출 시작")
        values = read_values
        RESULT_DIR = values["save_dir"] + "/"
        EXPERIMENT_NAME = values["hypothesis_name"]
        repeat_no = values["run_repeat_no"]

        values.pop("hypothesis_name")
        values.pop("run_repeat_no")
        values.pop("save_dir")
        values.pop("save_dir_btn")
        for x in values.keys():
            if type(values[x]) != bool:
                try:
                    values[x] = int(values[x])
                except ValueError:
                    values[x] = float(values[x])
        values['timetable'] = timetable_extra if values['timetable'] else timetable_normal

        for x in range(int(repeat_no)):
            model = SchoolModel(**values)
            datetime_string = str(datetime.datetime.now().strftime('%m-%d %H-%M-%S'))
            start = time.time()  # 모델 실행에 걸리는 시간을 측정한다.
            model.step()
            while model.i_count != 0 or model.e_count != 0:  # 감염자 또는 잠복기가 0명이 될 때까지 측정한다.
                model.step()
                if model.step_no % 100 == 0:
                    window.refresh()

            result = model.datacollector.get_model_vars_dataframe()
            result.plot()

            # png로 저장
            plt.savefig(RESULT_DIR + EXPERIMENT_NAME + datetime_string + '.png', bbox_inches='tight')
            plt.close()

            # csv 출력 폴더 만들기
            if not os.path.exists(RESULT_DIR + 'csv'):
                os.mkdir(RESULT_DIR + 'csv')
            if not os.path.exists(RESULT_DIR + 'csv/' + EXPERIMENT_NAME):
                os.mkdir(RESULT_DIR + 'csv/' + EXPERIMENT_NAME)

            # csv 파일로 실험 결과를 출력한다.
            result.to_csv(RESULT_DIR + 'csv/' + EXPERIMENT_NAME + '/' + EXPERIMENT_NAME + datetime_string + '.csv')

            # 소요 시간 출력
            end = time.time()
            print("[" + str(x + 1) + "] " + str(end - start) + '초 소요됨')

            window.refresh()
    print("지정된 폴더로 추출 완료.")