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

"""Signal manager to handle scan triggering."""

import logging
import django.dispatch
from django.utils.translation import ugettext as _
import api.messages as messages
from scanner.manager import SCAN_MANAGER
from scanner import ScanJobRunner

# Get an instance of a logger
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

PAUSE = 'pause'
CANCEL = 'cancel'
RESTART = 'restart'

# pylint: disable=W0613


def handle_scan(sender, instance, **kwargs):
    """Handle incoming scan.

    :param sender: Class that was saved
    :param instance: ScanJob that was triggered
    :param kwargs: Other args
    :returns: None
    """
    instance.log_message(_(messages.SIGNAL_STATE_CHANGE) % ('START'))
    scanner = ScanJobRunner(instance)
    if not SCAN_MANAGER.is_alive():
        SCAN_MANAGER.start()
        # Don't add the scan as it will be picked up
        # by the manager startup, looking for pending/running scans.
    else:
        SCAN_MANAGER.put(scanner)


def scan_action(sender, instance, action, **kwargs):
    """Handle action on scan.

    :param sender: Class that was saved
    :param instance: ScanJob that was saved
    :param action: The action to take on the scan (pause, cancel, resume)
    :param kwargs: Other args
    :returns: None
    """
    if action == PAUSE or action == CANCEL:
        SCAN_MANAGER.kill(instance)


def scan_pause(sender, instance, **kwargs):
    """Pause a scan.

    :param sender: Class that was saved
    :param instance: ScanJob that was saved
    :param kwargs: Other args
    :returns: None
    """
    instance.log_message(_(messages.SIGNAL_STATE_CHANGE) % ('PAUSE'))
    scan_action(sender, instance, PAUSE, **kwargs)


def scan_cancel(sender, instance, **kwargs):
    """Cancel a scan.

    :param sender: Class that was saved
    :param instance: ScanJob that was saved
    :param kwargs: Other args
    :returns: None
    """
    instance.log_message(_(messages.SIGNAL_STATE_CHANGE) % ('CANCEL'))
    scan_action(sender, instance, CANCEL, **kwargs)


def scan_restart(sender, instance, **kwargs):
    """Restart a scan.

    :param sender: Class that was saved
    :param instance: ScanJob that was saved
    :param kwargs: Other args
    :returns: None
    """
    instance.log_message(_(messages.SIGNAL_STATE_CHANGE) % ('RESTART'))
    scanner = ScanJobRunner(instance)

    if not SCAN_MANAGER.is_alive():
        SCAN_MANAGER.start()
        # Don't add the scan as it will be picked up
        # by the manager startup, looking for pending/running scans.
    else:
        SCAN_MANAGER.put(scanner)


# pylint: disable=C0103
start_scan = django.dispatch.Signal(providing_args=['instance'])
pause_scan = django.dispatch.Signal(providing_args=['instance'])
cancel_scan = django.dispatch.Signal(providing_args=['instance'])
restart_scan = django.dispatch.Signal(providing_args=['instance'])

start_scan.connect(handle_scan)
pause_scan.connect(scan_pause)
cancel_scan.connect(scan_cancel)
restart_scan.connect(scan_restart)
