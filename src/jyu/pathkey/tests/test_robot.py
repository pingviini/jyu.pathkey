import unittest

import robotsuite
from jyu.pathkey.testing import PATHKEY_ROBOT_TESTING
from plone.testing import layered


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('test_pathkey.robot'),
                layer=PATHKEY_ROBOT_TESTING),
    ])
    return suite
