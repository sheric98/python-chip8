class Keyboard:
    def __init__(self):
        self.keys = [False] * 16
        self.kp = None
        self.kp_wait = False

    def set_keys(self, keys):
        self.keys = keys

    def press_key(self, key):
        self.keys[key] = True

    def lift_key(self, key):
        self.keys[key] = False

    def get_key(self, key):
        return self.keys[key]

    def push_keypress(self, key):
        if self.kp_wait:
            self.kp = key

    def wait_keypress(self):
        if self.kp_wait:
            if self.kp:
                key = self.kp
                self.kp = None
                self.kp_wait = False
                return key
            else:
                return None
        else:
            self.kp = None
            self.kp_wait = True
            return None
