# from logging import raiseExceptions
# from typing import Type
import numpy as np


def type_of_dosis():
    """Function to ask for type of dosis: should a dosis compartment be used?

    Inputs
    -------
    None

    Outputs
    --------
    no_comps: int, number of compartments
    dosis_comp: bool, is a dosis compartment used?
    """

    print('Should a dosis compartment be used?')
    answer = input('y/n?')
    if answer not in ['y', 'n']:
        raise TypeError('Answer needs to be y or n.')
    dosis_comp = (answer == 'y')  # convert input into boolean,
    return dosis_comp


def number_of_compartments():
    """Function asks for user input on how many compartments there should be
    including the central compartment. Not counting the dosis compartment

    Input
    -----
    None

    Output
    ------
    no_comps: int, number of compartments
    """

    print('How many compartments including the central one should there be?')
    no_comps = int(input('Enter an integer between 1 and 3'))
    if (type(no_comps) != int) or (no_comps < 1) or (no_comps > 3):
        raise TypeError('Input needs to be an integer between 1 and 3.')

    return no_comps

def shape_of_dosis():
    """Function in which the user can set whether the dose is given in one spike
    or as a continuous dosis

    Input
    -----
    None

    Output
    ------
    shape: bool, True for spikes, False for continuous
    """
    print('Should a contnuous dosis be used?')
    answer = input('y/n?')
    if answer == 'y':
        shape = 1
    elif answer == 'n':
        shape = 0
    else:
        raise TypeError('Answer needs to be either y or n.')
    return shape


def number_of_spikes(shape):
    """Function asks users for input on how many spikes there
    should be if using a spiked dosage

    Input
    -----
    shape: bool, see shape_of_dosis()

    Output
    ------
    no_spikes: int, number of spikes in dosis
    """
    print('How many spikes should there be in the dosage?')
    no_spikes = int(input('Enter an integer between 1 and 10.'))
    return no_spikes


def dosage():
    """Function asks users for input on the amount of the dosis.

    Input
    -----
    None

    Output
    ------
    dose: float, dose in ng
    """
    print('What should the amount of dosis be in ng?')
    dose = float(input('Type a number larger than 0.'))
    return dose


def create_dosis_function(t, shape, no_spikes, strength):
    """Function takes inputs about dosis and creates an array
    for the dose in time

    Input
    -----
    t: array, time steps
    shape: bool, whether we have a continuous dosis
    strength: float, strength of the dosis

    Output
    ------
    dosis: func, function for dosis in time
    """

    dt = (t[-1]-t[0])/no_spikes  # time difference between spikes
    epsilon = dt/100  # width of spike (in time)
    times = np.arange(no_spikes)*dt

    if shape:

        def dosis(t):
            return strength
    else:

        def dosis(t):
            if t < times[0]:
                t = 0
            elif t > times[-1]+epsilon:
                t = 0
            elif (t > times[-1]) and (t <= times[-1]+epsilon):
                t = 1
            else:
                for it in range(0, no_spikes-1):
                    if t >= times[it] and (t <= times[it]+epsilon):
                        t = 1
                    elif (t > times[it]+epsilon) and (t < times[it+1]):
                        t = 0
            return t * strength

    return dosis

def set_model_args():
    """Function to set the model arguments like
    compartment volume

    Output
    ------
    model_args: dict, values of model arguments
    """

    model_args = {
        'name': 'model1',
        'Q_p1': 1.0,
        'V_c': 1.0,
        'V_p1': 1.0,
        'CL': 1.0,
        'X': 1.0,
        'k_a': 1.0
    }
    return model_args
