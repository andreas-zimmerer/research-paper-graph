# research-paper-graph

# Project Setup

## Backend

The backend is a Python application with Flask framework.

Some good starting resources are:
 - [The Flask mega tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
 - [Flask Project Website](https://palletsprojects.com/p/flask/)

### Virtualenv
This project uses `virtualenv` to make dependency management easier.
To activate the virtual environment on your command line, run
```
source venv/bin/activate
```
Now you should have python, pip and everything else available.

### Bare Python
If you don't want to use `virtualenv`, you can install the required dependencies with
```
pip install -r requirements.txt
```

### Installing new packages
When installing new packages, make sure that
 - they are in the `virtualenv`
 - they are in the `requirements.txt` file

The first point is simply done by activating the `virtualenv` before installing.
For the second point, run
```
pip freeze > requirements.txt
```
To update the `requirements.txt` file.

### Starting the Backend
To start the backend on a local machine, navigate to the `backend` directory.
Next, activate the `virtualenv` as described before.
Now you can run the backend on [localhost:5000](localhost:5000) by typing
```
flask run
```


## Frontend

The frontend is located in the `frontend` folder and is written in TypeScript with React.

Some good staring resources are:
 - [The TypeScript Handbook](https://www.typescriptlang.org/)
 - [TypeScript Example on React](https://www.typescriptlang.org/play/index.html?jsx=2&esModuleInterop=true&e=196#example/typescript-with-react)
 - [React + TypeScript Cheatsheets](https://github.com/typescript-cheatsheets/react-typescript-cheatsheet#reacttypescript-cheatsheets)
 - [React: Getting Started](https://reactjs.org/docs/getting-started.html)

To build the frontend, make sure you have `npm` or `yarn` installed.
Change to the `frontend` directory and run
```
npm install
```
and then
```
npm start
```

Now the frontend should open in your browser.

If you use `yarn`, issue the same commands but with `yarn` instead of `npm`.

