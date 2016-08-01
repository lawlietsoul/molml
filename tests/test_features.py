import unittest

import numpy

from molml.features import BagOfBonds, Connectivity, CoulombMatrix


METHANE_COORDS = '''
0.99826008 -0.00246000 -0.00436000
2.09021016 -0.00243000 0.00414000
0.63379005 1.02686007 0.00414000
0.62704006 -0.52773003 0.87811010
0.64136006 -0.50747003 -0.90540005
'''
METHANE_COORDS = numpy.array([map(float,x.split()) for x in METHANE_COORDS.strip().split('\n')])
METHANE_ELEMENTS = "C H H H H".strip().split()
METHANE = (METHANE_ELEMENTS, METHANE_COORDS)


BIG_COORDS = '''
-4.577500 -2.027000 0.000100
-3.170600 -2.027000 0.000100
-2.503900 -0.800400 0.000100
-3.258000 0.374300 -0.000100
-4.661200 0.271500 -0.000300
-5.320700 -0.903400 -0.000100
-1.405400 -0.760700 -0.000900
-2.513500 -3.148700 0.000400
-5.243115 -3.143726 0.000200
-4.629817 -3.882282 0.000225
-2.684596 1.541008 -0.000300
-5.814138 1.919458 1.213487
-5.406518 1.336626 -0.000400
-5.819921 1.927685 -1.195717
-6.619470 3.070525 -1.138918
-6.975346 3.579026 0.123745
-6.585259 3.021652 1.286714
-5.522105 1.500109 -2.163583
-5.454672 1.405691 2.352323
-4.624597 1.797860 2.632999
-7.030464 3.657794 -2.223500
-6.076905 4.646253 -2.621712
-6.415463 5.129236 -3.514470
-5.968814 5.371844 -1.842713
-5.132915 4.177431 -2.805889
-7.718078 4.640805 0.228360
-9.070199 4.905679 0.160311
-9.224797 6.330336 0.368614
-7.956294 6.841725 0.550312
-7.010267 5.819401 0.468316
-10.036777 4.061817 -0.048549
-10.929896 3.282089 -0.241536
-11.725464 2.587525 -0.413445
-11.347485 7.546787 0.385857
-10.352686 6.976697 0.377776
-7.456659 8.559162 2.073165
-7.456094 8.020721 0.773377
-6.908266 8.779686 -0.262429
-6.384356 10.039584 0.032126
-6.430989 10.491699 1.363650
-6.955556 9.772640 2.375141
-6.890997 8.392509 -1.291057
-5.955912 11.657573 1.687608
-7.955339 7.890595 3.070357
-8.953881 7.917520 3.023573
-7.644961 6.941155 3.023569
-5.863480 10.784819 -0.897020
-5.382191 11.473417 -1.755551
-4.953470 12.086803 -2.520310
'''
BIG_COORDS = numpy.array([map(float,x.split()) for x in BIG_COORDS.strip().split('\n')])
BIG_ELEMENTS = "C C C C C N H H O H H C C C C C N H O H O C H H H C C C C O C C H N C C C C C C N H H N H H C C H".strip().split()
BIG = (BIG_ELEMENTS, BIG_COORDS)


MID_COORDS = '''
-4.577500 -2.027000 0.000100
-3.170600 -2.027000 0.000100
-2.503900 -0.800400 0.000100
-3.258000 0.374300 -0.000100
-4.661200 0.271500 -2.000300
-5.320700 -0.903400 -2.000100
-4.661200 0.271500 -4.000300
-5.320700 -0.903400 -5.000100
-5.320700 -0.903400 -6.000100
'''
MID_COORDS = numpy.array([map(float,x.split()) for x in MID_COORDS.strip().split('\n')])
MID_ELEMENTS = '''C C O O O O H H H'''.strip().split()
MID = (MID_ELEMENTS, MID_COORDS)

ALL_DATA = [METHANE, MID, BIG]



