# -*- coding: utf-8 -*-

import os
import time
import pytest

IMAGE   =   "azshoo/alaska:1.0"
PORT    =   "8091"

@pytest.fixture( scope = 'class' )
def task_container():
    
    # It's light way, but, it no good. True way: use docker module.
    cid = os.popen( f"docker run -d -p {PORT}:{PORT} {IMAGE}" ).read().rstrip()
    if cid == 32256:
        pytest.fail( f"FATAL ERROR ({cid}): Can't run new container! May be, sudo?" )

    time.sleep( 5 ) # Otherwise, the service does not have time to start.

    yield

    return_cid = os.popen( f"docker stop {cid}" ).read().rstrip()
    if return_cid != cid:
        pytest.fail( f"ERROR: Can't stop this container: {cid}" )

    return_cid = os.popen( f"docker rm {cid}" ).read().rstrip()
    if return_cid != cid:
        pytest.fail( f"ERROR: Can't remove this container: {cid} " )

