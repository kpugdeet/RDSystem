
class LDA:
    def __init__(self):
        print ("Initial LDA")

    def calRanking (self, metaCard, userPref):
        rankList = {}
        rankList["0"] = "Document 0 is a document"
        rankList["1"] = "Document 1 is a document"
        rankList["2"] = "Document 2 is a document"
        rankList["3"] = "Document 3 is a document"
        return rankList

    def train (self, itemID, itemDes):
        print ("Train LDA")
        itemValue = []

        # Calculate topic distribution of each item
        for row in itemID:
            itemValue.append('1,2,3,10')

        return itemValue

    def calDistri (self, text):
        result = '1,2,3,4'

        return result