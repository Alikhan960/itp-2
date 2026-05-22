# Name: Alikhan Yertaiuly
# Group: SE-2504

import re
import time
import datetime
from abc import ABC, abstractmethod


# ============================================================
# TASK 1: Method Logging Decorator
# ============================================================

log_entries = []

def log_action(func):
    def wrapper(self, *args, **kwargs):
        class_name = self.__class__.__name__
        method_name = func.__name__
        result = func(self, *args, **kwargs)
        print(f"[LOG] {class_name}.{method_name} executed")
        entry = f"{class_name} | {method_name} | {result if result is not None else 'success'}"
        log_entries.append(entry)
        return result
    return wrapper


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    @log_action
    def login(self):
        return "success"

    @log_action
    def logout(self):
        return "success"


class Student(User):
    def __init__(self, username, email, student_id, gpa):
        super().__init__(username, email)
        self.student_id = student_id
        self.gpa = gpa

    @log_action
    def submit_assignment(self, course, score):
        return f"score={score}"

    @log_action
    def view_gpa(self):
        return str(self.gpa)


class Teacher(User):
    def __init__(self, username, email, teacher_id, department):
        super().__init__(username, email)
        self.teacher_id = teacher_id
        self.department = department

    @log_action
    def grade_student(self, student_name, score):
        return f"{student_name}={score}"

    @log_action
    def create_exam(self, course_name):
        return course_name


print("=" * 50)
print("TASK 1: Method Logging Decorator")
print("=" * 50)

alice = Student("alice01", "alice@email.com", "S001", 3.8)
bob   = Student("bob02",   "bob@email.com",   "S002", 3.5)
prof  = Teacher("prof_smith", "smith@email.com", "T001", "Computer Science")

users = [alice, bob, prof]

print("\n--- Login ---")
for user in users:
    user.login()

print("\n--- Student Actions ---")
alice.submit_assignment("Python Programming", 95)
alice.view_gpa()
bob.submit_assignment("Data Structures", 88)

print("\n--- Teacher Actions ---")
prof.grade_student("Alice", 95)
prof.create_exam("Python Programming")

print("\n--- Logout ---")
for user in users:
    user.logout()

with open("system_logs.txt", "w") as f:
    for entry in log_entries:
        f.write(entry + "\n")

print("\n--- Log File Content ---")
with open("system_logs.txt", "r") as f:
    print(f.read())


# ============================================================
# TASK 2: Secure Banking System with Decorators
# ============================================================

def require_login(func):
    def wrapper(self, *args, **kwargs):
        if not self._BankAccount__is_logged_in:
            print("Access denied. Please login first.")
            return None
        return func(self, *args, **kwargs)
    return wrapper

def validate_transaction(func):
    def wrapper(self, *args, **kwargs):
        amount = args[1] if func.__name__ == "transfer" else args[0]
        if amount <= 0:
            print("Transaction failed: invalid amount.")
            return None
        return func(self, *args, **kwargs)
    return wrapper


class BankAccount:
    def __init__(self, owner, password, initial_balance=1000):
        self.__owner = owner
        self.__balance = initial_balance
        self.__is_logged_in = False
        self.__password = password
        self.__transactions = []

    def login(self, password):
        if password == self.__password:
            self.__is_logged_in = True
            print(f"Login successful. Welcome, {self.__owner}!")
        else:
            print("Login failed: incorrect password.")

    def logout(self):
        self.__is_logged_in = False
        print(f"{self.__owner} logged out.")

    @require_login
    @validate_transaction
    def deposit(self, amount):
        self.__balance += amount
        self.__transactions.append(f"DEPOSIT -> {amount}")
        print(f"Deposited: {amount}")
        print(f"Current balance: {self.__balance}")

    @require_login
    @validate_transaction
    def withdraw(self, amount):
        if amount > self.__balance:
            print(f"Withdrawal failed: insufficient funds.")
            return
        self.__balance -= amount
        self.__transactions.append(f"WITHDRAW -> {amount}")
        print(f"Withdrawn: {amount}")
        print(f"Current balance: {self.__balance}")

    @require_login
    @validate_transaction
    def transfer(self, other_account, amount):
        if amount > self.__balance:
            print("Transfer failed: insufficient funds.")
            return
        self.__balance -= amount
        other_account._BankAccount__balance += amount
        self.__transactions.append(f"TRANSFER -> {amount} to {other_account._BankAccount__owner}")
        other_account._BankAccount__transactions.append(f"RECEIVED -> {amount} from {self.__owner}")
        print(f"Transferred {amount} to {other_account._BankAccount__owner}.")

    @require_login
    def show_balance(self):
        print(f"[{self.__owner}] Balance: {self.__balance}")

    def transaction_generator(self):
        for t in self.__transactions:
            yield t


print("\n" + "=" * 50)
print("TASK 2: Secure Banking System with Decorators")
print("=" * 50)

alice_acc = BankAccount("Alice", "alice_pass", initial_balance=1000)
bob_acc   = BankAccount("Bob",   "bob_pass",   initial_balance=500)

