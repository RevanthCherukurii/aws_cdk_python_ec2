import aws_cdk as core
import aws_cdk.assertions as assertions

from python_app.python_app_stack import PythonAppStack


# example tests. To run these tests, uncomment this file along with the example
# resource in python_app/python_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PythonAppStack(app, "python-app")
    template = assertions.Template.from_stack(stack)

