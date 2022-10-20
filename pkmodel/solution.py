#
# Solution.py functions
#

# Packages
import numpy as np
import matplotlib.pyplot as plt

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
    
    # check inputs
    for model in [model_sol, *args]:
        if not isinstance(model_sol, dict):
            raise TypeError('Model data output for plotting must be a dictionary')
    
    # create subplot
    f, (a0,a1) = plt.subplots(2, 1 , gridspec_kw={'height_ratios': [3, 1]})
    for model in [model_sol, *args]:    # calls plot_drug function
        plot_drug(model, f)
    
     # adding visualisation elements
    f.legend()
    f.suptitle('Drug amount in different systems')
    a0.set_ylabel('compartment drug amoount [ng]')
    a1.set_ylabel('drug dosage amount [ng]')
    a1.set_xlabel('time [h]')
    a0.set_xticks([])
    f.subplots_adjust(hspace=0)
    f.show()

def plot_drug(model, f):
    """
    Function that plots the concentration of the drug from the central
    compartment and also the one/two peripheral compartments (up to 
    the user's decision) over the time of the treatment.

    Inputs
    ------
    model (dict): The model results that are to be plotted by the function 
    
    fig (figure, 2 axes): The figure that the data will be plotted on   

    Outputs
    -------
    fig (figure): (same as fig input)

    """

    # check inputs
    if not isinstance(model, dict):
        raise TypeError('Model data output for plotting must be a dictionary')
    if not isinstance(f, plt.Figure) or len(f.axes) != 2:
        raise ValueError('Second argument must be a figure with 2 axes')

    # plots the drug concentration for each compartment 
    for comp in model.y:
        f.axes[0].plot(model.t, comp)
    f.axes[1].plot(model.t, model.dose)  # plots drug dosage

    return f

