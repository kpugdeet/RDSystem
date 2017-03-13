
class LDA:
    def __init__(self):
        self.rankList = {}
        print ("Initial LDA")

    def calRanking (self, metaCard, userPref):
        print metaCard
        print userPref

        self.rankList["0"] = "Document 0 is a document"
        self.rankList["1"] = "Document 1 is a document"
        self.rankList["2"] = "Document 2 is a document"
        self.rankList["3"] = "Document 3 is a document"
        return self.rankList

    def train (self, itemID, itemDes):
        print ("Train LDA")
        itemValue = []

        # Calculate topic distribution of each item
        for row in itemID:
            itemValue.append('1,2,3,0')

        return itemValue