from oaforests import crcf
import numpy as np


class TestAxisAlignedRule:
    def test_init(self):
        """ make sure the rule initializes and stores the correct values"""
        rule = crcf.AxisAlignedRule(5, 0)
        assert rule.dimension == 5
        assert rule.value == 0

    def test_evaluate(self):
        """ make sure simple evaluates perform as expected"""
        rule = crcf.AxisAlignedRule(5, 0)
        x = np.array([[0, 0, 0, 0, 0, -1],
                      [0, 0, 0, 0, 0, 1]])
        results = rule.evaluate(x)
        assert results[0]
        assert not results[1]

    def test_generate_biased(self):
        """ make sure new rules are generated according to a bias"""
        # a deterministic bias check
        bounding_box = np.array([[0, 0], [0, 1]])
        rule = crcf.AxisAlignedRule.generate(bounding_box, mode="biased")
        assert rule.dimension == 1
        assert rule.value >= 0
        assert rule.value <= 1

        # a rough attempt at testing the bias rate
        bounding_box = np.array([[0, 2], [0, 1]])
        num_rules = 1000
        rules = [crcf.AxisAlignedRule.generate(bounding_box, mode='biased') for _ in range(num_rules)]
        dimension_zeros = [1 if rule.dimension==0 else 0 for rule in rules]
        assert np.sum(dimension_zeros) > num_rules * 0.5
        assert np.sum(dimension_zeros) < num_rules * 0.8

    def test_generate_uniform(self):
        """ make sure we can generate a rule at uniform"""
        # a deterministic check
        bounding_box = np.array([[0, 0], [0, 1]])
        rule = crcf.AxisAlignedRule.generate(bounding_box, mode="uniform")
        assert rule.dimension == 0 or rule.dimension == 1
        assert rule.value >= 0
        assert rule.value <= 1


class TestNonAxisAlignedRule:
    def test_init(self):
        """ make sure the rule initializes and stores the correct values"""
        rule = crcf.NonAxisAlignedRule(np.array([1, 2, 3]),
                                       np.array([1, 2, 4]))
        assert rule.point == np.array([1,2,4])
        assert rule.normal == np.array([1,2,3])
