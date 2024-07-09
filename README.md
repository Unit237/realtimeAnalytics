# RealTime And Historical charts
The repository contains code for building realtime and historical charts by leveraging Go555ogle Pub/Sub and SocketIO for realtime and Bigquery and Flask for historical.
## Steps
+ Create/Setup your GCP environment (we'll need pub/sub and bigquery for this project)
  + create the json secret as seen starting at minute 1:34 in this video https://www.youtube.com/watch?v=xOtrCmPjal8]
    + place the json secret in your backend folder
  + create a pubsub topic and a subscriber to that topic
  + create a bigquery table and subscribe to the created pubsub topic
    + your table needs only one field: data with type string
     ![Screenshot 2024-07-09 at 4 08 40 PM](https://github.com/Unit237/realtimeAnalytics/assets/171470270/efc2b35a-d6f9-4262-95bc-2186be024371)
  + create a settings.ini file and place it in your backend folder 
it should be of the form  
    [DEFAULT]  
    credentials_path = xxxx-123.json  
    topic_path = projects/example-project/topics/pub-sub-topic-name-path  
    subscription_path = projects/example-project/topics/pub-sub-subscription-path
+ install the requirements using requirements.txt
+ npm install all requirements in the frontend folder
+ Run the stream_in.py server first (it is listening for dummy price data from stream_out)
+ Then run bigquery_server.py (it is serving bigquery directly to the frontend)
+ Then run the frontend (npm run dev)
+ Then run stream_out.py (it is creating mock prices *1<random_float<100*)
## Demo
https://github.com/Unit237/realtimeAnalytics/assets/171470270/7da73802-07dc-4906-b7ca-2b8334686c77

## The reads in bigquery are quite fast when table is relatively small <10mb speeds of 300ms as seen here 
![Screenshot 2024-07-09 at 4 12 03 PM](https://github.com/Unit237/realtimeAnalytics/assets/171470270/b4c540b9-661f-4a07-91fa-47c35b8ecf7a)
## Architecture
<img width="1378" alt="Screenshot 2024-07-09 at 4 13 15 PM" src="https://github.com/Unit237/realtimeAnalytics/assets/171470270/f2dc9b3d-6ea7-41fe-a2a5-77952600947c">
