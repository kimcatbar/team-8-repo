from app import myapp_obj, db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegistrationForm
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

@myapp_obj.route('/')
def home():
    return render_template('home.html')


@myapp_obj.route('/login', methods=['GET', 'POST'])           #when a user logs in it checks with the database if the user exists
def login():
    form = LoginForm()
    if form.validate_on_submit():
        current_user = User.query.filter_by(username=form.username.data).first()
        if current_user:
            if check_password_hash(current_user.password, form.password.data):
                login_user(current_user, remember=form.remember_me.data)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@myapp_obj.route('/dashboard', methods=['GET', 'POST'])              
@login_required
def dashboard():
    return render_template('dashboard.html')


@myapp_obj.route('/logout', methods=['GET', 'POST'])                 #logout form
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@myapp_obj.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@myapp_obj.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    current_user.remove()
    db.session.commit()
    flash("Account has been deleted.")
    return redirect('/home')

@myapp_obj.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@myapp_obj.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@myapp_obj.route('/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)

@myapp_obj.route('/messages/', methods=['POST', 'GET'])
@login_required
def messages():


	if request.args.get('thread_id'):

		#Thread ownership security check
		if not db.session.query(Message).filter(Message.thread_id == request.args.get('thread_id'), Message.recipient_id == current_user.username) \
		or not db.session.query(Message).filter(Message.thread_id == request.args.get('thread_id'), Message.sender_id == current_user.username):
			abort(404)
		

		#Fetches non deleted messages in the thread for the current user.
		message_thread_sender = db.session.query(Message).filter(Message.thread_id == request.args.get('thread_id'), Message.sender_id == current_user.username, Message.sender_del == False)
		message_thread_recipient = db.session.query(Message).filter(Message.thread_id == request.args.get('thread_id'), Message.recipient_id == current_user.username, Message.recipient_del == False)
		message_thread = message_thread_sender.union(message_thread_recipient).order_by(Message.timestamp.asc())
		

		if not message_thread.count():
				abort(404)


		#Custom pagination handler. Helps with older message ajax fetch requests and first /messages/ pull request offset.
		thread_count = len(message_thread.all())
		if thread_count <= 5:
			offset = 0
		else:
			offset = thread_count-5
		message_thread_paginated = message_thread.offset(offset).limit(5)

		if request.args.get('fetch'): #Need to see if database check for existence is needed here / how flask handles error when in production.

			fetch_last_query = db.session.query(Message).filter(Message.url == request.args.get('fetch')).one()
			testq = message_thread_sender.union(message_thread_recipient).order_by(Message.timestamp.asc()).filter(Message.id < fetch_last_query.id) #Replace this union alreay occurs above.
			testq_count = testq.count()
			if testq_count-5 < 0:
				offsetcnt = 0
			else:
				offsetcnt = testq_count-5
			testq = testq.offset(offsetcnt)

			fetched_messages = render_template('fetch_new_message.html', message_thread=testq)
			return {'status': 200, 'fetched_messages': fetched_messages, 'offsetcnt':offsetcnt}
		

		#This marks all messages within thread that are in the current_user's unread as read upon thread open if current user is recipient.
		for message in message_thread:
			if current_user.username == message.recipient_id:
				if message.read == False:
					message.read = True
					db.session.commit()
		

		#This sets the recipient ID on replies so even if a user is sending themself a thread the recipient ID will be correct. Possibly/probably refactor.
		if current_user.username == message_thread[0].sender_id:
			recip = message_thread[0].recipient_id
		else:
			recip = message_thread[0].sender_id
		

		#Notifies socket if messages are all read to sync orange mailbox notification.
		if not db.session.query(Message).filter(Message.recipient_id == current_user.username, Message.read == False).all():
			socketio.emit(current_user.websocket_id+'_notify', {'type':'mailbox', 'notify':'false'}, namespace='/messages')
		

		#Notifies socket when the thread is read so the messages page may update read/unread.
		socketio.emit(current_user.websocket_id+'_notify', {'type':'thread', 'notify':'false', 'thread_id':request.args.get('thread_id')}, namespace='/messages')
		

		return render_template('read_message_thread.html', message_thread=message_thread_paginated, thread_id=request.args.get('thread_id'),\
								recip=recip, thread_count=thread_count)


	else:
		page = request.args.get('page', 1, type=int)

		unread_messages = db.session.query(Message).filter(Message.recipient_id == current_user.username, Message.recipient_del == False).order_by(Message.timestamp.desc())


		#This sorts each message thread properly according to the datetime of the last recieved message in each thread which is then used in the custom sort_order
		unread_ids = {}

		for message in unread_messages:
			if not unread_ids.get(message.thread_id):
				unread_ids[message.thread_id] = len(unread_ids)+1
		if not unread_ids:
			sort_order = None
		else:
			sort_order = case(value=Message.thread_id, whens=unread_ids).asc()
		##########


		#This fixes message threads viewed on /messages/ so duplicates will not be displayed, using sqlalchemy's '.in_' for query on list items
		thread_list = []
		message_thread_list = []
		for message in unread_messages:
			if message.thread_id not in thread_list:
				thread_list.append(message.thread_id)
				message_thread_list.append(message.url)
		##########


		message_threads = unread_messages.filter(Message.url.in_(message_thread_list)).order_by(sort_order)


		#Determines what is highlighted on the private messages screen for new unread messages and threads. List is passed to messages.html where Jinja2 logic executes.
		unread_threads = unread_messages.filter(Message.read == False).order_by(Message.timestamp.desc()).all()
		if unread_threads:
			unread_threads_list = []
			for message in unread_threads:
				unread_threads_list.append(message.thread_id)
		else:
			unread_threads_list = []
		##########


		message_threads = message_threads.paginate(page, 5, False)

		#This returns rendered threads for insert when the "Load additional threads" button is clicked on /Messages/
		if page > 1:
			paged_threads = render_template('fetch_new_thread.html', messages=message_threads.items, unread_threads_list=unread_threads_list)

			if not unread_messages.filter(Message.url.in_(message_thread_list)).order_by(sort_order).paginate(page+1, 5, False).items:
				fetch_button = 'false'
			else:
				fetch_button = 'true'

			return {'status':200, 'threads':paged_threads, 'fetch_button':fetch_button}
        ##########

		#Determines if the fetch additional threads button is shown on the /messages/ page.
		if len(message_thread_list) > 5:
			fetch_button = 'true'
		else:
			fetch_button = 'false'
		##########

		return render_template('messages.html', messages=message_threads.items, unread_threads_list=unread_threads_list, fetch_button=fetch_button)



@myapp_obj.route('/messages/socket/', methods=['POST', 'GET']) #Add additional db check here for sender/recip del true and return 404 if so.
@login_required
def message_socket():

	message = db.session.query(Message).filter(Message.url == request.args.get('url')).all()

	if not message:
		abort(404)

	if current_user.username == message[0].recipient_id or current_user.username == message[0].sender_id:
		pass
	else:
		return {'status': 401}


	if current_user.username == message[0].recipient_id and request.args.get('read'):
		message[0].read = True #Maybe change this to ajax request when div is scrolled into view.
		db.session.commit()

		if not db.session.query(Message).filter(Message.recipient_id == current_user.username, Message.read == False, Message.recipient_del == False).all():
			socketio.emit(current_user.websocket_id+'_notify', {'type':'mailbox', 'notify':'false'}, namespace='/messages')


	if request.args.get('read'):
		socketio.emit(current_user.websocket_id+'_notify', {'type':'thread', 'notify':'false', 'thread_id':message[0].thread_id}, namespace='/messages')
		render_message = render_template('fetch_new_message.html', message_thread=message)
		return {'status':200, 'message':render_message}
	else:
		render_thread = render_template('fetch_new_thread.html', messages=message, unread_threads_list=[message[0].thread_id])
		return {'status':200, 'thread':render_thread, 'thread_id':message[0].thread_id}


@myapp_obj.route('/messages/new/', methods=['POST', 'GET'])
@login_required
def sendmessage():

	if request.method == 'GET':
		return render_template('send_message.html')


	if request.method == 'POST':

		#Data security checks
		if request.json.get('body') == '' or request.json.get('body') == None or len(request.json.get('subject')) > 70:
			return {'status':418}

		#Mitigates messaging attacks by ensuring thread_id has not been modified on the end user computer by checking thread ownership.
		if request.json.get('thread_id'):
			if db.session.query(Message).filter(Message.thread_id == request.json.get('thread_id'), Message.sender_id == current_user.username).all() or \
				db.session.query(Message).filter(Message.thread_id == request.json.get('thread_id'), Message.recipient_id == current_user.username).all():
				pass
			else:
				return {'status': 418}
		


		#Username exists validator
		if not db.session.query(User).filter(User.username == request.json.get('recipient_id').lower()).first():
			return {'error':'No user exists with that username.'}
		


		url = randstrurl(type=Message)
		timestamp=datetime.utcnow()

		if request.json.get('thread_id'):
			thread_id = request.json.get('thread_id')
			thread_query = db.session.query(Message).filter(Message.thread_id == thread_id)
			subject = thread_query.order_by(Message.timestamp.desc()).first().subject

		else:
			thread_id = randstrurl(type=Message, pmthread=True)
			subject = request.json.get('subject')


		new_message = Message(sender_id=current_user.username, recipient_id=request.json.get('recipient_id').lower(), subject=subject, body=request.json.get('body'), url=url, \
						 thread_id=thread_id, timestamp=timestamp, sender_del=False, recipient_del=False)
		db.session.add(new_message)
		db.session.commit()


		recipient_websocket_id = db.session.query(User).filter(User.username == request.json.get('recipient_id').lower()).one().websocket_id

		socketio.emit(recipient_websocket_id+'_newmsg', {'message_url' : url}, namespace='/messages') #Recipient websocket messages home listener
		socketio.emit(current_user.websocket_id+'_newmsg', {'message_url' : url}, namespace='/messages') #Messages home listener/thread fetch for sender (Maybe not needed)
		socketio.emit(thread_id, {'message_url' : url}, namespace='/messages') #In thread listener

		return {'status': 200}
