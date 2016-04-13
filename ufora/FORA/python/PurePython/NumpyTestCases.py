#   Copyright 2015 Ufora Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import numpy
import numpy.testing
import random
import time
import pandas
import pyfora.pure_modules.pure_pandas as pure_pandas
import ufora.test.PerformanceTestReporter as PerformanceTestReporter


class NumpyTestCases(object):
    @staticmethod
    def compareButDontCheckTypes(x, y):
        if isinstance(x, basestring) and isinstance(y, basestring):
            return x == y

        if hasattr(x, '__len__') and hasattr(y, '__len__'):
            l1 = len(x)
            l2 = len(y)
            if l1 != l2:
                return False
            for idx in range(l1):
                if not NumpyTestCases.compareButDontCheckTypes(x[idx], y[idx]):
                    return False
            return True
        else:
            return x == y

    def test_numpy(self):
        n = numpy.zeros(10)
        def f():
            return n.shape
        self.equivalentEvaluationTest(f)

    def test_empty_array_ctor(self):
        def f():
            return numpy.array([])

        self.equivalentEvaluationTest(f)

    def test_repeated_array_ctor(self):
        x = numpy.array([[1,2],[3,4]])
        def f():
            return numpy.array(x)

        self.equivalentEvaluationTest(f)

    def test_numpy_pinverse_2(self):
        numpy.random.seed(42)

        def f(array):
            return numpy.linalg.pinv(array)

        arr = numpy.random.rand(20, 10) * 1000
        t1 = time.time()
        r1 = self.evaluateWithExecutor(f, arr)
        t2 = time.time()
        r2 = f(arr)
        t3 = time.time()
        print t3 - t2, t2 - t1
        self.assertArraysAreAlmostEqual(r1, r2)

    def test_numpy_pinverse_1(self):
        def f(arr):
            array = numpy.array(arr)
            return numpy.linalg.pinv(array)

        arr1 = [ [67.0, 63.0, 87.0],
                [77.0, 69.0, 59.0],
                [85.0, 87.0, 99.0],
                [15.0, 17.0, 19.0] ]

        r1 = self.evaluateWithExecutor(f, arr1)
        r2 = f(arr1)
        self.assertArraysAreAlmostEqual(r1, r2)

        arr2 = [ [1.0, 1.0, 1.0, 1.0],
            [5.0, 7.0, 7, 9] ]
        r1 = self.evaluateWithExecutor(f, arr2)
        r2 = f(arr2)
        self.assertArraysAreAlmostEqual(r1, r2)

    def test_numpy_transpose(self):
        def f():
            array = numpy.array([ [67.0, 63.0, 87.0],
                [77.0, 69.0, 59.0],
                [85.0, 87.0, 99.0],
                [15.0, 17.0, 19.0] ])

            return array.transpose()
        self.equivalentEvaluationTest(f)


        def f2():
            arr = numpy.array([[[67.0], [87.0]], [[69.0], [85.0]], [[69.0], [15.0]]])

            return arr.transpose()
        self.equivalentEvaluationTest(f2)


        def f3():
            arr = numpy.array([1.0, 2.0, 3.0, 4.0, 5.0])

            return arr.transpose()
        self.equivalentEvaluationTest(f3)

    def test_numpy_indexing_1(self):
        def f():
            array = numpy.array([ [67.0, 63.0, 87.0],
                [77.0, 69.0, 59.0],
                [85.0, 87.0, 99.0],
                [15.0, 17.0, 19.0] ])

            toReturn = []
            l = len(array)
            l2 = len(array[0])
            for x in range(l):
                for y in range(l2):
                    toReturn = toReturn + [array[x][y]]
            return toReturn

        self.equivalentEvaluationTest(
            f, comparisonFunction=NumpyTestCases.compareButDontCheckTypes
            )

    def test_numpy_indexing_2(self):
        def f():
            arr = numpy.array([ 67.0, 63.0, 87.0, 77.0, 69.0, 59.0, 85.0, 87.0, 99.0 ])
            return (arr, arr[0], arr[1], arr[8])

        self.equivalentEvaluationTest(
            f, comparisonFunction=NumpyTestCases.compareButDontCheckTypes
            )

    def test_numpy_indexing_3(self):
        def f():
            arr = numpy.array([[[67.0, 63.0], [87.0, 77.0]], [[69.0, 59.0], [85.0, 87.0]]])
            return (arr, arr[0], arr[1], arr[1][0], arr[0][1][1])
        self.equivalentEvaluationTest(
            f, comparisonFunction=NumpyTestCases.compareButDontCheckTypes)

        def f2():
            arr = numpy.array([[[67.0], [87.0]], [[69.0], [85.0]], [[69.0], [15.0]]])
            return (arr, arr[0], arr[1], arr[1][0], arr[2][1][0])

        self.equivalentEvaluationTest(
            f2, comparisonFunction=NumpyTestCases.compareButDontCheckTypes)

        def f3():
            arr = numpy.array([[[[67.0, 63.0], [87.0, 77.0]], [[69.0, 59.0], [85.0, 87.0]]], \
                               [[[67.0, 63.0], [87.0, 77.0]], [[69.0, 59.0], [85.0, 87.0]]]])
            return (arr, arr[0], arr[1], arr[1][0], arr[0][1][1], arr[0][1][1][1])

        self.equivalentEvaluationTest(
            f3, comparisonFunction=NumpyTestCases.compareButDontCheckTypes)

    def test_return_numpy(self):
        n = numpy.zeros(10)
        def f():
            return n
        res = self.evaluateWithExecutor(f)

        self.assertTrue(isinstance(res, numpy.ndarray), res)

        self.equivalentEvaluationTest(f)

    def test_numpy_flatten(self):
        def f(lists):
            b = numpy.array(lists)
            return b.flatten()
        a = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        self.equivalentEvaluationTest(f, a)

        b = [[67.0, 63, 87],
               [77, 69, 59],
               [85, 87, 99],
               [79, 72, 71],
               [63, 89, 93],
               [68, 92, 78]]
        self.equivalentEvaluationTest(f, b)

        c = [[[[67.0, 63.0], [87.0, 77.0]], [[69.0, 59.0], [85.0, 87.0]]], \
             [[[67.0, 63.0], [87.0, 77.0]], [[69.0, 59.0], [85.0, 87.0]]]]

        self.equivalentEvaluationTest(f, c)

    def test_numpy_arrays_are_iterable(self):
        def f():
            array = numpy.array([[67, 63, 87],
               [77, 69, 59],
               [85, 87, 99],
               [79, 72, 71],
               [63, 89, 93],
               [68, 92, 78]])
            toReturn = []
            for val in array:
                toReturn = toReturn + [val]
            return toReturn

        self.equivalentEvaluationTest(f)

    def test_numpy_tolist(self):
        def f(lists):
            b = numpy.array(lists)
            return b.tolist()
        a = [1, 2, 3, 4, 5, 6]
        self.equivalentEvaluationTest(f, a)

        b = [[67, 63, 87],
             [77, 69, 59],
             [85, 87, 99],
             [79, 72, 71],
             [63, 89, 93],
             [68, 92, 78]]
        self.equivalentEvaluationTest(f, b)

        c = [[[[67.0, 63.0], [87.0, 77.0]], [[69.0, 59.0], [85.0, 87.0]]], \
             [[[67.0, 63.0], [87.0, 77.0]], [[69.0, 59.0], [85.0, 87.0]]]]
        self.equivalentEvaluationTest(f, c)

    def test_numpy_dot_product_1a(self):
        random.seed(43)

        listLength = 20
        def f(arr1, arr2):
            return numpy.dot(arr1, arr2)

        for _ in range(10):
            x1 = [random.uniform(-10, 10) for _ in range(0, listLength)]
            x2 = [random.uniform(-10, 10) for _ in range(0, listLength)]

            self.equivalentEvaluationTest(
                f, x1, x2,
                comparisonFunction=numpy.isclose
                )

    def test_numpy_dot_product_1b(self):
        random.seed(43)

        listLength = 20
        def f(arr1, arr2):
            return arr1.dot(arr2)

        for _ in range(10):
            x1 = numpy.array([
                random.uniform(-10, 10) for _ in range(0, listLength)])
            x2 = [random.uniform(-10, 10) for _ in range(0, listLength)]

            self.equivalentEvaluationTest(
                f, x1, x2,
                comparisonFunction=numpy.isclose
                )

    def test_numpy_dot_product_2a(self):
        random.seed(44)

        listLength = 20

        arr1 = [random.uniform(-10, 10) for _ in range(0, listLength)]
        arr2 = [random.uniform(-10, 10) for _ in range(0, listLength)]

        def f():
            a = numpy.array(arr1)
            b = numpy.array(arr2)

            return numpy.dot(a, b)

        r1 = self.evaluateWithExecutor(f)
        r2 = f()

        numpy.testing.assert_allclose(r1, r2)

    def test_numpy_dot_product_2b(self):
        random.seed(44)

        listLength = 20

        arr1 = [random.uniform(-10, 10) for _ in range(0, listLength)]
        arr2 = [random.uniform(-10, 10) for _ in range(0, listLength)]

        def f():
            a = numpy.array(arr1)
            b = numpy.array(arr2)

            return a.dot(b)

        r1 = self.evaluateWithExecutor(f)
        r2 = f()

        numpy.testing.assert_allclose(r1, r2)

    def test_numpy_dot_product_3a(self):
        def f():
            m1 = numpy.array([1.0, 2, 3, 4, 5, 6])
            m2 = numpy.array([[67.0, 63, 87],
                       [77, 69, 59],
                       [85, 87, 99],
                       [79, 72, 71],
                       [63, 89, 93],
                       [68, 92, 78]])
            return numpy.dot(m1, m2)
        self.equivalentEvaluationTest(f)

    def test_numpy_dot_product_3b(self):
        def f():
            m1 = numpy.array([1.0, 2, 3, 4, 5, 6])
            m2 = numpy.array([[67.0, 63, 87],
                       [77, 69, 59],
                       [85, 87, 99],
                       [79, 72, 71],
                       [63, 89, 93],
                       [68, 92, 78]])
            return m1.dot(m2)
        self.equivalentEvaluationTest(f)

    def test_numpy_dot_product_4a(self):
        def f():
            m1 = numpy.array([1.0, 2, 3])
            m2 = numpy.array([[67.0, 63, 87],
                       [77, 69, 59],
                       [85, 87, 99],
                       [79, 72, 71],
                       [63, 89, 93],
                       [68, 92, 78]])
            return numpy.dot(m2, m1)
        self.equivalentEvaluationTest(f)

    def test_numpy_dot_product_4b(self):
        def f():
            m1 = numpy.array([1.0, 2, 3])
            m2 = numpy.array([[67.0, 63, 87],
                       [77, 69, 59],
                       [85, 87, 99],
                       [79, 72, 71],
                       [63, 89, 93],
                       [68, 92, 78]])
            return numpy.dot(m2, m1)
        self.equivalentEvaluationTest(f)

    def test_numpy_dot_product_4c(self):
        def f():
            m1 = [1.0, 2, 3]
            m2 = numpy.array([[67.0, 63, 87],
                       [77, 69, 59],
                       [85, 87, 99],
                       [79, 72, 71],
                       [63, 89, 93],
                       [68, 92, 78]])
            return numpy.dot(m2, m1)
        self.equivalentEvaluationTest(f)

    def test_numpy_dot_product_5a(self):
        x = numpy.array([[1,2],[3,4]])
        y = numpy.array([1,2,3])

        with self.assertRaises(ValueError):
            with self.create_executor() as fora:
                with fora.remotely:
                    numpy.dot(y, x)

    def test_numpy_dot_product_5a(self):
        x = numpy.array([[1,2],[3,4]])
        y = numpy.array([1,2,3])

        with self.assertRaises(ValueError):
            with self.create_executor() as fora:
                with fora.remotely:
                    numpy.dot(y, x)

    def test_numpy_dot_product_5b(self):
        x = numpy.array([[1,2],[3,4]])
        y = numpy.array([1,2,3])

        with self.assertRaises(ValueError):
            with self.create_executor() as fora:
                with fora.remotely:
                    y.dot(x)

    def test_numpy_matrix_multiplication_1a(self):
        def f():
            m1 = numpy.array([ [67.0, 63, 87],
                       [77, 69, 59],
                       [85, 87, 99],
                       [79, 72, 71],
                       [63, 89, 93],
                       [68, 92, 78] ])
            m2 = m1.transpose()

            return numpy.dot(m1, m2)
        r1 = self.evaluateWithExecutor(f)
        r2 = f()
        self.assertArraysAreAlmostEqual(r1, r2)

    def test_numpy_matrix_multiplication_1b(self):
        def f():
            m1 = numpy.array([ [67.0, 63, 87],
                       [77, 69, 59],
                       [85, 87, 99],
                       [79, 72, 71],
                       [63, 89, 93],
                       [68, 92, 78] ])
            m2 = m1.transpose()

            return numpy.dot(m1, m2)
        r1 = self.evaluateWithExecutor(f)
        r2 = f()
        self.assertArraysAreAlmostEqual(r1, r2)

    def test_numpy_matrix_multiplication_misaligned_1(self):
        m1 = numpy.array([[1,2], [3,4]])
        m2 = numpy.array([[1,2], [3,4], [5,6]])

        with self.assertRaises(ValueError):
            with self.create_executor() as fora:
                with fora.remotely:
                    numpy.dot(m1, m2)

    def test_numpy_matrix_multiplication_misaligned_2(self):
        m1 = numpy.array([1,2, 3,4])
        m2 = numpy.array([[1,2], [3,4], [5,6]])

        with self.assertRaises(ValueError):
            with self.create_executor() as fora:
                with fora.remotely:
                    numpy.dot(m1, m2)

    def test_numpy_reshape(self):
        def f(newShape):
            m1 = numpy.array([
                [67.0, 63, 87],
                [77, 69, 59],
                [85, 87, 99],
                [79, 72, 71],
                [63, 89, 93],
                [68, 92, 78] ])
            return m1.reshape(newShape)

        self.equivalentEvaluationTest(f, (1, 18))
        self.equivalentEvaluationTest(f, (2, 9))
        self.equivalentEvaluationTest(f, (3, 6))
        self.equivalentEvaluationTestThatHandlesExceptions(f, (1, 1))

    def test_numpy_matrix_division(self):
        random.seed(44)

        matrix = numpy.array([ [67, 63, 87],
                       [77, 69, 59],
                       [85, 87, 99],
                       [79, 72, 71],
                       [63, 89, 93],
                       [68, 92, 78] ])

        for _ in range(10):
            def f(x):
                return matrix / x
            self.equivalentEvaluationTest(f, random.uniform(-10, 10))

            def f2(x):
                return matrix * x
            self.equivalentEvaluationTest(f2, random.uniform(-10, 10))

            def f3(x):
                return matrix + x
            self.equivalentEvaluationTest(f3, random.uniform(-10, 10))

            def f4(x):
                return matrix - x
            self.equivalentEvaluationTest(f4, random.uniform(-10, 10))

            def f5(x):
                return matrix ** x
            self.equivalentEvaluationTest(f5, random.uniform(-10, 10))

    def test_numpy_make_array(self):
        def f():
            return numpy.zeros(10)

        self.equivalentEvaluationTest(f)

    def test_numpy_addition_1(self):
        def f():
            x1 = numpy.array([[1,2],[3,4]])
            x2 = numpy.array([[8,7],[6,5]])

            return x1 + x2

        self.equivalentEvaluationTest(f)

    def test_numpy_binary_ops(self):
        def f():
            x1 = numpy.array([[1,2],[3,4]])
            x2 = numpy.array([[8,7],[6,5]])

            return (x1 / x2) ** 2 - x2 ** x2

        self.equivalentEvaluationTest(f)

    def test_numpy_addition_2(self):
        def f():
            x1 = numpy.array([[1,2],[3,4]])
            x2 = numpy.array([[8,7,5,6]])

            return x1 + x2

        with self.assertRaises(ValueError):
            with self.create_executor() as fora:
                with fora.remotely:
                    f()

    def test_numpy_arange(self):

        def f():
            return numpy.arange(-1,.9,.2)
        r1 = self.evaluateWithExecutor(f)
        r2 = f()
        self.assertArraysAreAlmostEqual(r1, r2)

    def test_numpy_zeros_1(self):
        def f():
            return numpy.zeros((10, 2))

        self.equivalentEvaluationTest(f)

    def test_numpy_zeros_2(self):
        def f():
            return numpy.zeros(10)

        self.equivalentEvaluationTest(f)

    def test_numpy_linsolve_1(self):
        a = numpy.array([[-2.0, 3.0], [4.0, 7.0]])
        b = numpy.array([[1.0], [2.0]])

        def f():
            return numpy.linalg.solve(a, b)

        self.equivalentEvaluationTest(f)

    def test_numpy_linsolve_2(self):
        a = numpy.array([[-2.0, 3.0], [-2.0, 3.0]])
        b = numpy.array([[1.0], [2.0]])

        def f():
            return numpy.linalg.solve(a, b)

        try:
            self.evaluateWithExecutor(f)
            self.assertTrue(False)
        except:
            # just see that we get an exception here without dying.
            # we're not wrapping the numpy linalg errors yet
            pass

    def test_numpy_linsolve_3(self):
        a = numpy.array([[-2.0, 3.0], [4.0, 7.0]])
        b = numpy.array([1.0, 2.0])

        def f():
            return numpy.linalg.solve(a, b)

        self.equivalentEvaluationTest(f)

    def test_numpy_slicing_1(self):
        size = 3
        def f(lowIx, highIx):
            x = numpy.array(range(size))
            return x[lowIx:highIx]

        for ix in range(size):
            for jx in range(size):
                self.equivalentEvaluationTest(f, ix, jx)

    def test_numpy_eq(self):
        x = numpy.array([1,2,3])
        y = numpy.array([1,0,2])
        def f():
            return x == y

        self.equivalentEvaluationTest(f)

    def test_numpy_isnan(self):
        def f(x):
            return [numpy.isnan(elt) for elt in x]

        vals = [1, 2.0, numpy.nan, numpy.inf, -numpy.nan]
        numpy.testing.assert_allclose(
            f(vals),
            self.evaluateWithExecutor(f, vals)
            )

    def test_numpy_isinf_1(self):
        def f(x):
            return [numpy.isnan(elt) for elt in x]

        vals = [1, 2.0, numpy.nan, numpy.inf, -numpy.nan]
        numpy.testing.assert_allclose(
            f(vals),
            self.evaluateWithExecutor(f, vals)
            )

    def test_numpy_isinf_2(self):
        def f(x):
            return numpy.isinf(x)

        arrays = [numpy.array([1.0, 2.0]),
                  numpy.array([[1.0,2.0],[numpy.inf,3.0]])]

        for array in arrays:
            numpy.testing.assert_array_equal(
                f(array),
                self.evaluateWithExecutor(f, array)
                )

    def test_numpy_isfinite_1(self):
        def f(x):
            return [numpy.isnan(elt) for elt in x]

        vals = [1, 2.0, numpy.nan, numpy.inf, -numpy.nan]
        numpy.testing.assert_allclose(
            f(vals),
            self.evaluateWithExecutor(f, vals)
            )

    def test_numpy_isfinite_2(self):
        def f(x):
            return numpy.isfinite(x)

        arrays = [numpy.array([1.0, 2.0]),
                  numpy.array([[1.0,2.0],[numpy.inf,3.0]])]

        for array in arrays:
            numpy.testing.assert_array_equal(
                f(array),
                self.evaluateWithExecutor(f, array)
                )

    def test_numpy_all_1(self):
        def f(x):
            return numpy.all(x)

        array = [1, 2.0, 0.0, True, False, numpy.nan, numpy.inf, -numpy.inf]

        for val in array:
            self.assertEqual(
                f(val),
                self.evaluateWithExecutor(f, val)
                )

    def test_numpy_all_2(self):
        def f(x):
            return numpy.all(x)

        array = [1, 2.0, 0.0, True, False, numpy.nan, numpy.inf, -numpy.inf]

        for ix in range(len(array)):
            sliced_array = array[:ix]
            self.assertEqual(
                f(sliced_array),
                self.evaluateWithExecutor(f, sliced_array),
                msg=str(sliced_array)
                )
        
    def check_svd(self, x):
        def svd(a):
            return numpy.linalg.svd(a)

        pyforaRes = self.evaluateWithExecutor(svd, x)
        numpyRes = svd(x)

        self.assertEqual(len(pyforaRes), len(numpyRes))

        for ix in xrange(len(pyforaRes)):
            numpy.testing.assert_allclose(
                pyforaRes[ix],
                numpyRes[ix]
                )

    def test_svd_1(self):
        self.check_svd(numpy.array([[1,3],[2,4]]))

    def test_isinstance_on_remote(self):
        from pyfora.pure_modules.pure_numpy import PurePythonNumpyArray

        with self.create_executor() as ufora:
            with ufora.remotely:
                a = numpy.array([[1,2],[3,4]])

            with ufora.remotely.downloadAll():
                res = isinstance(a, PurePythonNumpyArray)

            self.assertTrue(res)

    def test_norm_1(self):
        def f(x):
            return numpy.linalg.norm(x)

        x = numpy.array([1,2,3,4])

        self.assertEqual(
            f(x),
            self.evaluateWithExecutor(f, x)
            )

        x = x.reshape((2,2))

        self.assertEqual(
            f(x),
            self.evaluateWithExecutor(f, x)
            )

    def check_lstsq(self, a, b):
        def f():
            return numpy.linalg.lstsq(a, b)

        x1, resid1, rank1, sing1 = f()

        print f()

        x2, resid2, rank2, sing2 = self.evaluateWithExecutor(f)

        numpy.testing.assert_allclose(x1, x2)
        numpy.testing.assert_almost_equal(resid1, resid2)
        numpy.testing.assert_allclose(rank1, rank2)
        numpy.testing.assert_allclose(sing1, sing2)

    def test_lstsq_1(self):
        a = numpy.array([[1., 2.], [3., 4.], [5., 6.]])
        b = numpy.array([2., 1., 3.])

        self.check_lstsq(a, b)

    def test_lstsq_2(self):
        a = numpy.array([[1., 2., 3.], [3., 4., 6.]])
        b = numpy.array([2., 1.])

        self.check_lstsq(a, b)

    def test_numpy_eye(self):
        def f(nRows, nColumns):
            return numpy.eye(nRows, nColumns)

        self.equivalentEvaluationTest(f, 2, 2)
        self.equivalentEvaluationTest(f, 2, 4)
        self.equivalentEvaluationTest(f, 5, 3)

    def test_numpy_inv_1(self):
        def f(x):
            return numpy.linalg.inv(x)

        x = numpy.array([[1,2],[3,4]])

        numpy.testing.assert_allclose(
            f(x),
            self.evaluateWithExecutor(f, x)
            )

    def test_numpy_inv_2(self):
        def f(x):
            return numpy.linalg.inv(x)
            
        x = numpy.array([[1,1],[1,1]])

        try:
            self.evaluateWithExecutor(f, x)
        except Exception as e:
            self.assertEqual(
                e.remoteException.message,
                "matrix was singular"
                )
            return

        self.assertTrue(False)

    def test_numpy_eigh_1(self):
        def f(x, uplo='L'):
            return numpy.linalg.eigh(x)

        x = numpy.array([[2,1],[1,1]])

        res1 = f(x)
        res2 = self.evaluateWithExecutor(f, x)
        
        numpy.testing.assert_allclose(res1[0], res2[0])
        numpy.testing.assert_allclose(res1[1], res1[1])

    def test_numpy_abs(self):
        def f(x):
            return numpy.abs(x)

        x = numpy.array([[-2.0,1.0],[-3.0,0.0]])

        self.equivalentEvaluationTest(f, x)

    def test_dataframe_dot_perf_1(self):
        with self.create_executor() as executor:
            with executor.remotely:
                df, vec = generate_data(1000000, 20)
                
            def loop(ct):
                res = 0
                for ix in xrange(ct):
                    res = res + df.dot(vec)[ix % len(df)]

                return res

            @PerformanceTestReporter.PerfTest("pyfora.pure_pandas.dot_perf_1")
            def test():
                self.evaluateWithExecutor(loop, 100)

            test()

    def test_dataframe_dot_new_perf_1(self):
        with self.create_executor() as executor:
            with executor.remotely:
                df, vec = generate_data(200000, 100)

            print "Generating locally."

            df_local, vec_local = generate_data_local(200000, 100)

            print "Starting."
                
            def loop(ct):
                res = 0
                for ix in xrange(ct):
                    res = res + dot_new(df, vec)[0]

                return res

            def loop_local(ct):
                res = 0
                for ix in xrange(ct):
                    res = res + df_local.dot(vec_local)[0]

                return res

            self.evaluateWithExecutor(loop, 50)

            with PerformanceTestReporter.RecordAsPerfTest("pyfora.pure_pandas.dot_perf_unrolled.pyfora"):
                self.evaluateWithExecutor(loop, 50)

            with PerformanceTestReporter.RecordAsPerfTest("pyfora.pure_pandas.dot_perf_unrolled.native"):
                loop_local(50)

            
