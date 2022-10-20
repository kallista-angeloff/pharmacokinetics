#
# Protocol class
#

from pickle import FALSE
import numpy as np


class Protocol:  # do we need a class for this?
    """A Pharmokinetic (PK) protocol

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, value=43):
        self.value = value


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

    dosis_comp = FALSE
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
    no_comps = 1
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
