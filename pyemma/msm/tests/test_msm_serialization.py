# This file is part of PyEMMA.
#
# Copyright (c) 2016, 2014 Computational Molecular Biology Group, Freie Universitaet Berlin (GER)
#
# PyEMMA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from tempfile import NamedTemporaryFile

import numpy as np

from pyemma import datasets
from pyemma.msm import bayesian_markov_model
from pyemma import load


class TestMSMSerialization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data = datasets.load_2well_discrete()
        obs_micro = data.dtraj_T100K_dt10

        # stationary distribution
        pi_micro = data.msm.stationary_distribution
        pi_macro = np.zeros(2)
        pi_macro[0] = pi_micro[0:50].sum()
        pi_macro[1] = pi_micro[50:].sum()

        # coarse-grain microstates to two metastable states
        cg = np.zeros(100, dtype=int)
        cg[50:] = 1
        obs_macro = cg[obs_micro]
        # hidden states
        cls.nstates = 2
        # samples
        cls.nsamples = 10

        cls.lag = 100

        cls.msm = datasets.load_2well_discrete().msm
        cls.bmsm_rev = bayesian_markov_model(obs_macro, cls.lag,
                                             reversible=True, nsamples=cls.nsamples)

    def test_msm_save_load(self):
        with NamedTemporaryFile(delete=False) as f:
            self.msm.save(f.name)
            new_obj = load(f.name)

        np.testing.assert_equal(new_obj.transition_matrix, self.msm.transition_matrix)
        self.assertEqual(new_obj.nstates, self.msm.nstates)
        self.assertEqual(new_obj.is_sparse, self.msm.is_sparse)
        self.assertEqual(new_obj.is_reversible, self.msm.is_reversible)

        self.assertEqual(new_obj, self.msm)

    def test_sampled_MSM_save_load(self):
        with NamedTemporaryFile(delete=False) as f:
            self.bmsm_rev.save(f.name)
            new_obj = load(f.name)

        np.testing.assert_equal(new_obj.samples, self.bmsm_rev.samples)

        np.testing.assert_equal(new_obj.transition_matrix, self.bmsm_rev.transition_matrix)
        self.assertEqual(new_obj.nstates, self.bmsm_rev.nstates)
        self.assertEqual(new_obj.is_sparse, self.bmsm_rev.is_sparse)
        self.assertEqual(new_obj.is_reversible, self.bmsm_rev.is_reversible)
