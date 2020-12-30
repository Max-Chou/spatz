from itsdangerous import URLSafeSerializer, BadSignature

class SessionBase:
    def __init__(self, session_key=None, no_load=False):
        self._session_key = session_key
        self.accessed = False
        self.modified = False
        if session_key is None or no_load:
            self._session = {}
        else:
            self._session = self.load()
        
    @property
    def session_key(self):
        return self._session_key

    @property
    def session(self):
        self.accessed = True
        return self._session

    def __contains__(self, key):
        return key in self.session
    
    def __getitem__(self, key):
        return self.session[key]
    
    def __setitem__(self, key, value):
        self.session[key] = value
        self.modified = True

    def __delitem__(self, key):
        del self.session[key]
        self.modified = True

    def get(self, key, default=None):
        return self.session.get(key, default)

    def pop(self, key, *args):
        self.modified = self.modified or key in self.session
        return self.session.pop(key, *args)

    def setdefault(self, key, value):
        if key in self.session:
            return self.session[key]
        else:
            self.modified = True
            self.session[key] = value
            return value

    def update(self, dict_):
        self.session.update(dict_)
        self.modified = True

    def has_key(self, key):
        return key in self.session

    def keys(self):
        return self.session.keys()

    def values(self):
        return self.session.values()

    def items(self):
        return self.session.items()

    def iterkeys(self):
        return self.session.iterkeys()

    def itervalues(self):
        return self.session.itervalues()

    def iteritems(self):
        return self.session.iteritems()

    def clear(self):
        # To avoid unnecessary persistent storage accesses, we set up the
        # internals directly (loading data wastes time, since we are going to
        # set it to an empty dict anyway).
        self._session = {}
        self.accessed = True
        self.modified = True

    # Methods that child classes must implement.

    def exists(self, session_key):
        """
        Returns True if the given session_key already exists.
        """
        raise NotImplementedError('subclasses of SessionBase must provide an exists() method')

    def create(self):
        """
        Creates a new session instance. Guaranteed to create a new object with
        a unique key and will have saved the result once (with empty data)
        before the method returns.
        """
        raise NotImplementedError('subclasses of SessionBase must provide a create() method')

    def save(self, must_create=False):
        """
        Saves the session data. If 'must_create' is True, a new session object
        is created (otherwise a CreateError exception is raised). Otherwise,
        save() can update an existing object with the same key.
        """
        raise NotImplementedError('subclasses of SessionBase must provide a save() method')

    def delete(self, session_key=None):
        """
        Deletes the session data under this key. If the key is None, the
        current session key value is used.
        """
        raise NotImplementedError('subclasses of SessionBase must provide a delete() method')

    def load(self):
        """
        Loads the session data and returns a dictionary.
        """
        raise NotImplementedError('subclasses of SessionBase must provide a load() method')

    @classmethod
    def clear_expired(cls):
        """
        Remove expired sessions from the session store.

        If this operation isn't possible on a given backend, it should raise
        NotImplementedError. If it isn't necessary, because the backend has
        a built-in expiration mechanism, it should be a no-op.
        """
        raise NotImplementedError('This backend does not support clear_expired().')


class ClientSession(SessionBase):
    def __init__(self, app=None, session_key=None, no_load=False):
        if app is None:
            secret_key = "default"
        else:
            secret_key = app.config["SECRET_KEY"]

        self.serializer = URLSafeSerializer(secret_key)
        super(ClientSession, self).__init__(session_key, no_load)

    def load(self):
        try:
            return self.serializer.loads(self.session_key, salt="client-session")
        except (BadSignature, ValueError):
            self.create()
        return {}

    def create(self):
        self.modified = True

    def exists(self):
        return False

    def save(self):
        self._session_key = self._get_session_key()
        self.modified = True
    
    def delete(self):
        self._session_key = ''
        self._session = {}
        self.modified = True

    def cycle_key(self):
        self.save()

    def _get_session_key(self):
        return self.serializer.dumps(self.session, salt='client-session')

    @classmethod
    def clear_expired(cls):
        pass


class LocMemSession(SessionBase):
    pass