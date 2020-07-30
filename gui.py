import PySimpleGUI as sg
from mesa.visualization.ModularVisualization import ModularServer
from MesaABM.model import SchoolModel
from MesaABM.visualization import grid, s_chart
import asyncio

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
layout += [[sg.Text(a), sg.InputText(str(b), key=a)] for a, b in parameter_list]
layout += [[sg.Button('시각화', bind_return_key=True), sg.Button('닫기')]]
layout += [[sg.Text("데이터 추출하기")]]
layout += [[sg.Text("가설 이름"), sg.InputText("가설 1번", key="hypothesis_name")]]
layout += [[sg.InputText('3', key="run_repeat_no"), sg.Text("회 반복하기")]]
# layout += [[sg.Output(size=(50, 10))]]

window = sg.Window('Python을 이용한 감염병 시뮬레이션', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == '취소':
        break

    if event == '시각화':
        values.pop("hypothesis_name")
        values.pop("run_repeat_no")
        for x in values.keys():
            if values[x] == 'True' or values[x] == 'False':
                values[x] = bool(values[x])
            else:
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
