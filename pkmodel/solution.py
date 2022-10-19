#
# Solution class
#

## Packages
import numpy as np
import matplotlib.pyplot as plt

class Solution:
    """A Pharmokinetic (PK) model solution

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, value=44):
        self.value = value

def plot_drug(model,f):
    """
    Function that plots the concentration of the drug from the central
    compartment and also the one/two peripheral compartments (up to 
    the user's decision) over the time of the treatment.

    Inputs
    ------
    model (dict): The model results that are to be plotted by the function 
    
    fig (figure): The figure that the data will be plotted on   

    Outputs
    -------
    fig (figure): (same as fig input)

    """

    for comp in model['solution']:
        f.axes[0].plot(model['t'],comp)
    f.axes[1].plot(model['t'],model['dose'])
    return f

def solution(model_sol, *args):
    """ 
    Function that plots the results from the model and allows
    the user to compare results between different models.
    
    Uses the plot_drug function to plot the individual plots.

    Inputs
    ------
    model_sol (dict): The first set of model results. Should contain 2 keys 
                      ('dose', 'solution'). The dose values shows the amount 
                      of drug [units: ng] input with time, and the solution 
                      values show the amount of drug in the central (element 
                      0) and peripheral (subsequent elements) compartments.

    *args: Optional arguments for more sets of model results. Should have 
           same structure as model_sol.

    Outputs
    -------
    """

    f, (a0, a1) = plt.subplots(2, 1 , gridspec_kw={'height_ratios': [3, 1]})
    for model in [model_sol, *args]:
        plot_drug(model,f)
    
    f.legend()
    a0.set_ylabel('drug mass [ng]')
    a1.set_xlabel('time [h]')
    f.tight_layout()


