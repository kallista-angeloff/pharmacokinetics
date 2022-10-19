from logging import raiseExceptions
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
    dosis_comp = (answer == 'y')  #convert input into boolean,
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


def set_up_dict(no_comps, dosis_comp):
    """Creates the dictionary to save the dosis and
    solutions for the model

    Input
    ------


    Output
    -------
    data_dict: dict, dictionary of dosis and solutions

    """
    if dosis_comp:
        no_solutions = no_comps + 1
    else:
        no_solutions = no_comps
    data_dict = {'dosis': [],
                 'solution': np.zeros((no_solutions, 1000))}
    return data_dict


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
    shape = 0
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
    no_spikes = None
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
    dose = 10
    return dose


def create_dosis_function(shape, no_spikes, data_dict):
    """Function takes inputs about dosis and creates an array
    for the dose in time

    Input
    -----

    Output
    ------
    data_dict: dict, dictionary with dosis and solutions
    """
    return data_dict
