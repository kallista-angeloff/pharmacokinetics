import matplotlib.pylab as plt
import numpy as np
import scipy.integrate


def dose(t, X):
    return X

def rhs_iv_one_compartment(t, y, model_input): 
    '''Defines a one-compartment IV model.
    
    Parameters
    ----------
    model_input : dict
        `model_input` is a dictionary containing the following:
        V_c : float
            `V_c` is the volume in mL of the main compartment.
        CL: float
            `CL` is the clearance rate in mL/hr of the main compartment.
        X : float
            `X` is the dose in ng of the drug.
    dose : function
        `dose` is a function that takes two floats, t and X, representing
        the dosing protocol over time, and returns ... ?
    t : array
    X : float

    Return
    ----------
    dqc_dt : float
        `dqc_dt` is the rate of change of the drug in the main compartment
        over time, d(q_c)/dt.
    '''
    
    q_c = y
    dqc_dt = dose(t, model_input['X']) - q_c/model_input['V_c'] * model_input['CL']

    return dqc_dt

def iv_one_compartment(t_eval, y0, model_input):
    '''Solves the differential equations of a one-compartment IV dosing model (as 
    described in rhs_iv_one_compartment) using scipy.integrate.solve_ivp.
    
    Parameters
    ----------
    model_input : dict
        `model_input` is a dictionary containing the following: 



    t_eval : array
        `t_eval` is an array containing the timespan over which to 
        evaluate the differential equation.
    y0 : array (n.b. one-element array here)
        `y0` is an array containing the initial conditions for the 
        differential equation.

    Return
    ----------
    sol_iv_one_compartment : 


    '''

    sol_iv_one_compartment = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs_iv_one_compartment(t, y, model_input),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval
    )

    return sol_iv_one_compartment
    
# --- Two compartments --------------------------

def rhs_iv_two_compartments(t, y, model_input): 

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
    transition = model_input['Q_p1'] * q_c/model_input['V_c'] - q_p1/model_input['V_p1']
    dqc_dt = dose(t, model_input['X']) - q_c/model_input['V_c']*model_input['CL'] - transition
    dqp1_dt = transition
    
    return [dqc_dt, dqp1_dt]

def iv_two_compartments(t_eval, y0, model_input):
    '''Solves the differential equations of a two-compartment IV dosing model (as 
    described in rhs_iv_two_compartments) using scipy.integrate.solve_ivp.
    
    Parameters
    ----------
    model_input : dict
        `model_input` is a dictionary containing the following: 

    t_eval : array
        `t_eval` is an array containing the timespan over which to 
        evaluate the differential equations.
    y0 : array
        `y0` is an array containing the initial conditions for the 
        differential equations.

    Return
    ----------
    sol_iv_two_compartments : 
    '''
    
    sol_iv_two_compartments = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs_iv_two_compartments(t, y, model_input),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval
    )

    return sol_iv_two_compartments

# --- Subcutaneous ------------------------------

def rhs_subcutaneous(t, y, model_input):
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
    q_0, q_c, q_p1 = y
    
    transition = model_input['Q_p1'] * q_c/model_input['V_c'] - q_p1/model_input['V_p1']
    
    dq0_dt = dose(t, model_input['X']) - model_input['k_a'] * q_0
    dqc_dt = model_input['k_a']*q_0 - q_c/model_input['V_c']*model_input['CL'] - transition
    dqp1_dt = transition

    return [dq0_dt, dqc_dt, dqp1_dt]


def subcutaneous(t_eval, y0, model_input):
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

    sol_subcutaneous = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs_subcutaneous(t, y, model_input),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval
    )

    return sol_subcutaneous


# -----------------------------

t_eval = np.linspace(0, 1, 1000)
y0 = np.array([0.0, 0.0, 0.0]) # initial conditions - need variable number
model_input = {
    'name': 'test for output',
    'Q_p1': 2.0,
    'V_c': 1.0,
    'V_p1': 1.0,
    'CL': 1.0,
    'X': 1.0,
    'k_a': 2.0
}

fig = plt.figure()
sol = iv_one_compartment(t_eval, y0, model_input)


plt.plot(sol.t, sol.y[0, :], label=model_input['name'] + '- q_c')
plt.plot(sol.t, sol.y[1, :], label=model_input['name'] + '- q_p1')

plt.legend()
plt.ylabel('drug mass [ng]')
plt.xlabel('time [h]')
plt.show()