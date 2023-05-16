#!/usr/bin/env python3
#
# Copyright (c) 2023 Gabriel Cebrian-Marquez
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

"""Measurement RC Stats Subscription Worker."""

MANIFEST = {
    "label": "Measurement RC Stats Subscription",
    "desc": "A subscription to RC stats notifications from WAIS",
    "callbacks": {
        "default": "Called when new measurements are available"
    },
    "modules": [],
    "params": {
        "subscription": {
            "desc": "The Measurement RC Stats Subscription.",
            "mandatory": True,
            "type": "json"
        },
        "every": {
            "desc": "The control loop period (in ms).",
            "mandatory": False,
            "default": 5000,
            "type": "int"
        }
    }
}
