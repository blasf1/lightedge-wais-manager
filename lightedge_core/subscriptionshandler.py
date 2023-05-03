#!/usr/bin/env python3
#
# Copyright (c) 2020 Roberto Riggio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

"""Exposes a RESTful interface ."""

import uuid

import empower_core.apimanager.apimanager as apimanager


# pylint: disable=W0223
class SubscriptionsHandler(apimanager.APIHandler):
    """Access the WIA subscriptions."""

    URLS = [r"/wia/v1/subscriptions/?",
            r"/wia/v1/subscriptions/([a-zA-Z0-9-]*)/?"]

    @apimanager.validate(min_args=0, max_args=1)
    def get(self, sub_id=None):
        """Get the subscriptions

        Example URLs:

            GET /wia/v1/subscriptions

            {
              "_links": {
                "self": {
                  "href": "http://uri/wia/v1/subscriptions"
                },
                "subscription": [{
                    "href": "http://uri/wia/v1/subscriptions/1",
                    "subscriptionType": "MeasRcStatsSubscription"
                  },
                  {
                    "href": "http://uri/wia/v1/subscriptions/2",
                    "subscriptionType": "MeasRcStatsSubscription"
                  }
                ]
              }
            }
        """

        if sub_id:
            return self.service.subscriptions[uuid.UUID(sub_id)].subscription

        return self.service.get_subscriptions_links()

    @apimanager.validate(returncode=201, min_args=0, max_args=1)
    def post(self, *args, **kwargs):
        """Create a new subscription.

        POST /wia/v1/subscriptions

        {
          "callbackReference": "http://client.example.com/wia/v1/",
          "filterCriteria": { },
          "expiryDeadline": {
            "seconds": 1577836800,
            "nanoSeconds": 0
          },
          "subscriptionType": "MeasRcStatsSubscription"
        }
        """

        sub_id = uuid.UUID(args[0]) if len(args) > 0 else uuid.uuid4()

        sub = \
            self.service.add_subscription(sub_id=sub_id, params=kwargs)

        self.set_header("Location", "/wia/v1/subscriptions/%s" %
                        sub.service_id)

    @apimanager.validate(returncode=204, min_args=0, max_args=1)
    def delete(self, sub_id=None):
        """Delete a subscription.

        Args:

            [0], the subscription id

        Example URLs:

            DELETE /wia/v1/subscriptions/
              52313ecb-9d00-4b7d-b873-b55d3d9ada26
        """

        sub_id = uuid.UUID(sub_id) if sub_id else None

        self.service.rem_subscription(sub_id=sub_id)
