
# Python Starter

A starter template for Python projects, pre-configured with type checking, linting, formatting, unittests, and more. This project provides a solid foundation for clean, maintainable Python code.

---

## 🚀 Setup

1. **Create a virtual environment**  
   To create an isolated environment for your project, run:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**  
   Activate it with the following command:

   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

   On Windows:
   ```bash
   .\venv\Scripts\activate
   ```

3. **Install dependencies**  
   Install all the required dependencies listed in `requirements.txt`:

   ```bash
   pip3 install -r requirements.txt
   ```

   Alternatively, you can use `make` to handle installation:

   ```bash
   make install
   ```

---

## 🔧 Packages

This project includes the following packages for development:

- **[mypy](http://mypy-lang.org/)**: A static type checker for Python, helping ensure that types are consistent and errors are caught early.
- **[flake8](https://flake8.pycqa.org/)**: A linting tool to check your code for style violations and potential errors based on PEP 8 and other best practices.
- **[black](https://black.readthedocs.io/)**: An opinionated code formatter that enforces a consistent code style automatically.
- **[pytest](https://pytest.org/)**: A framework for writing simple and scalable test cases. Ideal for running unit tests and ensuring code reliability.

---

## ⚙️ Usage

You can use `make` for common tasks such as installation and testing:

### Install dependencies
```bash
make install
```

### Run linting with flake8
```bash
make lint
```

### Format code with black
```bash
make format
```

### Run tests with pytest
```bash
make test
```

---

## 📄 Configuration

- **`mypy.ini`**: Configures `mypy` for static type checking.
- **`.flake8`**: Configuration file for `flake8` to enforce your preferred linting rules.
- **`pyproject.toml`**: Configuration for `black` and other tools, ensuring consistent formatting across your project.
- **`Makefile`**: Automates common tasks like installation, linting, formatting, and testing.

---

## 🛠️ Development Workflow

1. Write your Python code in the `src` directory.
2. Use `make lint` to check for style violations.
3. Format your code with `make format` to ensure consistent formatting.
4. Write unit tests in the `tests` directory.
5. Run tests with `make test` to ensure everything works correctly.

---

## 📚 Additional Resources

- **[mypy documentation](http://mypy-lang.org/)** for type checking.
- **[flake8 documentation](https://flake8.pycqa.org/)** for linting setup and rules.
- **[black documentation](https://black.readthedocs.io/)** for understanding code formatting rules.
- **[pytest documentation](https://pytest.org/)** for testing guidelines and examples.

---

This setup ensures that your Python project stays clean, well-tested, and easy to maintain. Happy coding! 🚀
