#!/usr/bin/env python
# License: GPLv3 Copyright: 2020, Kovid Goyal <kovid at kovidgoyal.net>


from typing import TYPE_CHECKING, Optional

from .base import (
    MATCH_WINDOW_OPTION, ArgsType, Boss, PayloadGetType, PayloadType,
    RCOptions, RemoteCommand, ResponseType, Window, MatchError
)

if TYPE_CHECKING:
    from kitty.cli_stub import CloseWindowRCOptions as CLIOptions


class CloseWindow(RemoteCommand):
    '''
    match/str: Which window to close
    self/bool: Boolean indicating whether to close the window the command is run in
    ignore_no_match/bool: Boolean indicating whether no matches should be ignored or return an error
    '''

    short_desc = 'Close the specified windows'
    options_spec = MATCH_WINDOW_OPTION + '''\n
--self
type=bool-set
Close the window this command is run in, rather than the active window.


--ignore-no-match
type=bool-set
Do not return an error if no windows are matched to be closed.
'''
    argspec = ''

    def message_to_kitty(self, global_opts: RCOptions, opts: 'CLIOptions', args: ArgsType) -> PayloadType:
        return {'match': opts.match, 'self': opts.self, 'ignore_no_match': opts.ignore_no_match}

    def response_from_kitty(self, boss: Boss, window: Optional[Window], payload_get: PayloadGetType) -> ResponseType:
        try:
            windows = self.windows_for_match_payload(boss, window, payload_get)
        except MatchError:
            if payload_get('ignore_no_match'):
                return None
            raise
        for window in windows:
            if window:
                boss.mark_window_for_close(window)
        return None


close_window = CloseWindow()
