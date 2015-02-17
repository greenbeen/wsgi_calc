import sys
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
    """Depending on what url is passed, this will return the correlated problem/answer"""
    if path is '/':
        return home_page()
    # Splits operator from numbers in uri
    address_list = path.lstrip('/').split('/')
    # Pulls the type of math to be done from the uri
    math = address_list[0]
    # Converts string numbers to float, then back to string to allow eval statement
    # to function properly with division of uneven numbers 
    numbers = map(str, map(float, address_list[1:]))
    if len(numbers) <= 1 and math in math_list:
        return "<h1>You need to provide at least two numbers!</h1>"
    if math in math_list:
        operators = {"add": " + ", "subtract": " - ", "multiply": " * ", "divide": " / "}
        problem = ""
        for num in numbers:
            problem += num + operators[math]
        # Removing the last 2 removes an ending space and operator from string
        problem = problem[:-2]
        answer = str(eval(problem))
        return "{} = <b>{}</b>".format(problem, answer)

    # we get here if no url matches
    raise NameError


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
    srv = make_server('localhost', 8088, application) # Please note using 8088 port number
    srv.serve_forever()