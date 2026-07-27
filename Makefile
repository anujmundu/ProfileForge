install:
\tpip install -r requirements.txt

test:
\tpytest

dashboard:
\tpython -m src.dashboard.generator
