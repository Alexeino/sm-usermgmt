from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


class Hasher:
        
    @staticmethod
    def verify_password(plain_pwd,hashed_pwd):
        return Hasher.pwd_context.verify(plain_pwd,hashed_pwd)
    
    @staticmethod
    def get_pwd_hash(pwd):
        return pwd_context.hash(pwd)