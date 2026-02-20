import tensorflow as tf

# 로그 레벨 조정 (상세 정보 확인용)
tf.debugging.set_log_device_placement(True)

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
