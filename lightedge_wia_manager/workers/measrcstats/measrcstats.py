#!/usr/bin/env python3
#
# Copyright (c) 2021 Roberto Riggio
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

"""Measurement RC Stats Subscription."""

import uuid

from empower_core.app import EVERY

from lightedge_core.subscription import Subscription

DEFAULT_URI = "http://127.0.0.1:8891"


class MeasRcStats(Subscription):
    """Meas RC Stats."""

    SUB_TYPE = "meas_rc_stats"
    SUB_CONFIG = "MeasRcStatsSubscription"
    SUB_PARAMS = ['callbackReference', 'expiryDeadline',
                  'filterCriteria', 'subscriptionType']

    def __init__(self, context, service_id, every, subscription, uri):

        super().__init__(context=context, service_id=service_id, every=every,
                         subscription=subscription, uri=uri)

        self.app_id = None
        self.project_id = None

    async def loop(self):
        """Periodic job."""

        try:
            await self.register()
        except ConnectionRefusedError:
            self.log.error("Unable to contact controller")

    async def register(self):
        """Worker on controller."""

        # Both project id and app id are set check if they are valid
        if self.project_id and self.app_id:

            url = "/projects/%s/apps/%s/callbacks/default" % \
                (self.project_id, self.app_id)

            resp = await self.manager.get(self.manager.empower_url + url)

            # All ok, we can return
            if resp.code == 200:
                return

        self.project_id = uuid.UUID("10589166-E2AC-4D4C-9E92-C773B913E340")  # TODO: change by actual project id

        data = {
            "name": "empower.apps.wifircstats.wifircstats",
            "params": {
                "sta": "11:22:33:44:55:66",  # TODO: change by actual STA information
                "every": 2000
            }
        }

        url = "/projects/%s/apps" % self.project_id
        resp = await self.manager.post(self.manager.empower_url + url, data)

        if not resp.code == 201:
            self.log.error("Unable to start worker, error %u",
                           resp.code)
            return

        location = resp.headers['Location']

        self.app_id = location.split("/")[-1]

        # Add callback
        callback = "%s/wia/v1/subscriptions/%s/ch" % (self.uri,
                                                      self.service_id)

        data = {
            "version": "1.0",
            "name": "default",
            "callback": callback,
            "callback_type": "rest"
        }

        url = "/projects/%s/apps/%s/callbacks" % (self.project_id, self.app_id)
        resp = await self.manager.post(self.manager.empower_url + url, data)

        if not resp.code == 201:
            self.log.error("Unable to add callback, error %u",
                           resp.code)
            return

        self.log.info("Remote worker successfully configured.")


def launch(context, service_id, subscription, uri=DEFAULT_URI, every=EVERY):
    """ Initialize the module. """

    return MeasRcStats(context=context, service_id=service_id, every=every,
                       subscription=subscription, uri=uri)
