from pwdlib import PasswordHash
from .config import config


password_hasher = PasswordHash.recommended()


def get_password_hash(password:str)->str:
    return password_hasher.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return password_hasher.verify(plain_password, hashed_password)


#testing

if __name__== "__main__":
    hashed = get_password_hash("somethin of a difficult")
    is_valid = verify_password("somethin of a difficult", hashed)
    is_not_valid = verify_password("somethin of a difficult!  not", hashed)
    print(hashed)