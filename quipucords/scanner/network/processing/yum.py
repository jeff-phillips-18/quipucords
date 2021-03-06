# Copyright (c) 2018 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 3 (GPLv3). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv3
# along with this software; if not, see
# https://www.gnu.org/licenses/gpl-3.0.txt.

"""Initial processing of the shell output from the yum repolist data."""

import logging
from scanner.network.processing import process

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# pylint: disable=too-few-public-methods

# #### Processors ####


class ProcessEnableYumRepolist(process.Processor):
    """Process the list of enabled yum repositories."""

    KEY = 'yum_enabled_repolist'

    @staticmethod
    def process(output):
        """Pass the output back through."""
        repos = []
        out_lines = output['stdout_lines']
        for line in out_lines:
            repo, _, remainder = line.partition(' ')
            repo_name, _, _ = remainder.rpartition(' ')
            repos.append({'repo': repo.strip(), 'name': repo_name.strip()})
        return repos
