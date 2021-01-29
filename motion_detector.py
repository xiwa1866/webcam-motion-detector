# this file captures motion from a webcam and stores moving motion times 
# into a csv file 
import cv2, pandas
from datetime import datetime

# initialization
first_frame=None # create a first frame variable
video = cv2.VideoCapture(0) # start video capturing
status_list=[None, None] # a list that records if the object is 
# captured at each instance(image)
# if yes, status is setted to 1
# if no, status is setted to 0
times=[] # stores object opening/exiting time
df=pandas.DataFrame(columns=["Start", "End"] ) # load the times list into a pandas dataframe

# main video capture loop
while True:
    #capture an instant(image)
    check, frame = video.read()
    # assume no object in image
    status=0
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert image to gray scale
    gray=cv2.GaussianBlur(gray,(21,21),0) # make image vague to improve accuracy(of further steps)
    # check if first_frame has been stored
    # if not, update first_frame
    if first_frame is None:
        first_frame=gray
        continue #skip the rest of the loop
    delta_frame=cv2.absdiff(first_frame, gray) # new frame that store changes compared with first frame
    # set all pixels that diff < 30 to black pixels
    # ignore minor changes
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1] 

    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2) # smooth edges
    #find objects
    (cnts,_)=cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i in cnts:
        # if object is detacted
        if cv2.contourArea(i) >= 10000:
            # update status to true(object is indeed detacted)
            status=1
            #surround the object with a rectangle in the original image
            (x, y, w, h)=cv2.boundingRect(i)
            cv2.rectangle(frame, (x, y), (x+w,y+h), (0, 255, 0), 3)
    # update status to the list
    status_list.append(status)
    # truncate the list to its last two entries
    status_list = status_list[-2:]
    ''' 
    if status is different than last time, an object must have entered or exited screen
    append the current time to times.list
    '''
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    # display four windows
    cv2.imshow("diff", delta_frame)
    cv2.imshow("gray", gray)
    cv2.imshow("threshhold", thresh_frame)
    cv2.imshow("regular", frame)
    
    # wait 50 miliseconds for a keyboard input 
    key = cv2.waitKey(50)
    # the loop breaks only if user presses key 'q'
    if key == ord('q'):
        # append current times if object is still inside image when camera is turned off
        if status == 1:
            times.append(datetime.now())
        break
# load list times to a pandas dataframe
for i in range(0, len(times), 2):
    df=df.append({"Start":times[i], "End":times[i+1]}, ignore_index = True)
    
df.to_csv("Times.csv") # store data into a csv file
video.release() # stop video capture
cv2.destroyAllWindows # close all display windows
