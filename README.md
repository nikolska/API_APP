# API_APP

Blog written with Django Rest Framework.

<h3>Features:</h3>

- <i>articles/</i> : list + create (IsAuthenticatedOrReadOnly)

- <i>article/pk/</i> : retrieve + update (IsAuthorOrReadOnly)
 
- <i>comments/</i> : list + create (IsAuthenticatedOrReadOnly)

- <i>comments/new/pk/</i> : create (IsAuthenticated)

- <i>comments/pk/</i> : retrieve + update (IsAuthorOrReadOnly)
