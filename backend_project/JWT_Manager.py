
import jwt


class JWT_Manager():
    def __init__(self, private_path, public_path, algorithm='RS256'):
        self.private_path = private_path
        self.public_path = public_path
        self.algorithm = algorithm

        with open(self.private_path) as f:
            self.private_key_path = f.read()

        with open(self.public_path) as f:
            self.public_key_path = f.read()


    def encode(self, data):
        try:

            encoded = jwt.encode(data, self.private_key_path, algorithm=self.algorithm)
            return encoded
        except Exception as ex:
            print(ex)
            return None


    def decode(self, token):
        try:
            decoded = jwt.decode(token, self.public_key_path, algorithms=[self.algorithm])
            return decoded
        except Exception as ex:
            return None