print("\n--- Access without login ---")
alice_acc.deposit(200)

print("\n--- Alice logs in ---")
alice_acc.login("alice_pass")
alice_acc.deposit(500)
alice_acc.withdraw(200)

print("\n--- Bob logs in ---")
bob_acc.login("bob_pass")

print("\n--- Transfer ---")
alice_acc.transfer(bob_acc, 300)
alice_acc.transfer(bob_acc, 99999)  # should fail

print("\n--- Balances ---")
alice_acc.show_balance()
bob_acc.show_balance()

print("\n--- Transactions ---")
for t in alice_acc.transaction_generator():
    print(t)
for t in bob_acc.transaction_generator():
    print(t)

alice_acc.logout()
bob_acc.logout()


# ============================================================
# TASK 3: Performance Monitoring with Iterators
# ============================================================

def measure_time(func):
    def wrapper(self, *args, **kwargs):
        start = time.perf_counter()
        result = func(self, *args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{func.__name__} executed in {elapsed:.4f} ms")
        return result
    return wrapper


class ScoreIterator:
    def __init__(self, scores):
        self._scores = scores
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._scores):
            raise StopIteration
        value = self._scores[self._index]
        self._index += 1
        return value


class StudentAnalytics:
    def __init__(self, course_name, scores):
        self.course_name = course_name
        self.scores = scores

    @measure_time
    def calculate_average(self):
        return sum(self.scores) / len(self.scores)

    @measure_time
    def highest_score(self):
        return max(self.scores)

    @measure_time
    def lowest_score(self):
        return min(self.scores)

    @measure_time
    def sort_scores(self):
        return sorted(self.scores)

    @measure_time
    def generate_report(self):
        avg     = sum(self.scores) / len(self.scores)
        highest = max(self.scores)
        lowest  = min(self.scores)
        return (
            f"Course: {self.course_name}\n"
            f"Average Score: {avg:.2f}\n"
            f"Highest Score: {highest}\n"
            f"Lowest Score: {lowest}\n"
            f"Sorted Scores: {sorted(self.scores)}\n"
        )


print("\n" + "=" * 50)
print("TASK 3: Performance Monitoring with Iterators")
print("=" * 50)

#  scores.txt
with open("scores.txt", "w") as f:
    f.write("78 91 85 99 61 93\n")

with open("scores.txt", "r") as f:
    scores = [int(x) for x in f.read().split()]

print("\n--- Scores via ScoreIterator ---")
for score in ScoreIterator(scores):
    print(f"  Score: {score}")

analytics = StudentAnalytics("Python Programming", scores)

print("\n--- Analytics ---")
avg     = analytics.calculate_average()
highest = analytics.highest_score()
lowest  = analytics.lowest_score()
sorted_ = analytics.sort_scores()
report  = analytics.generate_report()

print(f"\n--- Analytics Report ---")
print(f"Average Score: {avg:.1f}")
print(f"Highest Score: {highest}")
print(f"Lowest Score: {lowest}")

with open("analytics_report.txt", "w") as f:
    f.write(report)

print("Report saved to analytics_report.txt")


# ============================================================
# TASK 4: Regex Validation System with Class Decorators
# ============================================================

EMAIL_RE    = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$')
PHONE_RE    = re.compile(r'^\+7\d{10}$')
EMP_ID_RE   = re.compile(r'^EMP-\d{4}$')
PASSWORD_RE = re.compile(r'^(?=.*[A-Z])(?=.*\d).{8,}$')

def validate_fields(cls):
    original_init = cls.__init__
    def new_init(self, name, employee_id, email, phone, password, department):
        if not EMAIL_RE.match(email):
            raise ValueError(f"Invalid email format.")
        if not PHONE_RE.match(phone):
            raise ValueError(f"Invalid phone number format.")
        if not EMP_ID_RE.match(employee_id):
            raise ValueError(f"Invalid employee ID format.")
        if not PASSWORD_RE.match(password):
            raise ValueError(f"Weak password.")
        original_init(self, name, employee_id, email, phone, password, department)
    cls.__init__ = new_init
    return cls


@validate_fields
class Employee:
    def __init__(self, name, employee_id, email, phone, password, department):
        self.name        = name
        self.employee_id = employee_id
        self.email       = email
        self.phone       = phone
        self.__password  = password
        self.department  = department

    def display_profile(self):
        print(f"  {self.employee_id} | {self.name} | {self.department} | {self.email}")

    def change_password(self, new_password):
        if not PASSWORD_RE.match(new_password):
            raise ValueError("Weak password.")
        self.__password = new_password
        print(f"Password updated for {self.name}.")

    def update_phone(self, new_phone):
        if not PHONE_RE.match(new_phone):
            raise ValueError(f"Invalid phone number format.")
        self.phone = new_phone
        print(f"Phone updated for {self.name}: {new_phone}")


print("\n" + "=" * 50)
print("TASK 4: Regex Validation System with Class Decorators")
print("=" * 50)

