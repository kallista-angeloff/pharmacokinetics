#
# Solution.py functions
#

# Packages
import os
from datetime import datetime
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
    fig, (ax_0,ax_1) = plt.subplots(2, 1 , gridspec_kw={'height_ratios': [3, 1]})
    for model in [model_sol, *args]:    # calls plot_drug function
        plot_drug(model, fig)
    
     # adding visualisation elements
    ax_0.legend()
    ax_1.legend()
    fig.suptitle('Pharmacokinetic Model')
    ax_0.set_ylabel('drug in compartment [ng]')
    ax_1.set_ylabel('dosage [ng]')
    ax_1.set_xlabel('time [h]')
    ax_0.set_xticks([])
    fig.subplots_adjust(hspace=0)
    
    # saving graph under ~/data
    if not os.path.exists(os.getcwd() + '/data/'):    # creating /data folder if it does not exist
        os.mkdir(os.getcwd() + '/data/')   
    fig.savefig(os.getcwd() + '/data/model' + datetime.today().strftime('%Y%m%d%H%M%S') + '.png')

def plot_drug(model, fig):
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
    if not isinstance(fig, plt.Figure) or len(fig.axes) != 2:
        raise ValueError('Second argument must be a figure with 2 axes')

    # plots the drug concentration for each compartment 
    comp_label = ['Central', 'Peripheral1', 'Peripheral2']
    for comp, _ in enumerate(model.y):
        fig.axes[0].plot(model.t, model.y[comp], label = model.name + ' ' + comp_label[comp])
    if 'dose_comp' in model.keys():
        fig.axes[0].plot(model.t, model.dose_comp, label = model.name + ' dose_comp')
    fig.axes[1].plot(model.t, model.dose, label = model.name)  # plots drug dosage
    
    return fig

