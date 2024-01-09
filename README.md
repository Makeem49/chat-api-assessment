Table of Contents

- Features
- Endpoints
- Getting Started
- Usage

Features

- User authentication (login, logout, registration).
- Real-time messaging through WebSocket.
- Simple and easy-to-use API endpoints.

- The API exposes the following endpoints:
    base_url = http://127.0.0.1:8000/api/auth/
    Login
        Endpoint: login/
        Description: Authenticate users and obtain access tokens.

    Logout
        Endpoint:  logout/
        Description: Invalidate user tokens to log them out by providing refresh token

    Register
        Endpoint: register/
        Description: Register new users.

    Send-message WebSocket Endpoint
        Endpoint: ws://127.0.0.1:8000/ws/chat/basket_ball/?token={{access_token}}
        Description: WebSocket endpoint for sending real-time messages.
        payload:
            {  
                "type":"chat_message",
                "content" : "Hello wolrd"
            }
  

    Read-message WebSocket Connection
        Endpoint: ws://127.0.0.1:8000/ws/read/basket_ball/?token={{access_token}}
        Description: WebSocket connection for reading messages and send response to the room notifying teh read status
        payload:
            {
             "message_id" : "30a6d602-b52c-45c0-a6c6-baf4c99eb5f4",
             "type":"read_messages"
            }


Getting Started

To get started with the Chat API, follow these steps:


1. 
  git clone [https://github.com/Makeem49/chat-api-assessment.git](https://github.com/Makeem49/chat-api-assessment.git)
  cd simple-chat-api

or 

Clone the image on docker hub : docker pull makeem/chat-api:v1


2. Install packeages using pip install
     - pip install -r requirements.txt
  
3. run the application using : python3 manage.py runserver 

  

        
