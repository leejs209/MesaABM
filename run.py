import MesaABM.model as model

my_model = model.SchoolModel(100, 14, 100, 100)

for _ in range(10):
    my_model.step()