# This file is part of ci_cpp.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest
# import numpy as np

import lsst.ci.cpp as cpp
import lsst.afw.image as afwImage
import lsst.utils.tests

from lsst.utils import getPackageDir


FILENAMES = {'bias': {2: 'DATA/biasGen/bias/2020-01-28/bias-det000_2020-01-28.fits',
                      3: 'DATA/calib/v00/bias/bias_bias_ci_cpp_bias_0_LATISS_calib_v00.fits'},
             'dark': {2: 'DATA/darkGen/dark/2020-01-28/dark-det000_2020-01-28.fits',
                      3: 'DATA/calib/v00/dark/dark_dark_ci_cpp_dark_0_LATISS_calib_v00.fits'},
             'flat': {2: 'DATA/calibs/flat/KPNO_406_828nm~EMPTY/2020-01-28/flat_KPNO_406_828nm~EMPTY-det000_2020-01-28.fits',  # noqa: E501
                      3: 'DATA/calib/v00/flat/KPNO_406_828nm~EMPTY/KPNO_406_828nm~EMPTY/flat_KPNO_406_828nm~EMPTY_KPNO_406_828nm~EMPTY_flat_ci_cpp_flat_0_LATISS_calib_v00.fits'},  # noqa: E501
             'crosstalk': {2: 'DATA/crosstalkGen/calibrations/crosstalk/crosstalk-det000.fits',
                           3: 'DATA/ci_cpp_crosstalk/20200730T16h50m46s/crosstalkProposal/crosstalkProposal_0_LATISS_ci_cpp_crosstalk_20200730T16h50m46s.fits'},  # noqa: E501
}


class ImageProductCases(lsst.utils.tests.TestCase):

    def setup_pair(self, file1, file2):
        """Lookup files and pass them to compare function.

        Parameters
        ----------
        file1 : `str`
            Partial filename of gen2 product.
        file2 : `str`
            Partial filename of gen3 product.

        Returns
        -------
        results : `lsst.pipe.base.Struct`
            Statistics results.
        """
        pathGen2 = getPackageDir('ci_cpp_gen2') + '/' + file1
        pathGen3 = getPackageDir('ci_cpp_gen3') + '/' + file2

        exp1 = afwImage.ExposureF().readFits(pathGen2)
        exp2 = afwImage.ExposureF().readFits(pathGen3)

        return cpp.compareExposures(exp1, exp2)

    def test_BiasImageProduct(self):
        """Compare bias frames.
        """
        results = self.setup_pair(FILENAMES['bias'][2],
                                  FILENAMES['bias'][3])

        self.assertMasksEqual(results.mi1.getMask(), results.mi2.getMask())
        self.assertFloatsAlmostEqual(results.imageStats[0], 0.0)

        # self.assertFloatsAlmostEqual(results.varianceStats[3], 0.0)

    def test_DarkImageProduct(self):
        """Compare dark frames.
        """
        results = self.setup_pair(FILENAMES['dark'][2],
                                  FILENAMES['dark'][3])

        # self.assertMasksEqual(results.mi1.getMask(), results.mi2.getMask())
        # self.assertFloatsAlmostEqual(results.imageStats[0], 0.0)
        print(results.imageStats, results.maskStats, results.varianceStats)

    def test_FlatImageProduct(self):
        """Compare flat frames.
        """
        results = self.setup_pair(FILENAMES['flat'][2],
                                  FILENAMES['flat'][3])

        # self.assertMasksEqual(results.mi1.getMask(), results.mi2.getMask())
        # self.assertFloatsAlmostEqual(results.imageStats[0], 0.0)
        print(results.imageStats, results.maskStats, results.varianceStats)


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
