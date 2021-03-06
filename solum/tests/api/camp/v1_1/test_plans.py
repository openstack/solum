# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from unittest import mock

from solum.api.controllers.camp.v1_1 import plans
from solum import objects
from solum.tests import base
from solum.tests import fakes


@mock.patch('pecan.request', new_callable=fakes.FakePecanRequest)
@mock.patch('pecan.response', new_callable=fakes.FakePecanResponse)
@mock.patch('solum.api.handlers.camp.plan_handler.PlanHandler')
class TestPlans(base.BaseTestCase):
    def setUp(self):
        super(TestPlans, self).setUp()
        objects.load()

    def test_plans_get(self, PlanHandler, resp_mock, request_mock):
        hand_get_all = PlanHandler.return_value.get_all
        fake_plan = fakes.FakePlan()
        hand_get_all.return_value = [fake_plan]

        resp = plans.PlansController().get()
        self.assertIsNotNone(resp)
        self.assertEqual(200, resp_mock.status)
        self.assertIsNotNone(resp['result'].plan_links)
        plan_links = resp['result'].plan_links
        self.assertEqual(1, len(plan_links))
        self.assertEqual(fake_plan.name, plan_links[0].target_name)
