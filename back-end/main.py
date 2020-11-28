from dotenv import load_dotenv
from dictionary_constructor import dictionary_constructor

load_dotenv()

def main(user_name, hashtags_in):
    dictionary_constructor(user_name, hashtags_in)

if __name__ == '__main__':
    main(user_name='balr',hashtags_in=['balr','Balr','BALR'])