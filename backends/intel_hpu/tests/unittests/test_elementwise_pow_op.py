# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function, division

import unittest

import numpy as np
import paddle
from tests.op_test import OpTest

paddle.enable_static()

import os

intel_hpus_module_id = os.environ.get("FLAGS_selected_intel_hpus", 0)
intel_hpus_static_mold = os.environ.get(
    "FLAGS_static_mold_intel_hpus", 0
)  # default is dynamic mold test FLAGS_static_mold_intel_hpus=0


class TestElementwisePowOp(OpTest):
    def setUp(self):
        self.op_type = "elementwise_pow"
        self.set_hpu()
        self.init_dtype()
        self.init_axis()
        self.init_input()
        self.init_output()

        self.inputs = {
            "X": OpTest.np_dtype_to_base_dtype(self.x),
            "Y": OpTest.np_dtype_to_base_dtype(self.y),
        }
        self.outputs = {"Out": self.out}

    def set_hpu(self):
        self.__class__.use_custom_device = True
        self.__class__.no_need_check_grad = True
        self.place = paddle.CustomPlace("intel_hpu", int(intel_hpus_module_id))
        if int(intel_hpus_static_mold) == 0:
            paddle.disable_static()
        else:
            paddle.enable_static()

    def init_input(self):
        np.random.seed(1024)
        self.x = np.random.uniform(1, 2, [13, 17]).astype(self.dtype)
        self.y = np.random.uniform(1, 2, [13, 17]).astype(self.dtype)

    def init_output(self):
        self.out = np.power(self.x, self.y)

    def init_dtype(self):
        self.dtype = np.float32

    def init_axis(self):
        self.axis = -1

    def test_check_output(self):
        self.check_output_with_place(self.place)


class TestElementwisePowOp_broadcast(TestElementwisePowOp):
    def init_input(self):
        self.x = np.random.uniform(1, 2, [13, 17]).astype(self.dtype)
        self.y = np.random.uniform(1, 2, [17]).astype(self.dtype)


class TestFP16ElementwisePowOp(TestElementwisePowOp):
    def init_dtype(self):
        self.dtype = np.float16


class TestFP16ElementwisePowOp_1(TestElementwisePowOp_broadcast):
    def init_dtype(self):
        self.dtype = np.float16


if __name__ == "__main__":
    unittest.main()
