# Copyright (C) 2007  Matthew Neeley
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import numpy as np

import sys
import os
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath('../..'))
from labrad import units
ValueArray = units.ValueArray
Value = units.Value

class LabradUnitsTests(unittest.TestCase):
    def testParsing(self):
        # prefixes
        # multiplication
        # division
        # powers
        pass
    
    def testArithmetic(self):
        m = units.Unit('m')
        kg = units.Unit('kg')
        km = units.Unit('km')
        
        #self.assertEqual(units.Value(5.0, None)*m, 5.0*m)
        
        # addition
        self.assertEqual(1.0*kg + 0.0, 1.0*kg)
        with self.assertRaises(TypeError): _ = 1.0*kg + 1.0*m
        with self.assertRaises(TypeError): _ = 1.0*kg + 2.0
        self.assertAlmostEqual(1.0*km/m + 5.0, 1005)
        self.assertNotEqual(1.0*kg, None)
    
    def test_valueArray(self):
        # Slicing
        self.assertTrue((ValueArray([1,2,3], 'm')[0:2] == ValueArray([1,2], 'm')).all())
        # Cast to unit
        self.assertTrue((ValueArray([1.2, 4, 5], 'm')['m'] == np.array([1.2, 4, 5])).all())
        # Addition and subtraction of compatible units
        self.assertTrue((ValueArray([3,4], 'm') + ValueArray([100, 200], 'cm') == 
                         ValueArray([4, 6], 'm')).all())
        self.assertTrue((ValueArray([2, 3, 4], 'm') - ValueArray([100, 200, 300], 'cm') ==
                         ValueArray([1, 1, 1], 'm')).all())
        # Division with units remaining
        self.assertTrue((ValueArray([3, 4, 5], 'm') / ValueArray([1, 2, 5], 's') ==
                         ValueArray([3, 2, 1], 'm/s')).all())
        # Division with no units remaining
        self.assertTrue((ValueArray([3, 4, 5], 'm') / ValueArray([1, 2, 5], 'm') ==
                         ValueArray([3, 2, 1], '')).all())
        # Powers
        self.assertTrue((ValueArray([2, 3], 'm')**2 == ValueArray([4, 9], 'm^2')).all())
    
    def testNegativePowers(self):
        self.assertEqual(str(units.Unit('1/s')), 's^-1')
        self.assertEqual(str(units.Unit('1/s^1/2')), 's^-1/2')
    
    def testTypeConversions(self):
        m = units.Unit('m')
        V = units.Unit('V')
        GHz = units.Unit('GHz')
        x1 = 1.0*m
        x2 = 5j*V
        a = np.arange(10)*1.0
        va = units.ValueArray(np.arange(10)*1.0, 'GHz')

        # Unit times number
        self.assertIsInstance(1.0*m, units.Value)
        self.assertIsInstance(1*m, units.Value)
        self.assertIsInstance(m*1.0, units.Value)
        self.assertIsInstance(m*1, units.Value)

        # Value times value or number
        self.assertIsInstance(x1*x1, units.Value)
        self.assertIsInstance(x1*5, units.Value)
        self.assertIsInstance(0*x1, units.Value)

        # Unit times complex
        self.assertIsInstance((1+1j)*V, units.Complex)
        self.assertIsInstance(V*(1+1j), units.Complex)

        # Value times Complex/complex
        self.assertIsInstance(x1*1j, units.Complex)
        self.assertIsInstance(1j*x1, units.Complex)
        self.assertIsInstance(x2*x1, units.Complex)
        self.assertIsInstance(x1*x2, units.Complex)

        # Unit/Value/ValueArray times array
        self.assertIsInstance(x1*a, units.ValueArray)
        self.assertIsInstance(x2*a, units.ValueArray)
        self.assertIsInstance(GHz*a, units.ValueArray)
        self.assertIsInstance(va*a, units.ValueArray)

        # Unit/Value/ValueArray times ValueArray
        self.assertIsInstance(x1*va, units.ValueArray)
        self.assertIsInstance(x2*va, units.ValueArray)
        self.assertIsInstance(GHz*va, units.ValueArray)
        self.assertIsInstance(va*va, units.ValueArray)

        # array times ?
        self.assertIsInstance(a*x1, units.ValueArray)
        self.assertIsInstance(a*x2, units.ValueArray)
        self.assertIsInstance(a*GHz, units.ValueArray)
        self.assertIsInstance(a*va, units.ValueArray)

        # ValueArray times ?
        self.assertIsInstance(va*x1, units.ValueArray)
        self.assertIsInstance(va*x2, units.ValueArray)
        self.assertIsInstance(va*GHz, units.ValueArray)
        self.assertIsInstance(va*a, units.ValueArray)

    def testComparison(self):
        s = units.Unit('s')
        ms = units.Unit('ms')
        kg = units.Unit('kg')
        self.assertTrue(1*s > 10*ms, '1*s > 10*ms')
        self.assertTrue(1*s >= 10*ms, '1*s >= 10*ms')
        self.assertTrue(1*s < 10000*ms, '1*s > 10000*ms')
        self.assertTrue(1*s <= 10000*ms, '1*s >= 10000*ms')
        self.assertTrue(10*ms < 1*s, '10*ms < 1*s')
        self.assertTrue(10*ms <= 1*s, '10*ms <= 1*s')
        self.assertTrue(10000*ms > 1*s, '10000*ms < 1*s')
        self.assertTrue(10000*ms >= 1*s, '10000*ms <= 1*s')
        with self.assertRaises(TypeError):
            nogood = 1*s > 1*kg

        self.assertFalse(1*s == 1*kg)
        self.assertTrue(0*s == 0)
        self.assertTrue(4*s > 0)
        with self.assertRaises(TypeError): _ = 4*s > 1
    
    def testComplex(self):
        V = units.Unit('V')

        self.assertTrue(1j*V != 1.0*V)
        self.assertTrue(1j*V == 1.0j*V)
        self.assertTrue(1.0*V == (1+0j)*V)
        with self.assertRaises(TypeError): _ = 1.0j*V < 2j*V

    def testDimensionless(self):
        ns = units.Unit('ns')
        GHz = units.Unit('GHz')

        self.assertTrue(isinstance((5*ns)*(5*GHz), float))
        self.assertTrue(hasattr((5*ns)*(5*GHz), 'inUnitsOf'))
        self.assertTrue( ((5*ns)*(5*GHz)).isDimensionless() )
        self.assertTrue( (5*ns)*(5*GHz) < 50 )
        self.assertTrue(isinstance(units.WithUnit(5.0, ''), units.DimensionlessFloat))
        
        self.assertTrue((5*ns*5j*GHz) == 25j)
        self.assertTrue((5*ns*5j*GHz).isDimensionless())

if __name__ == "__main__":
    unittest.main()
