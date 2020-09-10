#!/usr/bin/env python

from mosq_test_helper import *

rc = 1
mid = 3265
keepalive = 60
connect_packet = mosq_test.gen_connect("pub-qos2-disco-test", keepalive=keepalive, clean_session=False)
connack1_packet = mosq_test.gen_connack(flags=0, rc=0)
connack2_packet = mosq_test.gen_connack(flags=1, rc=0)

subscribe_packet = mosq_test.gen_subscribe(mid, "qos2/disconnect/test", 2)
suback_packet = mosq_test.gen_suback(mid, 2)

mid = 1
publish_packet = mosq_test.gen_publish("qos2/disconnect/test", qos=2, mid=mid, payload="disconnect-message")
publish_dup_packet = mosq_test.gen_publish("qos2/disconnect/test", qos=2, mid=mid, payload="disconnect-message", dup=True)
pubrec_packet = mosq_test.gen_pubrec(mid)
pubrel_packet = mosq_test.gen_pubrel(mid)
pubcomp_packet = mosq_test.gen_pubcomp(mid)

mid = 3266
publish2_packet = mosq_test.gen_publish("qos1/outgoing", qos=1, mid=mid, payload="outgoing-message")
puback2_packet = mosq_test.gen_puback(mid)

port = mosq_test.get_port()
broker = mosq_test.start_broker(filename=os.path.basename(__file__), port=port)

try:
    sock = mosq_test.do_client_connect(connect_packet, connack1_packet, port=port)

    mosq_test.do_send_receive(sock, subscribe_packet, suback_packet, "suback")

    pub = subprocess.Popen(['./03-publish-b2c-disconnect-qos2-helper.py', str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    hrc = pub.wait()
    (stdo, stde) = pub.communicate()
    if hrc:
        exit(hrc)
    # Should have now received a publish command

    if mosq_test.expect_packet(sock, "publish", publish_packet):
        # Send our outgoing message. When we disconnect the broker
        # should get rid of it and assume we're going to retry.
        sock.send(publish2_packet)
        sock.close()

        sock = mosq_test.do_client_connect(connect_packet, connack2_packet, port=port)
        if mosq_test.expect_packet(sock, "dup publish", publish_dup_packet):
            mosq_test.do_send_receive(sock, pubrec_packet, pubrel_packet, "pubrel")

            sock.close()

            sock = mosq_test.do_client_connect(connect_packet, connack2_packet, port=port)
            if mosq_test.expect_packet(sock, "dup pubrel", pubrel_packet):
                sock.send(pubcomp_packet)
                rc = 0
            sock.close()

finally:
    broker.terminate()
    broker.wait()
    (stdo, stde) = broker.communicate()
    if rc:
        print(stde)

exit(rc)

