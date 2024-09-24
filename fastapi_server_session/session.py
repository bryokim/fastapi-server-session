# pyright: basic

# Copyright (c) 2022 DevGuyAhnaf

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections.abc import MutableMapping
from typing import Any

from .interfaces.base import BaseSessionInterface


class Session(MutableMapping):
    def __init__(
        self,
        interface: BaseSessionInterface,
        session_id: str,
    ):
        self.session_id = session_id
        self.interface = interface

    def _initiate_session(self, session_id: str) -> None:
        self.session_id = session_id
        self.interface._set_session_data(session_id, {})

    def _session_check(self) -> None:
        if not self.interface._get_session_data(self.session_id):
            self._initiate_session(self.session_id)

    def clear(self) -> None:
        """Clears and deletes the session"""
        self.interface._delete_session(self.session_id)

    def __setitem__(self, key, value) -> None:
        self._session_check()
        data = self.interface._get_session_data(self.session_id)
        data[key] = value
        self.interface._set_session_data(self.session_id, data)

    def __getitem__(self, key) -> Any | None:
        try:
            return self.interface._get_session_data(self.session_id).get(key)
        except Exception:
            return None

    def __delitem__(self, key) -> None:
        data = self.__getitem__(key)
        try:
            del data[key]
            self.interface._set_session_data(self.session_id, data)
        except (KeyError, TypeError):  # Session key did not exist or data is None
            return

    def __iter__(self):
        return iter(self.interface._get_session_data(self.session_id))

    def __len__(self):
        return len(self.interface._get_session_data(self.session_id))

    def __str__(self):
        return str(self.interface._get_session_data(self.session_id))

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.session_id}>"
