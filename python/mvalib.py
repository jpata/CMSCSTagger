
class Data(object):
    def __init__(self, **kwargs):
        self.classes = kwargs.get("classes", [])
        self.name = kwargs.get("name")
        
    def selection(self, sel):
        """
        Applies selection on the data.
        """
        pass

    def load(self):
        pass
        
    def get_category(self, category):
        """
        Returns the data in a category.
        Category is "test", "train".

        Arguments:
            category (string) - the category to get

        Returns (Data): selected data
        """
        pass
        
    def __len__(self):
        pass


class TrainingReport(object):
    pass


class Classifier(object):
    def __init__(self, **kwargs):
        pass

    def prepare(self):
        pass

    def add_class(self, class_name, class_id, data):
        pass

    def train(self, data):
        pass

    def evaluate(self, data):
        pass
