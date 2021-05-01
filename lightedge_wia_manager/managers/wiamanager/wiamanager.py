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

"""WLAN Information API Manager."""

from empower_core.service import EService
from empower_core.serialize import serializable_dict

from lightedge_wia_manager.managers.wiamanager.querieshandler \
    import QueriesHandler

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8888


@serializable_dict
class APInfo():
    """ Information on APs available from the WLAN Access Information
    Service."""

    def __init__(self):

        self.info = {
            "apId": None,
            "channel": None,
            "wlanCap": None,
            "wanMetrics": None,
            "bssLoad": None,
            "extBssLoad": None,
            "apLocation": None,
            "apNeighbor": None
        }

    def to_dict(self):
        """Return JSON-serializable representation of the object."""

        return self.info


class WIAManager(EService):
    """WLAN Information API Manager.

    Parameters:
        ctrl_host: sd-ran controller host (optional, default: 127.0.0.1)
        ctrl_host: sd-ran controller port (optional, default: 8888)
    """

    HANDLERS = [QueriesHandler]

    def __init__(self, context, service_id, ctrl_host, ctrl_port):

        super().__init__(context=context, service_id=service_id,
                         ctrl_host=ctrl_host, ctrl_port=ctrl_port)

        self.aps = list()

        ap1 = APInfo()

        self.aps.append(ap1)

    def get_aps(self):
        """Return the APs."""

        return self.aps

    @property
    def ctrl_host(self):
        """Return ctrl_host."""

        return self.params["ctrl_host"]

    @ctrl_host.setter
    def ctrl_host(self, value):
        """Set ctrl_host."""

        if "ctrl_host" in self.params and self.params["ctrl_host"]:
            raise ValueError("Param ctrl_host can not be changed")

        self.params["ctrl_host"] = str(value)

    @property
    def ctrl_port(self):
        """Return ctrl_port."""

        return self.params["ctrl_port"]

    @ctrl_port.setter
    def ctrl_port(self, value):
        """Set host."""

        if "ctrl_port" in self.params and self.params["ctrl_port"]:
            raise ValueError("Param ctrl_port can not be changed")

        self.params["ctrl_port"] = int(value)


def launch(context, service_id, ctrl_host=DEFAULT_HOST,
           ctrl_port=DEFAULT_PORT):
    """ Initialize the module. """

    return WIAManager(context, service_id, ctrl_host, ctrl_port)