candidates = [
    ("Alice Brown", "EMP-1001", "alice@test.com",  "+77071234567", "Secure123", "IT"),
    ("Bob Smith",   "EMP-1002", "bob@company.org", "+77779876543", "Hello@999", "Finance"),
    ("Carol Doe",   "EMP-1003", "bad-email",        "+77071234567", "Secure123", "HR"),
    ("Dan Lee",     "EMP1004",  "dan@ok.com",        "+77071111111", "Secure123", "IT"),
    ("Eve White",   "EMP-1005", "eve@ok.com",        "+77072222222", "weakpass",  "Sales"),
]

valid_employees   = []
invalid_entries   = []

for (name, emp_id, email, phone, password, dept) in candidates:
    try:
        emp = Employee(name, emp_id, email, phone, password, dept)
        print(f"Employee created successfully: {name}")
        emp.display_profile()
        valid_employees.append(emp)
    except ValueError as e:
        print(f"Validation Error: {e}")
        invalid_entries.append(f"{emp_id} | {name} | ERROR: {e}")

print("\n--- Update operations ---")
try:
    valid_employees[0].change_password("NewPass99")
    valid_employees[0].update_phone("+77070000000")
    valid_employees[0].update_phone("bad-number")
except ValueError as e:
    print(f"Validation Error: {e}")

with open("employees_valid.txt", "w") as f:
    f.write("--- Valid Employees ---\n")
    for emp in valid_employees:
        f.write(f"{emp.employee_id} | {emp.name} | {emp.department}\n")

with open("employees_invalid.txt", "w") as f:
    f.write("--- Invalid Entries ---\n")
    for entry in invalid_entries:
        f.write(entry + "\n")

print("\n--- Valid Employees ---")
with open("employees_valid.txt", "r") as f:
    print(f.read())

print("--- Invalid Entries ---")
with open("employees_invalid.txt", "r") as f:
    print(f.read())


# ============================================================
# TASK 5: Plugin-Based Text Processing System
# ============================================================

plugin_registry = []

def register_plugin(cls):
    plugin_registry.append(cls)
    return cls


class TextPlugin(ABC):
    @abstractmethod
    def process(self, text):
        pass

    @abstractmethod
    def plugin_info(self):
        pass


@register_plugin
class WordCounterPlugin(TextPlugin):
    def plugin_info(self):
        return "Counts total words in the text."
    def process(self, text):
        words = re.findall(r'\b\w+\b', text)
        return {"Total Words": len(words)}

@register_plugin
class EmailExtractorPlugin(TextPlugin):
    def plugin_info(self):
        return "Extracts all email addresses."
    def process(self, text):
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        return {"Emails Found": emails}

@register_plugin
class HashtagExtractorPlugin(TextPlugin):
    def plugin_info(self):
        return "Extracts all hashtags."
    def process(self, text):
        hashtags = re.findall(r'#\w+', text)
        return {"Hashtags Found": hashtags}

@register_plugin
class SentenceStatisticsPlugin(TextPlugin):
    def plugin_info(self):
        return "Counts sentences and average words per sentence."
    def process(self, text):
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        avg = sum(len(re.findall(r'\b\w+\b', s)) for s in sentences) / len(sentences) if sentences else 0
        return {"Total Sentences": len(sentences), "Avg Words/Sentence": round(avg, 2)}


def line_reader(filepath):
    with open(filepath, "r") as f:
        for line in f:
            yield line.rstrip("\n")


class TextEngine:
    def __init__(self):
        self._plugins = [cls() for cls in plugin_registry]
        self._results = {}

    def run_all(self, text):
        for plugin in self._plugins:
            self._results[type(plugin).__name__] = plugin.process(text)

    def export_report(self, filepath):
        with open(filepath, "w") as f:
            f.write("=== Text Analysis Report ===\n\n")
            for name, data in self._results.items():
                f.write(f"[{name}]\n")
                for key, val in data.items():
                    f.write(f"  {key}: {val}\n")
                f.write("\n")

    def print_results(self):
        for name, data in self._results.items():
            print(f"[{name}]")
            for key, val in data.items():
                print(f"  {key}: {val}")


print("\n" + "=" * 50)
print("TASK 5: Plugin-Based Text Processing System")
print("=" * 50)

#  sample_text.txt
with open("sample_text.txt", "w") as f:
    f.write("Contact admin@test.com for updates and info@company.org for support.\n")
    f.write("#python #decorators are useful for clean code.\n")
    f.write("Python is a great language for beginners and experts alike.\n")
    f.write("Make sure to email support@example.com if you have any issues.\n")
    f.write("#programming #coding are trending topics today.\n")

print("\nRegistered Plugins:")
for cls in plugin_registry:
    print(f"  - {cls.__name__}")

print("\n--- Reading file line by line ---")
lines = []
for line in line_reader("sample_text.txt"):
    print(f"  {line}")
    lines.append(line)

full_text = "\n".join(lines)

engine = TextEngine()
engine.run_all(full_text)

print("\n--- Processing Results ---")
engine.print_results()

engine.export_report("analysis_report.txt")
print("\nReport saved to analysis_report.txt")