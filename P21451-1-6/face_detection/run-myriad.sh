./interactive_face_detection_demo -i cam -d MYRIAD -m intel_models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -d_ag MYRIAD -m_ag intel_models/age-gender-recognition-retail-0013/FP16/age-gender-recognition-retail-0013.xml -d_em MYRIAD -m_em intel_models/emotions-recognition-retail-0003/FP16/emotions-recognition-retail-0003.xml -d_hp MYRIAD -m_hp intel_models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml -r | python3 /export/install/Plugfest2019/P21451-1-6/face_detection/face-mqtt.py -c /export/install/Plugfest2019/P21451-1-6/config.yml
