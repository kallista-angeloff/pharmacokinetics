import scipy.integrate
import pkmodel as pk


def rhs_iv_one_compartment(t, y, model_input):
    '''Defines a one-compartment IV model.

    Parameters
    ----------
    t : array
    `t` is an array containing the time over which to solve.
    y : array
    `y` is an array containing the quantities changing, e.g.
    q_c, the amount of the drug in the main compartment.
    model_input : dict
        `model_input` is a dictionary containing the following:
        V_c : float
            `V_c` is the volume in mL of the main compartment.
        CL: float
            `CL` is the clearance rate in mL/hr of the main compartment.
        X : float
            `X` is the dose in ng of the drug.
    Return
    ----------
    dqc_dt : array
        `dqc_dt` is the rate of change of the drug in the main compartment
        over time, d(q_c)/dt.
    '''

    q_c = y
    dose = pk.create_dosis_function(model_input['dose_shape'], 
                                    model_input['dose_spikes'], 
                                    model_input['dose_strength'])
    dqc_dt = dose(t) - q_c/model_input['V_c'] * model_input['CL']
    return [dqc_dt]


def iv_one_compartment(t_eval, y0, model_input):
    '''Solves the differential equations of a one-compartment IV dosing model (as
    described in rhs_iv_one_compartment) using scipy.integrate.solve_ivp.

    Parameters
    ----------
    t_eval : array
        `t_eval` is an array containing the timespan over which to
        evaluate the differential equations.
    y0 : array
        `y0` is an array containing the initial conditions for the
        differential equations.
    model_input : dict
        `model_input` is a dictionary containing the following:
        V_c : float
            `V_c` is the volume in mL of the main compartment.
        CL: float
            `CL` is the clearance rate in mL/hr of the main compartment.
        X : float
            `X` is the dose in ng of the drug.

    Return
    ----------
    sol_iv_one_compartment : bunch object OdeResult
    Fields of interest:
        .t : array
        .y : array
    which give the time points and values of the solution at those points.
    '''

    sol_iv_one_compartment = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs_iv_one_compartment(t, y, model_input),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval
    )
    # print(sol_iv_one_compartment.message)  # test
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

    dose = pk.create_dosis_function(model_input['dose_shape'],
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
    sol_iv_two_compartments : bunch object OdeResult
    Fields of interest:
        .t : array
        .y : array
    which give the time points and values of the solution at those points.
    '''

    sol_iv_two_compartments = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs_iv_two_compartments(t, y, model_input),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval
    )
    print(sol_iv_two_compartments.message)
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

    Return
    ----------

    '''
    q_0, q_c, q_p1 = y
    transition = model_input['Q_p1'] * q_c/model_input['V_c'] - q_p1/model_input['V_p1']
    dose = pk.create_dosis_function(model_input['dose_shape'],
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
    sol_subcutaneous : bunch object OdeResult
    Fields of interest:
        .t : array
        .y : array
    which give the time points and values of the solution at those points.

    '''

    sol_subcutaneous = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs_subcutaneous(t, y, model_input),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval
    )
    print(subcutaneous.message)
    return sol_subcutaneous
