import tensorflow as tf
from tensorflow import keras

# โมเดลที่ถูกฝึกอบรมแล้ว
model = keras.models.load_model('tester.keras')

# ลงทะเบียนฟังก์ชัน sparse_softmax_cross_entropy
def sparse_softmax_cross_entropy(y_true, y_pred):
    return tf.compat.v1.losses.sparse_softmax_cross_entropy(y_true, y_pred)

model.compile(
    optimizer="Adam",
    loss=sparse_softmax_cross_entropy,  # ใช้ฟังก์ชันที่ลงทะเบียนแทน
    metrics=["accuracy"],
)

# ตัวอย่างข้อมูลทดสอบ
input_data_path = "C:\\Users\\ASUS\\Desktop\\spreaker_recog\\seen_data\\Aong01_1.wav"

# อ่านและแปลงข้อมูลเสียง
audio, _ = tf.audio.decode_wav(tf.io.read_file(input_data_path), desired_channels=1)
audio = tf.expand_dims(audio, axis=0)  # เพิ่มมิติเพื่อให้เข้ากับรูปแบบข้อมูล

# ทำนาย
predictions = model.predict(audio)

# แสดงผลลัพธ์
print("Predictions:", predictions)