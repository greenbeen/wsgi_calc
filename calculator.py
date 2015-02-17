
math_list = ["add", "subtract", "multiply", "divide"]


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        body = resolve_path(path)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1><br>Your choices are 'add', 'subtract', 'multiply' or 'divide'"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]


def resolve_path(path):
    if path is '/':
        return home_page()
    address_list = path.lstrip('/').split('/')
    math = address_list[0]
    numbers = map(int, address_list[1:])
    if len(numbers) <= 1 and math in math_list:
        return "<h1>You need to provide at least two numbers!</h1>"

    if math == "add":
        return add(numbers)
    elif math == "subtract":
        return subtract(numbers)
    elif math == "multiply":
        return multiply(numbers)
    elif math == "divide":
        return divide(numbers)

    # we get here if no url matches
    raise NameError

def add(numbers):
    problem = '+'.join(map(str,numbers))
    answer = str(sum(numbers))
    response = formated('+', numbers, answer)
    return response

def subtract(numbers):
    first_num = numbers[0]
    rest = numbers[1:]
    for num in rest:
        first_num -= num
    answer = str(first_num)
    response = formated('-', numbers, answer)
    return response


def multiply(numbers):
    first_num = numbers[0]
    rest = numbers[1:]
    for num in rest:
        first_num *= num
    answer = str(first_num)
    response = formated('*', numbers, answer)
    return response

def divide(numbers):
    first_num = numbers[0]
    rest = numbers[1:]
    for num in rest:
        first_num /= num
    answer = str(first_num)
    response = formated('/', numbers, answer)
    return response

def formated(operator, numbers, answer):
    problem = operator.join(map(str, numbers))
    answer = "{} = {}".format(problem, answer)
    return answer



def home_page():
    home = """<h1>Calculator Home Page</h1>
            <br>
            To use this site, type the function you would like to use<br>
            You can choose from '/add', '/subtract', '/multiply' or '/divide'<br>
            Then list the numbers with a '/' between<br>
            <br>
            Example: localhost:8080/add/2/3    This will add 2+3<br>"""
    return home




if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8088, application)
    srv.serve_forever()