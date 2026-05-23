"""Unit tests for NISSD module"""

import unittest
import numpy as np
import sys
sys.path.append('../..')

from vagus_decipher.nissd import NeuroImmuneStateSpaceModel, JacobianConstraint

class TestNISSD(unittest.TestCase):
    
    def setUp(self):
        self.state_dim = 7
        self.model = NeuroImmuneStateSpaceModel(state_dim=self.state_dim)
    
    def test_state_transition(self):
        S = np.ones(self.state_dim) * 0.5
        Lambda = np.array([5.0])
        S_next = self.model.state_transition(S, Lambda, dt=0.001)
        self.assertEqual(len(S_next), self.state_dim)
        self.assertTrue(np.all(S_next >= 0))
    
    def test_observation(self):
        S = np.ones(self.state_dim) * 0.5
        Lambda = self.model.observation(S)
        self.assertEqual(len(Lambda), 1)
        self.assertTrue(Lambda[0] >= 0)
    
    def test_state_names(self):
        names = self.model.get_state_names()
        self.assertEqual(len(names), self.state_dim)
        expected = ['TNF_a', 'IL_1b', 'IL_6', 'IL_10', 'C3a', 'NeutAct', 'CoagAct']
        self.assertEqual(names, expected)
    
    def test_jacobian_constraint(self):
        def f_theta(S):
            return np.maximum(S * 0.95, 0)
        
        J = JacobianConstraint.compute_jacobian(f_theta, np.ones(self.state_dim))
        loss = JacobianConstraint.sign_constraint_loss(J)
        self.assertGreaterEqual(loss, 0)

if __name__ == '__main__':
    unittest.main()
