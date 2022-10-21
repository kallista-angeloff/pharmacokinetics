import scipy.integrate

import pkmodel as pk


def rhs_iv_one_compartment(t, y, model_input, t_eval):
    '''Defines a one-compartment IV model.
    
    Parameters
    ----------
    :param t: `t` is an array containing the time over which to solve.
    :type t: array 

    :param y: `y` is an array containing the quantities changing, e.g.
        q_c, the amount of the drug in the main compartment.
    :type y: array

    :param model_input: `model_input` is a dictionary containing the following: 
    
    :param k_a: `k_a` is the absorption rate in 1/hr of the drug in the 
        initial dosing compartment.
    :type k_a: float
    :param Q_p1: `Q_p1` is the exchange rate in mL/hr between the main and 
        peripheral compartments.
    :type Q_p1: float
    :param V_c: `V_c` is the volume in mL of the main compartment.
    :type V_c: float
    :param V_p1: `V_p1` is the volume in mL of the peripheral compartment.
    :type V_p1: float
    :param CL: `CL` is the clearance rate in mL/hr of the main compartment.
    :type CL: float
    :param `X`: is the dose in ng of the drug.
    :type X: float
    

    Return
    ----------
    :return dqc_dt: `dqc_dt` is the rate of change of the drug in the main compartment over time, d(q_c)/dt.
    :rtype dqc_dt: array

    '''
    
    q_c = y
    dose = pk.create_dosis_function(t_eval,
                                    model_input['dose_shape'], 
                                    model_input['dose_spikes'], 
                                    model_input['dose_strength'])
    print(dose(t))
    dqc_dt = dose(t) - q_c/model_input['V_c'] * model_input['CL']
    return [dqc_dt]


def iv_one_compartment(t_eval, y0, model_input):
    '''Solves the differential equations of a one-compartment IV dosing model (as 
    described in rhs_iv_one_compartment) using scipy.integrate.solve_ivp.
    
    Parameters
    ----------
    :param t: `t_eval` is an array containing the time over which to solve.array containing the timespan over which to 
        evaluate the differential equations.
    :type t_eval: array

    :param y0: `y0` is an array containing the initial conditions for the 
        differential equations.
    :type y0: array

    :param model_input: `model_input` is a dictionary containing the following: 
    
    :param k_a: `k_a` is the absorption rate in 1/hr of the drug in the 
        initial dosing compartment.
    :type k_a: float
    :param Q_p1: `Q_p1` is the exchange rate in mL/hr between the main and 
        peripheral compartments.
    :type Q_p1: float
    :param V_c: `V_c` is the volume in mL of the main compartment.
    :type V_c: float
    :param V_p1: `V_p1` is the volume in mL of the peripheral compartment.
    :type V_p1: float
    :param CL: `CL` is the clearance rate in mL/hr of the main compartment.
    :type CL: float
    :param `X`: is the dose in ng of the drug.
    :type X: float
    
    Return
    ----------
    :return sol_iv_one_compartment: `sol_iv_one_compartment` contains the solution to d(q_c)/dt.
        Fields of interest: .t and .y, which give the time points and 
        values of the solution at those points.
    :rtype sol_iv_one_compartment: bunch object OdeResult
    '''

    sol_iv_one_compartment = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs_iv_one_compartment(t, y, model_input, t_eval),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval, max_step = t_eval[1] - t_eval[0]
    )
    print(sol_iv_one_compartment.message) # test
    return sol_iv_one_compartment
    
# --- Two compartments --------------------------

def rhs_iv_two_compartments(t, y, model_input, t_eval): 

    '''Defines a two-compartment IV model (main and peripheral compartments).
    
    Parameters
    ----------
    :param t: `t` is an array containing the time over which to solve.
    :type t: array 

    :param y: `y` is an array containing the quantities changing, e.g.
        q_c, the amount of the drug in the main compartment.
    :type y: array

    :param model_input: `model_input` is a dictionary containing the following: 

    :param k_a: `k_a` is the absorption rate in 1/hr of the drug in the 
        initial dosing compartment.
    :type k_a: float
    :param Q_p1: `Q_p1` is the exchange rate in mL/hr between the main and 
        peripheral compartments.
    :type Q_p1: float
    :param V_c: `V_c` is the volume in mL of the main compartment.
    :type V_c: float
    :param V_p1: `V_p1` is the volume in mL of the peripheral compartment.
    :type V_p1: float
    :param CL: `CL` is the clearance rate in mL/hr of the main compartment.
    :type CL: float
    :param `X`: is the dose in ng of the drug.
    :type X: float
     
    Return
    ----------
    :return dqc_dt: `dqc_dt` is the rate of change of the drug in the main 
        compartment over time, d(q_c)/dt.
    :rtype dqc_dt: array
    
    :return dqp1_dt: `dqp_1_dt` is the rate of change of the drug in the peripheral 
    compartment over time, d(q_p1)/dt.
    :rtype dqp1_dt: array

    '''
    
    q_c, q_p1 = y
    
    transition = model_input['Q_p1'] * q_c/model_input['V_c'] - q_p1/model_input['V_p1']

    dose = pk.create_dosis_function(t_eval,
                                 model_input['dose_shape'],
                                 model_input['dose_spikes'],
                                 model_input['dose_strength'])
    dqc_dt = dose(t) - q_c/model_input['V_c']*model_input['CL'] - transition
    dqp1_dt = transition

    return [dqc_dt, dqp1_dt]


