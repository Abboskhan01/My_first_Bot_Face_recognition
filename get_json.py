import os
import json
from json import JSONEncoder
import numpy as np
import face_recognition

class nump(JSONEncoder):
    def default(self,obj):
        if isinstance(obj,np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self,obj)



data = []
for k in os.listdir("Yonalishlar"):
    for d in os.listdir(f"My_first_Bot_Face_recognition/Yonalishlar/{k}"):
        name = d.split(".")[0]
        path = f"My_first_Bot_Face_recognition/Yonalishlar/{k}/{d}"
        naun = face_recognition.load_image_file(path)
        encode_picture = face_recognition.face_encodings(naun)[0]

        i = {
            "name":name,
            "path":path,
            "dir":k,
            "encode":encode_picture
        }
        data.append(i)
encode_data = json.dumps(data,cls=nump)


def main():
    with open ("../sample.json", 'w') as sample:
        sample.write(encode_data)

if __name__ == '__main__':
    main()
