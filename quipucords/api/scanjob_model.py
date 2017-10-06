#
# Copyright (c) 2017 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 3 (GPLv3). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv3
# along with this software; if not, see
# https://www.gnu.org/licenses/gpl-3.0.txt.
#
"""Defines the models used with the API application.
   These models are used in the REST definitions
"""

from django.db import models
from api.networkprofile_model import NetworkProfile


class ScanJob(models.Model):
    """The host credential for connecting to host systems via ssh"""
    DISCOVERY = 'discovery'
    HOST = 'host'
    SCAN_TYPE_CHOICES = ((DISCOVERY, 'discovery'), (HOST, 'host'))

    profile = models.ForeignKey(NetworkProfile, on_delete=models.CASCADE)
    scan_type = models.CharField(
        max_length=9,
        choices=SCAN_TYPE_CHOICES,
        default=HOST,
    )

    class Meta:
        verbose_name_plural = 'Scan Jobs'