def dot_new(df, vec):
    assert df.shape[1] == len(vec)

    res = []
    jx = 0
    jx2 = 1
    jx3 = 2
    jx4 = 3
    jx5 = 4
    jx6 = 5
    jx7 = 6
    jx8 = 7
    jx_max = len(df)
    while jx8 < jx_max:
        acc = 0.0
        acc2 = 0.0
        acc3 = 0.0
        acc4 = 0.0
        acc5 = 0.0
        acc6 = 0.0
        acc7 = 0.0
        acc8 = 0.0
        ix = 0
        ix_max = len(vec)
        while ix < ix_max:
            v = vec[ix]
            acc = acc + df._columns[ix][jx] * v
            acc2 = acc2 + df._columns[ix][jx2] * v
            acc3 = acc3 + df._columns[ix][jx3] * v
            acc4 = acc4 + df._columns[ix][jx4] * v
            acc5 = acc5 + df._columns[ix][jx5] * v
            acc6 = acc6 + df._columns[ix][jx6] * v
            acc7 = acc7 + df._columns[ix][jx7] * v
            acc8 = acc8 + df._columns[ix][jx8] * v
            ix = ix + 1
        res = res + [acc] + [acc2] + [acc3] + [acc4] + [acc5] + [acc6] + [acc7] + [acc8]
        jx = jx + 8
        jx2 = jx2 + 8
        jx3 = jx3 + 8
        jx4 = jx4 + 8
        jx5 = jx5 + 8
        jx6 = jx6 + 8
        jx7 = jx7 + 8
        jx8 = jx8 + 8

    return res

    return pure_pandas.PurePythonSeries([
        sum(df._columns[ix][jx] * vec[ix] + 12341234.0 for ix in xrange(len(vec))) \
        for jx in xrange(len(df))
        ])

