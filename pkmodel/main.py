#install packages
import matplotlib.pylab as plt
import numpy as np
import pkmodel as pk

# setting variables and storage arrays
print('How many models do you want to run?')
no_models = int(input('Enter a whole number: '))

if not isinstance(no_models, int):
    raise TypeError('Answer needs to be a whole number.')
m_input = [pk.set_model_args()] * no_models # Array storing model inputs that WILL be used in model.py
m_type = [{}] * no_models   # Array storing model inputs that WILL NOT be used in model.py

for i in range(no_models):
    m_input[i]['dose_shape'] = pk.shape_of_dosis()
    m_input[i]['dose_strength'] = pk.dosage()
    m_input[i]['dose_spikes'] = pk.number_of_spikes(m_input[i]['dose_shape'])

    m_type[i]['no_comp'] = pk.number_of_compartments()
    m_type[i]['dose_comp'] = pk.type_of_dosis()

t_eval = np.linspace(0,12,121)
sol = [None] * no_models    # a list where each element stores the output of each model run

# determining which type of model to run and running it
for m in range(no_models):
    if m_type[m]['dose_comp']:  # runs 1-comparment m with subcutaneous dosing
        y0 = np.array([0.0, 0.0, 0.0])
        sol[m] = pk.subcutaneous(t_eval, y0, m_input[m])
    elif m_type[m]['no_comp'] == 2: # runs 2-comparment model with continuous dosing
        y0 = np.array([0.0, 0.0])
        sol[m] = pk.iv_two_compartments(t_eval, y0, m_input[m])
    else:   # runs 1-comparment model with continuous dosing
        y0 = np.array([0.0])
        sol[m] = pk.iv_one_compartment(t_eval, y0, m_input[m])
    
    dose_func = pk.create_dosis_function(m_input[m]['dose_shape'],
                                    m_input[m]['dose_spikes'],
                                    m_input[m]['dose_strength'])
    sol[m].dose = []
    for t in t_eval:
        sol[m].dose.append(dose_func(t))
    
    sol[m].name = 'model '+str(m)

# plotting the solution
pk.solution(*sol)

