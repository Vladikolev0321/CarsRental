from flask import render_template, request, redirect
from flask_socketio import join_room, emit

from carsRental import app, socketio, db
from carsRental.models import User, Message
from flask_login.utils import login_required
from flask_login import login_user, current_user

@app.route('/chat/<group_id>')
@login_required
def chat(group_id):
    # token = request.cookies.get('token')
    # current_user = User.find_by_token(token)

    group = group_id.query.filter_by(id=group_id).first()

    outbound = Message.query.filter_by(sender_id=current_user.id, receiver_id=group.id)
    inbound = Message.query.filter_by(sender_id=cgroup.id, receiver_id=current_user.id)

    messages = sorted(list(outbound) + list(inbound), key=lambda x: x.timestamp)

    return render_template('chat.html',
            # current_user=current_user,
            correspondent=group,
            messages=messages)

@app.route('/message/<receiver_id>', methods=['POST'])
@login_required
def send_message(receiver_id):
    token = request.cookies.get('token')
    sender = User.find_by_token(token)
    receiver = User.query.filter_by(id=receiver_id).first()

    content = request.form['message']

    # TODO: check if the sender can send messages to the receiver

    msg = Message(sender=sender, receiver=receiver, content=content)
    db.session.add(msg)
    db.session.commit()
    return redirect('/chat/' + str(receiver_id
        ))

def get_room(sender, receiver):
    return '_'.join(sorted([str(sender), str(receiver)]))

@socketio.on('join')
def join(message):
    sender_id = message['sender']
    receiver_id = message['receiver']
    token = request.cookies.get('token')
    sender = User.find_by_token(token)
    receiver = User.query.filter_by(id=receiver_id).first()
    if receiver not in sender.likes or sender not in receiver.likes:
        return "You can't get into this chat room", 403
    room = get_room(sender_id, receiver_id)
    join_room(room)

@socketio.on('send_message')
def send_message(message):
    sender_id = message['sender']
    receiver_id = message['receiver']
    room = get_room(sender_id, receiver_id)

    token = request.cookies.get('token')
    sender = User.find_by_token(token)
    receiver = User.query.filter_by(id=receiver_id).first()

    if receiver not in sender.likes or sender not in receiver.likes:
        return "You can't send a message to this user.", 403

    content = message['msg']

    msg = Message(sender=sender, receiver=receiver, content=content)
    db.session.add(msg)
    db.session.commit()

    emit('message', {'msg': str(sender.username) + ': ' + content}, room=room)