def iv_two_compartments(t_eval, y0, model_input):
    '''Solves the differential equations of a two-compartment IV dosing model (as 
    described in rhs_iv_two_compartments) using scipy.integrate.solve_ivp.
    
    Parameters
    ----------
    :param t_eval: `t_eval` is an array containing the timespan over which to 
        evaluate the differential equations.
    :type t_eval: array

    :param y0: `y0` is an array containing the initial conditions for the 
        differential equations.
    :type y0: array

    :param model_input: `model_input` is a dictionary containing the following: 

    :param k_a: `k_a` is the absorption rate in 1/hr of the drug in the 
        initial dosing compartment.
    :type k_a: float
    :param Q_p1: `Q_p1` is the exchange rate in mL/hr between the main and 
        peripheral compartments.
    :type Q_p1: float
    :param V_c: `V_c` is the volume in mL of the main compartment.
    :type V_c: float
    :param V_p1: `V_p1` is the volume in mL of the peripheral compartment.
    :type V_p1: float
    :param CL: `CL` is the clearance rate in mL/hr of the main compartment.
    :type CL: float
    :param `X`: is the dose in ng of the drug.
    :type X: float

    Return
    ----------
    :return: `sol_iv_two_compartments` contains the solutions to d(q_c)/dt and d(q_p1)/dt.
        Fields of interest: .t and .y, which give the time points and values 
        of the solutions at those points.
    :rtype sol_iv_two_compartments: bunch object OdeResult
    '''
    
    sol_iv_two_compartments = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs_iv_two_compartments(t, y, model_input, t_eval),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval, max_step = t_eval[1] - t_eval[0]
    )
    print(sol_iv_two_compartments.message)
    return sol_iv_two_compartments

# --- Subcutaneous ------------------------------

def rhs_subcutaneous(t, y, model_input, t_eval):
    '''Defines a subcutaneous injection delivery model with an initial    
    dosing compartment and an additional peripheral compartment.

    Parameters
    ----------
    :param t: `t` is an array containing the time over which to solve.
    :type t: array 

    :param y: `y` is an array containing the quantities changing, e.g.
        q_c, the amount of the drug in the main compartment.
    :param type: array

    :param model_input: `model_input` is a dictionary containing the following: 

    :param k_a: `k_a` is the absorption rate in 1/hr of the drug in the 
        initial dosing compartment.
    :type k_a: float
    :param Q_p1: `Q_p1` is the exchange rate in mL/hr between the main and 
        peripheral compartments.
    :type Q_p1: float
    :param V_c: `V_c` is the volume in mL of the main compartment.
    :type V_c: float
    :param V_p1: `V_p1` is the volume in mL of the peripheral compartment.
    :type V_p1: float
    :param CL: `CL` is the clearance rate in mL/hr of the main compartment.
    :type CL: float
    :param `X`: is the dose in ng of the drug.
    :type X: float
    
    Return
    ----------
    :return dq0_dt: `dq0_dt` is the rate of change of the drug in the dosing compartment
        over time, d(q_0)/dt.
    :rtype dq0_dt: array

    :return dqc_dt: `dqc_dt` is the rate of change of the drug in the main compartment 
        over time, d(q_c)/dt.
    :rtype dqc_dt: array
    
    :return dqp_1_dt: `dqp_1_dt` is the rate of change of the drug in the peripheral 
        compartment over time, d(q_p1)/dt.
    :rtype dqp_1_dt: array    
    '''
    q_0, q_c, q_p1 = y
    
    transition = model_input['Q_p1'] * q_c/model_input['V_c'] - q_p1/model_input['V_p1']
    dose = pk.create_dosis_function(t_eval,
                                 model_input['dose_shape'],
                                 model_input['dose_spikes'],
                                 model_input['dose_strength'])
    dq0_dt = dose(t) - model_input['k_a'] * q_0
    dqc_dt = model_input['k_a']*q_0 - q_c/model_input['V_c']*model_input['CL'] - transition
    dqp1_dt = transition

    return [dq0_dt, dqc_dt, dqp1_dt]

def subcutaneous(t_eval, y0, model_input):
    '''Solves the differential equations involved in subcutaneous dosing
    (as described in rhs_subcutaneous) using scipy.integrate.solve_ivp.

    Parameters
    ----------
    :param t: `t_eval` is an array containing the timespan over which to 
        evaluate the differential equations.
    :type t_eval: array

    :param y0: `y0` is an array containing the initial conditions for the 
        differential equations.
    :type y0: array

    :param model_input: `model_input` is a dictionary containing the following: 
    
    :param k_a: `k_a` is the absorption rate in 1/hr of the drug in the 
        initial dosing compartment.
    :type k_a: float
    :param Q_p1: `Q_p1` is the exchange rate in mL/hr between the main and 
        peripheral compartments.
    :type Q_p1: float
    :param V_c: `V_c` is the volume in mL of the main compartment.
    :type V_c: float
    :param V_p1: `V_p1` is the volume in mL of the peripheral compartment.
    :type V_p1: float
    :param CL: `CL` is the clearance rate in mL/hr of the main compartment.
    :type CL: float
    :param `X`: is the dose in ng of the drug.
    :type X: float

    Return
    ----------
    :return sol_subcutaneous: `sol_subcutaneous` contains the solutions to d(q_0)/dt, d(q_c)/dt, 
        and d(q_p1)/dt. Fields of interest: .t and .y, which give the time points 
        and values of the solutions at those points.
    :rtype sol_subcutaneous: bunch object OdeResult
    
    '''

    sol_subcutaneous = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs_subcutaneous(t, y, model_input, t_eval),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval, max_step = t_eval[1] - t_eval[0]
    )

    sol_subcutaneous.dose_comp = sol_subcutaneous.y[0]
    sol_subcutaneous.y = sol_subcutaneous.y[1:]
    
    print(sol_subcutaneous.message)
    return sol_subcutaneous

