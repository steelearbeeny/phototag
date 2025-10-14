import face_recognition
import json

image = face_recognition.load_image_file("/home/arbeeny/images/princess.jpg")
face = face_recognition.face_locations(image)
print("top right bottom left")
#print("(y,x) (y,x)")

#print(dir(face))
#print(json.dumps(face))


print("TYPE: ", type(face))
print("LEN : ", len(face))

top=0
left=0
bottom=0
right=0

i=1

print(face)

for f in face:    
    top=f[0]
    right=f[1]
    bottom=f[2]
    left=f[3]

    print(f"FACE {i} {f} : UL ({left},{top}) WH ({right-left},{bottom-top})")
    #enc=face_recognition.face_encodings(image,[f],1,"small")
    #print("ENC",enc)
    #enc=face_recognition.face_encodings(image)
    #print("ENC ALL",enc)


    i=i+1




