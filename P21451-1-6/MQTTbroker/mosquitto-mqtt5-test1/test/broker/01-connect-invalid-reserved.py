#!/usr/bin/env python

# Test whether a CONNECT with reserved set to 1 results in a disconnect. MQTT-3.1.2-3

from mosq_test_helper import *

rc = 1
keepalive = 10
connect_packet = mosq_test.gen_connect("connect-invalid-test", keepalive=keepalive, connect_reserved=True, proto_ver=4)

port = mosq_test.get_port()
broker = mosq_test.start_broker(filename=os.path.basename(__file__), port=port)

try:
    sock = mosq_test.do_client_connect(connect_packet, "", port=port)
    sock.close()
    rc = 0

finally:
    broker.terminate()
    broker.wait()
    (stdo, stde) = broker.communicate()
    if rc:
        print(stde)

exit(rc)

