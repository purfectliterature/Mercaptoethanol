class Assessment:
    def __init__(self, id, title):
        self.id = id
        self.title = title
    
    def __str__(self):
        return f"<Assessment {self.id} {self.title}>"

    def to_pair(self):
        return (self.id, self.title)

    def filename(self):
        return self.title.replace(":", "") + ".zip"
