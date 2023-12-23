# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import logging
import os
import re
from pathlib import Path
from typing import Final, Optional

_SCHEME_REGEX: Final = re.compile("^[a-zA-Z0-9]+://")


def _starts_with_scheme(s: str) -> bool:
    return re.match(_SCHEME_REGEX, s) is not None


def _get_path_from_env(var_name: str) -> Optional[Path]:
    pathname = os.getenv(var_name)
    if not pathname:
        return None

    try:
        path = Path(pathname)
    except ValueError as ex:
        raise RuntimeError(
            f"The value of the `{var_name}` environment variable must be a pathname, but is '{pathname}' instead."
        ) from ex

    if not path.exists():
        logger = logging.getLogger("fairseq2.assets")

        logger.warning(
            f"The path '{path}' pointed to by the `{var_name}` environment variable does not exist."
        )

        return None

    return path
