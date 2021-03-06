#!/usr/bin/env python3

import os
import lab
import json
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)

class TestGas(unittest.TestCase):
    def test_01(self):
        print("step(gas_3) example ... ", end="", flush=True)
        input = {"width": 3,
                 "state": [["w"], ["w"], ["w"], ["w"],
                           ["r", "l"], ["w"], ["w"], [],
                           ["w"], ["w"], ["d", "w"], ["w"]],
                 "height": 4}
        result = lab.step(input)
        expect = {"width": 3,
                  "state": [["w"], ["u", "w"], ["w"], ["w"],
                            [], ["w"], ["w"], ["u", "d"],
                            ["w"], ["w"], ["w"], ["w"]],
                  "height": 4}
        self.check_result(result, expect)

    def test_02(self):
        print("step(step(gas_3)) example ... ", end="", flush=True)
        input = {"width": 3,
                 "state": [["w"], ["u", "w"], ["w"], ["w"],
                           [], ["w"], ["w"], ["u", "d"],
                           ["w"], ["w"], ["w"], ["w"]],
                 "height": 4}
        result = lab.step(input)
        expect = {"width": 3,
                  "state": [["w"], ["w"], ["w"], ["w"],
                            ["d"], ["w"], ["l", "w"], [],
                            ["r", "w"], ["w"], ["w"], ["w"]],
                  "height": 4}
        self.check_result(result, expect)

    def test_03(self):
        descrip, input, expect = self.load_case('3')
        print(descrip, " ... ", end="", flush=True)
        result = lab.step(input)
        self.check_result(result, expect)

    def test_04(self):
        descrip, input, expect = self.load_case('4')
        print(descrip, " ... ", end="", flush=True)
        result = lab.step(input)
        self.check_result(result, expect)

    def test_05(self):
        descrip, input, expect = self.load_case('5')
        print(descrip, " ... ", end="", flush=True)
        result = lab.step(input)
        self.check_result(result, expect)

    def test_06(self):
        descrip, input, expect = self.load_case('6')
        print(descrip, " ... ", end="", flush=True)
        result = lab.step(input)
        self.check_result(result, expect)

    def test_07(self):
        descrip, input, expect = self.load_case('7')
        print(descrip, " ... ", end="", flush=True)
        result = lab.step(input)
        self.check_result(result, expect)

    def test_08(self):
        descrip, input, expect = self.load_case('8')
        print(descrip, " ... ", end="", flush=True)
        result = lab.step(input)
        self.check_result(result, expect)

    def test_09(self):
        descrip, input, expect = self.load_case('9')
        print(descrip, " ... ", end="", flush=True)
        result = lab.step(input)
        self.check_result(result, expect)

    def test_10(self):
        descrip, input, expect = self.load_case('10')
        print(descrip, " ... ", end="", flush=True)
        result = lab.step(input)
        self.check_result(result, expect)

    def test_11(self):
        descrip, input, expect = self.load_case('11')
        print(descrip, " ... ", end="", flush=True)
        result = lab.step(input)
        self.check_result(result, expect)

    def extra_test_all(self):
        for n in range(1, 12):
            with self.subTest(case=n):
                descrip, input, expect = self.load_case(str(n))
                print("  subTest:", descrip, "... ", flush=True)
                result = lab.step(input)
                self.check_result(result, expect)

    def test_my_01(self):
        # test step()
        input = {"width": 3,
                 "state": [["w"], [], [],
                           ["w", "l"], ['l', 'r'], [],
                           [], ["d"], []],
                 "height": 3}
        result = lab.step(input)
        expect = {"width": 3,
                  "state": [["w"], ["u"], [],
                            ['w'], ["r"], [],
                            [], ["d"], []],
                  "height": 3}
        self.check_result(result, expect)

    def test_my_02(self):
        # test collide()
        input = {"width": 3,
                 "state": [['w', 'd'], ['w', 'u'], ['w', 'l', 'r'],
                           ['w'], ['u'], ['l', 'r'],
                           ['w', 'l'], ['w', 'r'], ['u', 'd'],
                           ['l', 'r', 'u', 'd'], ['d'], ['l', 'd', 'r']],
                 "height": 4}
        result = lab.collide(input)
        expect = {"width": 3,
                  "state": [['w', 'u'], ['w', 'd'], ['w', 'l', 'r'],
                            ['w'], ['u'], ['u', 'd'],
                            ['w', 'r'], ['w', 'l'], ['l', 'r'],
                            ['l', 'r', 'u', 'd'], ['d'], ['l', 'd', 'r']],
                  "height": 4}
        self.check_result(result, expect)

    def test_my_03(self):
        # test propagate()
        input = {"width": 3,
                 "state": [['l'], ['r'], ['u'],
                           ['w', 'l', 'u'], ['u', 'd'], ['u', 'l', 'd'],
                           ['l', 'r'], ['u'], ['l', "r"]],
                 "height": 3}
        result = lab.propagate(input)
        expect = {"width": 3,
                  "state": [['u'], ['u'], ['r', 'u'],
                            ["w"], ['u', "l"], [],
                            [], ['d', 'r', 'l'], ['d']],
                  "height": 3}
        self.check_result(result, expect)

    def load_case(self, case):
        # Read input
        with open("cases/"+case+'.in', 'r') as f:
            d = json.loads(f.read())
        # Read golden output
        with open("cases/"+case+'.out', 'r') as f:
            g = json.loads(f.read().replace("\'", '"').replace("(", '[').replace(")", ']'))
        return d['test'], d['input']['gas'], g

    def check_result(self, result, expect):
        self.assertEqual(result["width"], expect["width"])
        self.assertEqual(result["height"], expect["height"])
        self.assertEqual(len(result["state"]), len(expect["state"]))
        for i in range(len(expect["state"])):
            res = sorted(result["state"][i])
            exp = sorted(expect["state"][i])
            self.assertEqual(res, exp)

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
