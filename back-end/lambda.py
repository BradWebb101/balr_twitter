from dictionary_constructor import dictionary_constructor

def handler(event, context): 
    dictionary_constructor(user_name='balr',hashtags_in=['balr','Balr','BALR'])
    return {
        'statusCode':'200'
    }


