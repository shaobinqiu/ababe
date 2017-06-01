# encoding: utf-8
# Distributed under the terms of the MIT License.

import nose
from nose.tools import *

class testVaspPOSCAR:

    def test_get_string(self):
        pass

    def test_write_file(self):
        """.
        The function is tested by save structure
        to a POSCAR file, and then read from it.
        Compare the parameters read from to the 
        origin input parameter. Using almostEqual
        """
        pass

if __name__ == "__main__":
    nose.main()