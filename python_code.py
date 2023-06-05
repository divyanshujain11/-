#boto3 library to connect python code to aws services 
import boto3 
#cv2 library for capturing images for Hand gestures
import cv2
from cvzone.HandTrackingModule import HandDetector

# to store instance ids which we create or destroy
allOs=[]

# create or destroy "ec2 instances"
ec2 = boto3.resource("ec2",region_name='ap-south-1')
def myOsLaunch():
    instances = ec2.create_instances(
        ImageId="ami-0a2acf24c0d86e927",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        SecurityGroupIds=["sg-0abb972efed0502cb"]
    )
    myId=instances[0].id
    allOs.append(myId)
    print("total OS :" ,len(allOs))
    print(myId)

def osTerminate():
    osdelete=allOs.pop()
    ec2.instances.filter(InstanceIds=[osdelete]).terminate()
    print("total OS : ",len(allOs))


#capturing images and detect hand gestures
cap=cv2.VideoCapture(0)
detector=HandDetector(maxHands=1)
while True:
    status,photo=cap.read()
    cv2.imshow("myphoto",photo)
    if cv2.waitKey(1000)==13:
        break
# cv2.destroyAllWindows()

    hand=detector.findHands(photo,draw=False)

    if hand:
            lmlist=hand[0]
#             print(detector.fingersUp(lmlist))
            totalFinger=detector.fingersUp(lmlist)
            totalFinger=detector.fingersUp(lmlist)
            if totalFinger==[0,1,1,0,0]:
                print("i know 2 or 3 -finger up")
                myOsLaunch()
            elif totalFinger==[0,1,0,0,0]:
                print("i know only 1 finger up,index finger")
                osTerminate()
            else:
                print("i dont consider in my Do it with Attitude ")
    else:print("no hand")
                
cv2.destroyAllWindows()
cap.release()    
