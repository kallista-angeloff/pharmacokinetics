import matplotlib.pylab as plt
import numpy as np
import scipy.integrate


def rhs_iv_one_compartment(t, Q_p1, V_c, V_p1, CL, X): #add dose function as an argument
    '''Defines a one-compartment IV model.
    
    Parameters
    ----------
    V_c : float
        `V_c` is the volume in mL of the main compartment.
    CL: float
        `CL` is the clearance rate in mL/hr of the main compartment.
    X : float
        `X` is the dose in ng of the drug.
    
    Return
    ----------
    dqc_dt : float
        `dqc_dt` is the rate of change of the drug in the main compartment
        over time, d(q_c)/dt.
    '''
    
    # dqc_dt = dose(t, X) - q_c / V_c * CL 
    dqc_dt = X - q_c / V_c * CL 

    return dqc_dt

def iv_one_compartment(V_c, CL, X):
    '''Solves the differential equations of a one-compartment IV dosing model (as 
    described in rhs_iv_one_compartment) using scipy.integrate.solve_ivp.
    
    Parameters
    ----------
    model_args : dict
        `model_args` is a dictionary containing the following: ### 
    t_eval : array
        `t_eval` is an array containing the timespan over which to 
        evaluate the differential equation.
    y0 : array (n.b. one-element array here)
        `y0` is an array containing the initial conditions for the 
        differential equation.

    Return
    ----------
    sol_iv_one_compartment : ###
    '''

    args = [
        model_args['Q_p1'], model_args['V_c'], model_args['V_p1'], model_args['CL'], model_args['X']
    ]
    sol_iv_one_compartment = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs_iv_one_compartment(t, y, *args),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval
    )

    return sol_iv_one_compartment
    
# --- Two compartments --------------------------

def rhs_iv_two_compartments(t, y, Q_p1, V_c, V_p1, CL, X): 
    # add dose function as an argument
    # pass in dictionary and call by keys
    '''Defines a two-compartment IV model (main and peripheral compartments).
    
    Parameters
    ----------
    Q_p1 : float
        `Q_p1` is the exchange rate in mL/hr between the main and peripheral 
        compartments.
    V_c : float
        `V_c` is the volume in mL of the main compartment.
    V_p1: float
        `V_p1` is the volume in mL of the peripheral compartment.
    CL: float
        `CL` is the clearance rate in mL/hr of the main compartment.
    X : float
        `X` is the dose in ng of the drug.
    
    Return
    ----------
    dqc_dt : float
        `dqc_dt` is the rate of change of the drug in the main compartment
        over time, d(q_c)/dt.
    dqp1_dt : float
        `dqp_1_dt` is the rate of change of the drug in the peripheral 
        compartment over time, d(q_p1)/dt.
    '''
    q_c, q_p1 = y
    transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
    dqc_dt = dose(t, X) - q_c / V_c * CL - transition
    dqp1_dt = transition
    
    return [dqc_dt, dqp1_dt]

def iv_two_compartments(model_args, t_eval, y0):
    '''Solves the differential equations of a two-compartment IV dosing model (as 
    described in rhs_iv_two_compartments) using scipy.integrate.solve_ivp.
    
    Parameters
    ----------
    model_args : dict
        `model_args` is a dictionary containing the following: ### 
    t_eval : array
        `t_eval` is an array containing the timespan over which to 
        evaluate the differential equations.
    y0 : array
        `y0` is an array containing the initial conditions for the 
        differential equations.

    Return
    ----------
    sol_iv_two_compartments : ###
    '''
    
    args = [
        model_args['Q_p1'], model_args['V_c'], model_args['V_p1'], model_args['CL'], model_args['X']
    ]
    sol_iv_two_compartments = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs_iv_two_compartments(t, y, *args),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval
    )

    return sol_iv_two_compartments

# --- Subcutaneous ------------------------------

def rhs_subcutaneous(k_a, Q_p1, V_c, V_p1, CL, X):
    '''Defines a subcutaneous injection delivery model with an initial 
    dosing compartment and an additional peripheral compartment.

    Parameters
    ----------
    k_a : float
        `k_a` is the absorption rate in 1/hr of the drug in the initial dosing 
        compartment.
    Q_p1 : float
        `Q_p1` is the exchange rate in mL/hr between the main and peripheral 
        compartments.
    V_c : float
        `V_c` is the volume in mL of the main compartment.
    V_p1: float
        `V_p1` is the volume in mL of the peripheral compartment.
    CL: float
        `CL` is the clearance rate in mL/hr of the main compartment.
    X : float
        `X` is the dose in ng of the drug.
    
    Return
    ----------

    '''
    pass

def subcutaneous(model_args, t_eval, y0):
    '''Solves the differential equations involved in subcutaneous dosing
    (as described in rhs_subcutaneous) using scipy.integrate.solve_ivp.

    Parameters
    ----------
    model_args : dict
        `model_args` is a dictionary containing the following: ### 
    t_eval : array
        `t_eval` is an array containing the timespan over which to 
        evaluate the differential equations.
    y0 : array
        `y0` is an array containing the initial conditions for the 
        differential equations.

    Return
    ----------
    sol_subcutaneous : ###
    
    '''
    args = [
        model_args['Q_p1'], model_args['V_c'], model_args['V_p1'], 
        model_args['CL'], model_args['X']
    ]
    sol_subcutaneous = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs_subcutaneous(t, y, *args),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval
    )

    return sol_subcutaneous


