def hello():
    print("Hello world :D")

def world():
    """
    This function prints the world

    ..and its really cool!
    """
    print("The whole world")

def add_hello(input):
    return input+", hello!"

class HelloWorld:
    def __init__(self):
        self.hello = "Hello"
        self.world = "World"
    
    def print_hello_world(self):
        print(f"{self.hello} {self.world}")

    def __str__(self):
        return f"{self.hello} {self.world}"