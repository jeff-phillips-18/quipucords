#!/usr/bin/env python
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
""" Base CLI Command Class """

from __future__ import print_function
import sys
import requests
from cli.utils import log, handle_error_response
from cli.request import request, CONNECTION_ERROR_MSG, SSL_ERROR_MSG


# pylint: disable=too-few-public-methods, too-many-instance-attributes
class CliCommand(object):

    """ Base class for all sub-commands. """
    # pylint: disable=too-many-arguments
    def __init__(self, subcommand, action, parser, req_method, req_path,
                 success_codes):
        self.subcommand = subcommand
        self.action = action
        self.parser = parser
        self.req_method = req_method
        self.req_path = req_path
        self.success_codes = success_codes
        self.args = None
        self.req_payload = None
        self.req_params = None
        self.response = None

    def _validate_args(self):
        """
        Sub-commands can override to do any argument validation they
        require.
        """
        pass

    def _build_req_params(self):
        """
        Sub-commands can override to construct request parameters.
        """
        pass

    def _build_data(self):
        """
        Sub-commands can define this method to construct request payload.
        """
        pass

    def _handle_response_error(self):
        """
        Sub-commands can override this method to perform error handling.
        """
        r_data = self.response.json()
        handle_error_response(r_data)
        self.parser.print_help()
        sys.exit(1)

    def _handle_response_success(self):
        """
        Sub-commands can override this method to perform success handling.
        """
        pass

    def _do_command(self):
        """
        Sub-commands define this method to perform the
        required action once all options have been verified.
        """
        self._build_req_params()
        self._build_data()

        try:
            self.response = request(method=self.req_method, path=self.req_path,
                                    params=self.req_params,
                                    payload=self.req_payload)
            # pylint: disable=no-member
            if self.response.status_code not in self.success_codes:
                # handle error cases
                self._handle_response_error()
            else:
                self._handle_response_success()
        except AssertionError as assert_err:
            log.error(assert_err)
            self.parser.print_help()
            sys.exit(1)
        except requests.exceptions.SSLError as ssl_error:
            print(SSL_ERROR_MSG)
            log.error(ssl_error)
            self.parser.print_help()
            sys.exit(1)
        except requests.exceptions.ConnectionError as conn_err:
            print(CONNECTION_ERROR_MSG)
            log.error(conn_err)
            self.parser.print_help()
            sys.exit(1)

    def main(self, args):
        """
        The method that does a basic check for command
        validity and set's the process in motion.
        """
        self.args = args
        self._validate_args()

        self._do_command()