class ConnectivityTest(unittest.TestCase):
    def test_fit_atom(self):
        a = Connectivity(depth=1)
        a.fit(ALL_DATA)
        self.assertEqual(a._base_chains, 
                        set([('N',), ('C',), ('O',), ('H',)]))

    def test_fit_bond(self):
        a = Connectivity(depth=2)
        a.fit(ALL_DATA)
        self.assertEqual(a._base_chains, 
                        set([('H', 'O'), ('C', 'H'), ('H', 'N'), ('C', 'C'), 
                            ('H', 'H'), ('O', 'O'), ('C', 'N'), ('C', 'O')]))

    def test_fit_angle(self):
        a = Connectivity(depth=3)
        a.fit(ALL_DATA)
        self.assertEqual(a._base_chains, 
                        set([('H', 'N', 'H'), ('C', 'N', 'H'), ('C', 'C', 'O'),
                            ('N', 'C', 'N'), ('C', 'O', 'C'), ('C', 'N', 'C'),
                            ('H', 'C', 'H'), ('C', 'O', 'H'), ('C', 'C', 'C'), 
                            ('C', 'C', 'H'), ('H', 'C', 'O'), ('N', 'C', 'O'), 
                            ('H', 'C', 'N'), ('C', 'C', 'N')]))
        
    def test_fit_dihedral(self):
        # This is to test the double order flipping (CCCH vs HCCC)
        a = Connectivity(depth=4)
        a.fit(ALL_DATA)
        self.assertEqual(a._base_chains,
                        set([('N', 'C', 'N', 'C'), ('C', 'C', 'C', 'O'), 
                            ('H', 'C', 'O', 'C'), ('H', 'C', 'C', 'N'), 
                            ('H', 'C', 'N', 'C'), ('N', 'C', 'C', 'O'), 
                            ('C', 'C', 'C', 'N'), ('H', 'C', 'C', 'H'), 
                            ('C', 'C', 'N', 'C'), ('O', 'C', 'N', 'C'), 
                            ('C', 'C', 'O', 'C'), ('C', 'C', 'C', 'H'), 
                            ('C', 'C', 'C', 'C'), ('H', 'C', 'C', 'O'), 
                            ('C', 'C', 'N', 'H'), ('N', 'C', 'O', 'H'), 
                            ('C', 'C', 'O', 'H'), ('N', 'C', 'N', 'H')]))

    def test_fit_atom_bond(self):
        # This should be the exact same thing as doing it with use_bond_order=False
        a = Connectivity(depth=1, use_bond_order=True)
        a.fit(ALL_DATA)
        self.assertEqual(a._base_chains, 
                        set([('N',), ('C',), ('O',), ('H',)]))
        

    def test_fit_bond_bond(self):
        a = Connectivity(depth=2, use_bond_order=True)
        a.fit(ALL_DATA)
        self.assertEqual(a._base_chains, 
                        set([(('H', 'N', '1'),), (('C', 'N', '3'),), 
                            (('H', 'O', '1'),), (('H', 'H', '1'),), 
                            (('C', 'H', '1'),), (('O', 'O', '1'),), 
                            (('C', 'N', '2'),), (('C', 'O', '1'),), 
                            (('C', 'C', '3'),), (('C', 'N', 'Ar'),), 
                            (('C', 'C', '1'),), (('C', 'O', 'Ar'),), 
                            (('C', 'C', '2'),), (('C', 'C', 'Ar'),)]))

    def test_transform(self):
        a = Connectivity()
        a.fit(ALL_DATA)
        expected_results = numpy.array([[ 0,  1,  0,  4],
                                        [ 0,  2,  3,  2],
                                        [ 5, 25,  4, 15]])
        self.assertTrue((a.transform(ALL_DATA) == expected_results).all())

    def test_small_to_large_transform(self):
        a = Connectivity()
        a.fit([METHANE])
        expected_results = numpy.array([[ 1,  4],
                                        [ 2,  2],
                                        [25, 15]])
        self.assertTrue((a.transform(ALL_DATA) == expected_results).all())

    def test_large_to_small_transform(self):
        a = Connectivity()
        a.fit([BIG])
        expected_results = numpy.array([[ 0,  1,  0,  4],
                                        [ 0,  2,  3,  2],
                                        [ 5, 25,  4, 15]])
        self.assertTrue((a.transform(ALL_DATA) == expected_results).all())

    def test_transform_before_fit(self):
        a = Connectivity()
        with self.assertRaises(ValueError):
            a.transform(ALL_DATA)

    def test_fit_transform(self):
        a = Connectivity()
        expected_results = numpy.array([[ 0,  1,  0,  4],
                                        [ 0,  2,  3,  2],
                                        [ 5, 25,  4, 15]])
        self.assertTrue((a.fit_transform(ALL_DATA) == expected_results).all())


