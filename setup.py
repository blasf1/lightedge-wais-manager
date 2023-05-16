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

"""Setup script."""

from setuptools import setup, find_packages

setup(name="lightedge-wais-manager",
      version="1.0",
      description="LightEdge WLAN Access Information Service Manager",
      author="Gabriel Cebrian-Marquez",
      author_email="Gabriel.Cebrian@uclm.es",
      url="http://lightedge.github.io/",
      long_description="The LightEdge WLAN Access Information Service Manager",
      packages=find_packages())
