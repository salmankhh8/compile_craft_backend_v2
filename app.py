from flask import Flask, jsonify, request

from compile_code import ExecuteJavascriptCode, ExecutePythonCode
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['secret'] = 'secret'
CORS(app)
socketio = SocketIO(app,cors_allowed_origins="*")

mongo_url="mongodb+srv://salmankhh8:RZRBZ45knXBwnSw1@cluster0.fvlhn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
user_connections={}

user_sessions = {}

@socketio.on('connect')

# //1053454717110-fi07ao6m7s0p1git73ca9g7q8o68qktm.apps.googleusercontent.com
# secret=> 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
def connect_client():
    user_id = request.sid  # Unique session ID for the connection
    email = request.args.get('email')  # Email from query string
    start_time = datetime.now()

    if email not in user_sessions:
        user_sessions[email] = []

    # Append the new session for this email
    user_sessions[email].append({"sid": user_id, "start_time": start_time})

    print(f"User {email} connected with session ID {user_id} at {start_time}")

    # Emit session info back to the client
    emit('session_info', {
        "session_id": user_id,
        "email": email,
        "start_time": start_time.isoformat(),
    })
    
    # return jsonify({"user_id":user_id,"start_time":start_time,"user_sessions":user_sessions})

old_time = "2025-01-13T08:44:00.199Z"
# starting_time = datetime.datetime.now()s

def subtract_date(old_time, new_time):
    
    new_time_obj = datetime.fromisoformat(new_time.replace("Z", "+00:00"))
    old_time_obj = datetime.fromisoformat(old_time.replace("Z", "+00:00"))
    
    time_differnce = new_time_obj - old_time_obj
    
    return time_differnce

user_activity = {}


@socketio.on('send_time')
def recieve_message(message):
    # print("mesaged recieved",message)
    
    current_time = message.get("current_time")
    
    user_id = message.get('user_id')
    timestamp = datetime.fromisoformat(message.get('current_time').replace('Z', ''))  # Parse ISO timestamp
    if user_id not in user_activity:
        # Initialize user activity if not present
        user_activity[user_id] = {
            "last_active_time": timestamp,
            "total_active_time": timedelta(0),
        }
    else:
        # Calculate duration since the last activity
        last_active_time = user_activity[user_id]["last_active_time"]
        duration = timestamp - last_active_time

        if duration <= timedelta(seconds=5):
            # Add duration to total active time if it's within the allowed interval
            user_activity[user_id]["total_active_time"] += duration

        # Update last active time
        user_activity[user_id]["last_active_time"] = timestamp
    print(f"User {user_id} activity recorded at {timestamp}")
    print(f"Total active time for {user_id}: {user_activity[user_id]['total_active_time']}")

    
    
    
    # result = subtract_date(old_time,current_time)
    # print( result, message )
    

# @socketio.on('send_time')
# def handle_send_time(data):
#     """
#     Receive the ISO time from the frontend and calculate the duration since the last update.
#     """
    
#     try:
#         user_id = request.sid
#         if data == "conncted":
#             if user_id not in user_sessions:
#                 current_time = datetime.datetime.now()
#                 user_sessions[user_id] = {
#                     'start_time': current_time,
#                     'last_update_time': current_time,
#                     'total_duration': 0
#                 }
#                 print(f"User {user_id} connected at {current_time}.")
#         else:
#             # For any other message, update the session
#             current_time = datetime.datetime.now()
#             if user_id in user_sessions:
#                 last_time = user_sessions[user_id]['last_update_time']
#                 duration_since_last_update = (current_time - last_time).total_seconds()

#                 # Update the user's session
#                 user_sessions[user_id]['total_duration'] += duration_since_last_update
#                 user_sessions[user_id]['last_update_time'] = current_time

#                 # Emit the updated total duration back to the client
#                 socketio.emit('duration_update', {
#                     'user_id': user_id,
#                     'total_duration': user_sessions[user_id]['total_duration']
#                 })
                 
#     except Exception as e:
#         socketio.emit('error', {'error': str(e)})
        
#     user_id = request.sid
#     if user_id not in user_sessions:
#         emit('error', {'message': 'User connection not found!'})
#         return

#     current_time = datetime.fromisoformat(data.get('current_time'))
#     last_time = user_sessions[user_id].get('last_update_time', user_sessions[user_id]['start_time'])

#     # Calculate duration since the last update and add to total duration
#     duration = current_time - last_time
#     user_sessions[user_id]['total_duration'] += duration
#     user_sessions[user_id]['last_update_time'] = current_time

#     print(f"User {user_id} updated. Total duration: {user_sessions[user_id]['total_duration']}")
#     emit('duration_update', {
#         'total_duration': str(user_sessions[user_id]['total_duration']),
#         'current_time': current_time.isoformat()
#     })

@app.route('/compileCode', methods=['post'])
def get_data():
    print("rout triggereds")
    print(request.get_json())
    data = request.get_json()
    
    if data["language"]=="javascript":   
        print("javascript exected")
        # data.get("result")
        js_code_func = ExecuteJavascriptCode()
        compiled_res = js_code_func.execute_js(data['code'])
        
        print(compiled_res,"js compiled result")
        
        return jsonify({ "success": True, "result": compiled_res })
    elif data["language"]=="python":
        py_code_def = ExecutePythonCode()
        executed_res = py_code_def.execute_python_code(data['code'])
        print(executed_res, "python compiled result")
        
        return jsonify({ "success": True, "result": executed_res['output'] })
    
    
@app.route('/login', methods=['post'])
def login_user():
    print("lgin API")
    data = request.get_json()
    print(data)


if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()  # Ensures compatibility
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
