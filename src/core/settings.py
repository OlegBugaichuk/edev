SECRET_KEY = "112dbdc16a525f7385b84bdae087b6cba40b671890b787bc577848c4e14b60ee"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DB_CONF = {
    'NAME': 'edev',
    'USER': 'project',
    'PASSWORD': 'password',
    'HOST': 'localhost',
}

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_CONF['USER']}:{DB_CONF['PASSWORD']}@{DB_CONF['HOST']}:5432/{DB_CONF['NAME']}"
