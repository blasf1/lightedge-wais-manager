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

"""A genercic subscription."""

from empower_core.launcher import srv_or_die
from empower_core.worker import EWorker


class Subscription(EWorker):
    """A generci subscription."""

    SUB_TYPE = None
    SUB_CONFIG = None
    SUB_PARAMS = ['callbackReference', 'expiryDeadline', 'subscriptionType']

    MODULES = []

    def __init__(self, context, service_id, every, subscription, uri):

        super().__init__(context=context, service_id=service_id, every=every,
                         subscription=subscription, uri=uri)

        self.manager = srv_or_die("wiamanager")

    def handle_response(self, callback):
        """Handle response to one subscription."""

        self.log.info("Received callback for subscription %s", self.service_id)
        self.log.info(callback)

        # handle callbacks
        self.handle_callbacks()

    @property
    def uri(self):
        """Return uri."""

        return self.params["uri"]

    @uri.setter
    def uri(self, value):
        """Set uri."""

        self.params["uri"] = value

    @property
    def callback_reference(self):
        """Return callback_reference."""

        return self.subscription['callbackReference']

    @property
    def expiry_deadline(self):
        """Return expiry_deadline."""

        return self.subscription['expiryDeadline']

    @property
    def subscription_type(self):
        """Return expiry_deadline."""

        return self.subscription['subscriptionType']

    @property
    def subscription(self):
        """Return subscription."""

        return self.params["subscription"]

    @subscription.setter
    def subscription(self, value):
        """Set subscription."""

        for param in self.SUB_PARAMS:
            if param not in value:
                raise ValueError("Unable to find '%s'")

        self.params["subscription"] = value
