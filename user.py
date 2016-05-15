class user:
    username=None;
    password=None;
    activo = False;

    def __init__(self, user, password):
        self.username = user;
        self.password = password;

    def activar(self, a):
        self.activo=a

        