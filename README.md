MODELS:
    User: 
        id,
        username,
        password,
        authtoken
    Categorie:
        id,
        user: User,
        name
    ProgrammedMessage:
        id,
        message,
        user: User, 
        messageTo,
        categorie: manytomany(Categorie),

user -> categories -> messageslist