import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


from src import execute




if __name__ == "__main__":
    obj = execute.Execute()
    while True:
        user_input = input(">>").strip()
        result = obj.route(user_input)
        print(result)
