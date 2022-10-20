#install packages
import matplotlib.pylab as plt
import numpy as np
import pkmodel as pk

# setting variables and storage arrays
print('How many models do you want to run?')
no_models = input('Enter a whole number')
if isinstance(no_models, int):
    raise TypeError('Answer needs to be a whole number.')
model_input = [pk.set_model_args()] * no_models # Array storing model inputs that WILL be used in model.py
model_type = [{}] * no_models   # Array storing model inputs that WILL NOT be used in model.py

for i in range(no_models):
    model_input[i]['dose_shape'] = pk.shape_of_dosis()
    model_input[i]['dose_strength'] = pk.dosage()
    model_input[i]['dose_spikes'] = pk.number_of_spikes(model_input[i]['dose_shape'])

    model_type[i]['no_comp'] = pk.number_of_compartments()
    model_type[i]['dose_comp'] = pk.type_of_dosis()

t_eval = np.linspace(0,12,121)
sol = [None] * no_models    # a list where each element stores the output of each model run

# determining which type of model to run and running it
for model in range(no_models):
    if model_type[model]['dose_comp']:  # runs 1-comparment model with subcutaneous dosing
        y0 = np.array([0.0, 0.0, 0.0])
        sol[model] = pk.subcutaneous(t_eval, y0, model_input[model])
    elif model_type[model]['no_comp'] == 2: # runs 2-comparment model with continuous dosing
        y0 = np.array([0.0, 0.0])
        sol[model] = pk.iv_two_compartments(t_eval, y0, model_input[model])
    else:   # runs 1-comparment model with continuous dosing
        y0 = np.array([0.0])
        sol[model] = pk.iv_one_compartment(t_eval, y0, model_input[model])
    sol[model].dose = a

# plotting the solution
pk.solution(*sol)

