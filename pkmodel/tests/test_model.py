import unittest
import numpy as np
import pkmodel as pk
class ModelTest(unittest.TestCase):
    """
    Tests the :class:`Model` class.
    """
    # set model and parameters
    
    def test_rhs_iv_one_compartment(self):
        t = np.linspace(0,10,10)
        t_eval = t
        y = np.array([0.0])
        model_input = pk.set_model_args()
        model_input['dose_shape'] = 1
        model_input['dose_strength'] = 5
        model_input['dose_spikes'] = 5
        
        dqc_dt = pk.rhs_iv_one_compartment(t, y, model_input, t_eval)
        self.assertEqual(dqc_dt,[5])

    def test_iv_one_compartment(self):
        t = np.linspace(0,10,10)
        t_eval = t
        y = np.array([0.0])
        model_input = pk.set_model_args()
        model_input['dose_shape'] = 1
        model_input['dose_strength'] = 5
        model_input['dose_spikes'] = 5

        sol = pk.iv_one_compartment(t_eval, y, model_input)
        analytical_answer = [0, 3.3544858,4.45811595,4.82138807,4.9410439,
                              4.98053981,4.9935766,4.99787977,4.99930016,4.99976893]
        for i,_ in enumerate(analytical_answer):
            self.assertAlmostEqual(sol.y[0][i],analytical_answer[i])

    def test_rhs_iv_two_compartments(self):
        t = np.linspace(0,10,10)
        t_eval = t
        y0 = np.array([0.0, 0.0])
        model_input = pk.set_model_args()
        model_input['dose_shape'] = 1
        model_input['dose_strength'] = 5
        model_input['dose_spikes'] = 5
        
        y = pk.rhs_iv_two_compartments(t, y0, model_input, t_eval)
        self.assertEqual(y,[5, 0])

    def test_iv_two_compartments(self):
        t = np.linspace(0,10,10)
        t_eval = t
        y = np.array([0.0, 0.0])
        model_input = pk.set_model_args()
        model_input['dose_shape'] = 1
        model_input['dose_strength'] = 5
        model_input['dose_spikes'] = 5

        sol = pk.iv_two_compartments(t_eval, y, model_input)
        analytical_answer = [[0, 2.55804985, 3.4476088, 3.98732743, 4.33753041,
                              4.56662951, 4.7165019, 4.81454476, 4.8786816, 4.92063166],
                             [0, 1.21696084, 2.4974675, 3.36121108, 3.92798228,
                              4.29873486, 4.54126326, 4.69991416, 4.80369651, 4.87158889]]
        for i,_ in enumerate(analytical_answer):
            self.assertAlmostEqual(sol.y[0][i], analytical_answer[0][i])
            self.assertAlmostEqual(sol.y[1][i], analytical_answer[1][i])

    def test_rhs_subcutaneous(self):
        t = np.linspace(0,10,10)
        t_eval = t
        y0 = np.array([0.0, 0.0, 0.0])
        model_input = pk.set_model_args()
        model_input['dose_shape'] = 1
        model_input['dose_strength'] = 5
        model_input['dose_spikes'] = 5
        
        y = pk.rhs_subcutaneous(t, y0, model_input, t_eval)
        self.assertEqual(y,[5, 0, 0])
    def test_subcutaneous(self):
        t = np.linspace(0,10,10)
        t_eval = t
        y = np.array([0.0, 0.0, 0.0])
        model_input = pk.set_model_args()
        model_input['dose_shape'] = 1
        model_input['dose_strength'] = 5
        model_input['dose_spikes'] = 5

        sol = pk.subcutaneous(t_eval, y, model_input)
        analytical_answer = [[0, 1.217114, 2.49773141, 3.36184863, 3.92828391,
                              4.2988771, 4.54133004, 4.69994531, 4.80371091, 4.8715931 ],
                             [0, 0.42088089, 1.48679277, 2.526699, 3.32425309,
                              3.88472022, 4.26413746, 4.51655376, 4.68306514, 4.79244861]]
        analytical_dose = [0, 3.35403456, 4.45811639, 4.82141364, 4.94105234,
                           4.9805426, 4.99357751, 4.99788007, 4.99930026, 4.99976902]
        for i,_ in enumerate(analytical_answer):
            self.assertAlmostEqual(sol.y[0][i], analytical_answer[0][i])
            self.assertAlmostEqual(sol.y[1][i], analytical_answer[1][i])
            self.assertAlmostEqual(sol.dose_comp[i], analytical_dose[i])

if __name__ == '__main__':
    unittest.main()

