# coding: utf-8

from unittest import TestCase
from StructuredPerceptron.train_structured_perceptron import StructuredPerceptron


class TestStructuredPerceptron(TestCase):
    def test_train_partially_labled_structured_perceptron(self):
        # self.fail()
        pass


    def test_violates(self):
        st_percep = StructuredPerceptron()
        self.assertTrue(st_percep.violates(u"コーナーキックチャンス", u"コーナーキック チャンス"))
        self.assertTrue(st_percep.violates(u"コー ナーキックチャンス", u"コーナーキック チャンス"))
        self.assertFalse(st_percep.violates(u"コーナー キック チャンス", u"コーナーキック チャンス"))
        pass