class CoulombMatrixTest(unittest.TestCase):
    def test_fit(self):
        a = CoulombMatrix()
        a.fit(ALL_DATA)
        self.assertEqual(a._max_size, 49)

    def test_transform(self):
        a = CoulombMatrix()
        a.fit([METHANE])
        expected_results = numpy.array([
            [  36.8581052 ,   5.49459021,   5.49462885,   5.4945    ,
                5.49031286,   5.49459021,   0.5       ,   0.56071947,
                0.56071656,   0.56064037,   5.49462885,   0.56071947,
                0.5       ,   0.56071752,   0.56064089,   5.4945    ,
                0.56071656,   0.56071752,   0.5       ,   0.56063783,
                5.49031286,   0.56064037,   0.56064089,   0.56063783,   
                0.5]])
        try:
            numpy.testing.assert_array_almost_equal(
                                        a.transform([METHANE]),
                                        expected_results)
        except AssertionError as e:
            self.fail(e)

    def test_small_to_large_transform(self):
        a = CoulombMatrix()
        a.fit([METHANE])
        with self.assertRaises(ValueError):
            a.transform(ALL_DATA)

    def test_large_to_small_transform(self):
        a = CoulombMatrix()
        a.fit([MID])

        expected_results = numpy.array([
            [ 36.8581052 ,   5.49459021,   5.49462885,   5.4945    ,
               5.49031286,   0.        ,   0.        ,   0.        ,
               0.        ,   5.49459021,   0.5       ,   0.56071947,
               0.56071656,   0.56064037,   0.        ,   0.        ,
               0.        ,   0.        ,   5.49462885,   0.56071947,
               0.5       ,   0.56071752,   0.56064089,   0.        ,
               0.        ,   0.        ,   0.        ,   5.4945    ,
               0.56071656,   0.56071752,   0.5       ,   0.56063783,
               0.        ,   0.        ,   0.        ,   0.        ,
               5.49031286,   0.56064037,   0.56064089,   0.56063783,
               0.5] + [0.0] * 40
        ])
        try:
            numpy.testing.assert_array_almost_equal(
                                        a.transform([METHANE]),
                                        expected_results)
        except AssertionError as e:
            self.fail(e)


    def test_transform_before_fit(self):
        a = CoulombMatrix()
        with self.assertRaises(ValueError):
            a.transform(ALL_DATA)

    def test_fit_transform(self):
        a = CoulombMatrix()
        expected_results = numpy.array([
            [  36.8581052 ,   5.49459021,   5.49462885,   5.4945    ,
                5.49031286,   5.49459021,   0.5       ,   0.56071947,
                0.56071656,   0.56064037,   5.49462885,   0.56071947,
                0.5       ,   0.56071752,   0.56064089,   5.4945    ,
                0.56071656,   0.56071752,   0.5       ,   0.56063783,
                5.49031286,   0.56064037,   0.56064089,   0.56063783,   
                0.5]])
        try:
            numpy.testing.assert_array_almost_equal(
                                        a.fit_transform([METHANE]),
                                        expected_results)
        except AssertionError as e:
            self.fail(e)



class BagOfBondsTest(unittest.TestCase):
    def test_fit(self):
        a = BagOfBonds()
        a.fit([METHANE])
        expected_results = {
            ('C', 'H'): 4, 
            ('H', 'H'): 6,
        }
        self.assertEqual(a._bag_sizes, expected_results)

    def test_fit_multi_mol(self):
        a = BagOfBonds()
        a.fit(ALL_DATA)
        expected_results = {
            ('H', 'O'): 60,
            ('C', 'H'): 375,
            ('H', 'N'): 75,
            ('C', 'C'): 300,
            ('H', 'H'): 105,
            ('O', 'O'): 6,
            ('C', 'N'): 125,
            ('N', 'O'): 20,
            ('C', 'O'): 100,
            ('N', 'N'): 10,
        }
        self.assertEqual(a._bag_sizes, expected_results)

    def test_transform(self):
        a = BagOfBonds()
        a.fit([METHANE])
        expected_results = numpy.array([
            [ 0.56071947,  0.56071752,  0.56071656,  0.56064089,  0.56064037,
              0.56063783,  5.49462885,  5.49459021,  5.4945    ,  5.49031286]
        ])
        try:
            numpy.testing.assert_array_almost_equal(
                                        a.transform([METHANE]),
                                        expected_results)
        except AssertionError as e:
            self.fail(e)

    def test_small_to_large_transform(self):
        a = BagOfBonds()
        a.fit([METHANE])
        with self.assertRaises(ValueError):
            a.transform(ALL_DATA)

    def test_large_to_small_transform(self):
        a = BagOfBonds()
        a.fit([BIG])

        expected_results = numpy.array([
            [0.0] * 60 + 
            [5.494628848219048, 5.494590213211275, 5.494499999706413, 
            5.49031286145183] +
            [0.0] * 746 +
            [0.5607194714171738, 0.5607175240809282, 0.5607165613824526, 
            0.5606408892793993, 0.5606403708987712, 0.560637829974531] + 
            [0.0] * 360
            ])
        try:
            numpy.testing.assert_array_almost_equal(
                                        a.transform([METHANE]),
                                        expected_results)
        except AssertionError as e:
            self.fail(e)

    def test_transform_before_fit(self):
        a = BagOfBonds()
        with self.assertRaises(ValueError):
            a.transform(ALL_DATA)



if __name__ == '__main__':
    unittest.main()