def dot_new_single(df, vec):
    assert df.shape[1] == len(vec)

    res = []
    jx = 0
    jx_max = len(df)
    while jx < jx_max:
        acc = 0.0
        ix = 0
        ix_max = len(vec)
        while ix < ix_max:
            acc = acc + df._columns[ix][jx] * vec[ix]
            ix = ix + 1
        res = res + [acc]
        jx = jx + 1

    return res

    return pure_pandas.PurePythonSeries([
        sum(df._columns[ix][jx] * vec[ix] + 12341234.0 for ix in xrange(len(vec))) \
        for jx in xrange(len(df))
        ])

            
def dot_new_sumform(df, vec):
    return pure_pandas.PurePythonSeries([
        sum(df._columns[ix][jx] * vec[ix] + 12341234.0 for ix in xrange(len(vec))) \
        for jx in xrange(len(df))
        ])

def generate_data(nRows, nColumns):
    df = pure_pandas.PurePythonDataFrame(
        [[float(rowIx % (colIx + 2)) for rowIx in xrange(nRows)] \
         for colIx in xrange(nColumns)]
        )

    vec = [float(rowIx) for rowIx in xrange(nColumns)]

    return df, vec

def generate_data_local(nRows, nColumns):
    df = pandas.DataFrame(
        [[float(rowIx % (colIx + 2)) for colIx in xrange(nColumns)]
          for rowIx in xrange(nRows)]
        )

    vec = [float(rowIx) for rowIx in xrange(nColumns)]

    return df, vec

