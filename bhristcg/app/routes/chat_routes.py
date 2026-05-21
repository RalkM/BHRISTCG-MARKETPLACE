#Chat Routes
from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.models.message import Message, Notification
from app.models.user import User

chat_bp = Blueprint('chat', __name__)
MAX_MSG = 1000


@chat_bp.route('/inbox')
@login_required
def inbox():
    sent_ids = db.session.query(Message.recipient_id).filter_by(sender_id=current_user.id).distinct()
    recv_ids = db.session.query(Message.sender_id).filter_by(recipient_id=current_user.id).distinct()
    partner_ids = set([r[0] for r in sent_ids] + [r[0] for r in recv_ids])
    partners = User.query.filter(User.id.in_(partner_ids)).all()

    active_partner_id = request.args.get('with', type=int)
    messages, active_partner = [], None
    unread_only = request.args.get('unread') == '1'

    if active_partner_id:
        active_partner = User.query.get_or_404(active_partner_id)
        q = Message.query.filter(
            or_(
                (Message.sender_id == current_user.id) & (Message.recipient_id == active_partner_id),
                (Message.sender_id == active_partner_id) & (Message.recipient_id == current_user.id),
            )
        ).order_by(Message.created_at.asc())
        if unread_only:
            q = q.filter_by(is_read=False)
        messages = q.all()
        Message.query.filter_by(
            sender_id=active_partner_id, recipient_id=current_user.id, is_read=False
        ).update({'is_read': True})
        db.session.commit()

    unread_count = Message.query.filter_by(recipient_id=current_user.id, is_read=False).count()
    return render_template('chat/inbox.html',
                           partners=partners, active_partner=active_partner,
                           messages=messages, unread_count=unread_count,
                           unread_only=unread_only)


@chat_bp.route('/message/send', methods=['POST'])
@login_required
def send_message():
    recipient_id = request.form.get('recipient_id', type=int)
    body = request.form.get('body', '').strip()

    if not recipient_id:
        return jsonify({'error': 'Missing recipient.'}), 400
    if not body:
        return jsonify({'error': 'Message cannot be empty.'}), 400
    if len(body) > MAX_MSG:
        return jsonify({'error': f'Message too long (max {MAX_MSG} chars).'}), 400
    if recipient_id == current_user.id:
        return jsonify({'error': 'Cannot message yourself.'}), 400

    recipient = User.query.get(recipient_id)
    if not recipient:
        return jsonify({'error': 'User not found.'}), 404

    msg = Message(sender_id=current_user.id, recipient_id=recipient_id, body=body)
    notif = Notification(
        user_id=recipient_id, type='message',
        title=f'New message from {current_user.username}',
        body=body[:80] + ('…' if len(body) > 80 else ''),
        link=f'/inbox?with={current_user.id}',
    )
    db.session.add_all([msg, notif])
    db.session.commit()

    from app import socketio
    socketio.emit('new_message', msg.to_dict(), room=f'user_{recipient_id}')
    socketio.emit('notification', {
        'type': 'message', 'title': notif.title, 'body': notif.body,
    }, room=f'user_{recipient_id}')

    return jsonify({'success': True, 'message': msg.to_dict()})


@chat_bp.route('/api/notifications')
@login_required
def get_notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(
        Notification.created_at.desc()).limit(20).all()
    unread = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify({'notifications': [n.to_dict() for n in notifs], 'unread_count': unread})


@chat_bp.route('/api/notifications/read', methods=['POST'])
@login_required
def mark_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    return jsonify({'success': True})


def register_socketio_events(socketio):
    from flask_socketio import join_room, leave_room

    @socketio.on('connect')
    def on_connect():
        if current_user.is_authenticated:
            join_room(f'user_{current_user.id}')

    @socketio.on('disconnect')
    def on_disconnect():
        if current_user.is_authenticated:
            leave_room(f'user_{current_user.id}')

    @socketio.on('send_message')
    def on_send_message(data):
        if not current_user.is_authenticated:
            return
        recipient_id = data.get('recipient_id')
        body = (data.get('body') or '').strip()
        if not recipient_id or not body or len(body) > MAX_MSG:
            return
        try:
            recipient_id = int(recipient_id)
        except (ValueError, TypeError):
            return
        if recipient_id == current_user.id:
            return
        recipient = User.query.get(recipient_id)
        if not recipient:
            return
        msg = Message(sender_id=current_user.id, recipient_id=recipient_id, body=body)
        db.session.add(msg)
        db.session.commit()
        socketio.emit('new_message', msg.to_dict(), room=f'user_{recipient_id}')
        socketio.emit('message_sent', msg.to_dict(), room=f'user_{current_user.id}')
