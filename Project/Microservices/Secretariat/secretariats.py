class secretariats:
    def __init__(self, Location, Name, Description, OpeningHours):
        self.Name = Name
        self.Location = Location
        self.Description = Description
        self.OpeningHours = OpeningHours

    def __str__(self):
        return "%d - %s - %s - %s" % (self.Location, self.Name, self.Description, self.OpeningHours)

