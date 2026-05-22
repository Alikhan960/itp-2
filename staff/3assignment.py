# Name: Alikhan Yertaiuly
# Group Number: SE-2504

# TASK 1: Function Arguments
def create_profile(name, age, city="Astana", **kwargs):
    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"City: {city}")
    for key, value in kwargs.items():
        print(f"{key.capitalize()}: {value}")

for i in range(3):
    print(f"\nEntry {i+1}:")
    u_name = input("Enter name: ")
    u_age = input("Enter age: ")
    u_city = input("Enter city (press Enter for default): ")
    u_hobby = input("Enter a hobby: ")
    
    if u_city:
        create_profile(u_name, u_age, city=u_city, hobby=u_hobby)
    else:
        create_profile(u_name, u_age, hobby=u_hobby)
        

# TASK 2: Lambda, Map, and Filter
nums = list(map(int, input("Enter a list of numbers separated by spaces: ").split()))
threshold = int(input("Enter threshold X: "))

squared = list(map(lambda x: x**2, nums))
even_nums = list(filter(lambda x: x % 2 == 0, nums))
greater_than_x = list(filter(lambda x: x > threshold, nums))

print(f"Original list: {nums}")
print(f"Squared numbers: {squared}")
print(f"Even numbers: {even_nums}")
print(f"Numbers greater than {threshold}: {greater_than_x}")

# TASK 3: Basic Class and Object
class Book:
    def __init__(self, title="", author="", pages=0):
        self.title = title
        self.author = author
        self.pages = pages

    def describe(self):
        print(f"The book '{self.title}' by {self.author} has {self.pages} pages.")

books = []
for i in range(3):
    print(f"Enter book {i+1} details:")
    t = input("Title: ")
    a = input("Author: ")
    p = int(input("Number of pages: "))
    books.append(Book(t, a, p))

for b in books:
    b.describe()

# TASK 4: Class with __init__ and __str__
class Rectangle:
    def __init__(self, width, height):
        self.width = float(width)
        self.height = float(height)

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"

w = input("Enter rectangle width: ")
h = input("Enter rectangle height: ")
rect = Rectangle(w, h)
print(rect)
print(f"Area: {rect.area()}")
print(f"Perimeter: {rect.perimeter()}")

# TASK 5: Single Inheritance
class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_info(self):
        print(f"Vehicle: {self.make} {self.model} ({self.year})")

class Car(Vehicle):
    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        self.num_doors = num_doors

    def honk(self):
        print("Beep beep!")

v_make = input("Car Make: ")
v_model = input("Car Model: ")
v_year = input("Year: ")
v_doors = input("Number of doors: ")

my_car = Car(v_make, v_model, v_year, v_doors)
my_car.display_info()
print(f"Doors: {my_car.num_doors}")
my_car.honk()

# TASK 6: Method Overriding and Polymorphism
import math

class Shape:
    def area(self): return 0
    def describe(self): print("This is a shape.")

class Circle(Shape):
    def __init__(self, radius): self.radius = float(radius)
    def area(self): return math.pi * (self.radius ** 2)
    def describe(self): print(f"This is a circle with radius {self.radius}.")

class Square(Shape):
    def __init__(self, side): self.side = float(side)
    def area(self): return self.side ** 2
    def describe(self): print(f"This is a square with side {self.side}.")

c_rad = input("Enter radius for the circle: ")
s_side = input("Enter side length for the square: ")

shapes = [Circle(c_rad), Square(s_side)]
for s in shapes:
    s.describe()
    print(f"Area: {round(s.area(), 2)}")

# TASK 7: Association
class Author:
    def __init__(self, name, nationality):
        self.name = name
        self.nationality = nationality

class Book:
    def __init__(self, title, year, author_obj):
        self.title = title
        self.year = year
        self.author = author_obj

    def get_book_info(self):
        print(f"Book: \"{self.title}\" ({self.year})")
        print(f"Author: {self.author.name} ({self.author.nationality})")

a_n = input("Author Name: ")
a_nat = input("Author Nationality: ")
b_t = input("Book Title: ")
b_y = input("Publication Year: ")

auth = Author(a_n, a_nat)
bk = Book(b_t, b_y, auth)
bk.get_book_info()

# TASK 8: File I/O with Class Serialization
class Student:
    def __init__(self, name, student_id, grades):
        self.name = name
        self.id = student_id
        self.grades = grades

    def average_grade(self):
        return sum(self.grades) / len(self.grades)

    def to_file_string(self):
        return f"{self.name},{self.id},{' '.join(map(str, self.grades))}"

    @classmethod
    def from_file_string(cls, line):
        parts = line.strip().split(',')
        return cls(parts[0], parts[1], list(map(float, parts[2].split())))

st_list = []
for i in range(3):
    name = input("Enter student name: ")
    sid = input("Enter student ID: ")
    grds = list(map(float, input("Enter grades separated by spaces: ").split()))
    st_list.append(Student(name, sid, grds))

with open("students.txt", "w") as f:
    for s in st_list:
        f.write(s.to_file_string() + "\n")

print("Data written to students.txt.")
print("--- Loaded Students")
with open("students.txt", "r") as f:
    for line in f:
        obj = Student.from_file_string(line)
        print(f"{obj.name} (ID: {obj.id}) - Average: {round(obj.average_grade(), 1)}")

# TASK 9: CSV Processing with Classes
import csv

class Employee:
    def __init__(self, name, age, department, salary):
        self.name, self.age, self.dept, self.salary = name, int(age), department, float(salary)
    
    def give_raise(self, percent): self.salary *= (1 + percent/100)
    def to_dict(self): return {"name": self.name, "age": self.age, "department": self.dept, "salary": self.salary}

emp_list = []
for _ in range(3):
    emp_list.append(Employee(input("Name: "), input("Age: "), input("Dept: "), input("Salary: ")))

with open("employees.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "department", "salary"])
    writer.writeheader()
    writer.writerows([e.to_dict() for e in emp_list])

read_emps = []
with open("employees.csv", "r") as f:
    for row in csv.DictReader(f):
        e = Employee(row['name'], row['age'], row['department'], row['salary'])
        e.give_raise(5)
        read_emps.append(e)

with open("employees_updated.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "department", "salary"])
    writer.writeheader()
    writer.writerows([e.to_dict() for e in read_emps])
print("Updated data written to employees_updated.csv")

# TASK 10: Employee Management System
import csv
from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name, id): self.name, self.id = name, id
    @abstractmethod
    def calculate_pay(self): pass
    @abstractmethod
    def to_csv_row(self): pass

class HourlyEmployee(Employee):
    def __init__(self, name, id, rate, hours):
        super().__init__(name, id)
        self.rate, self.hours = float(rate), float(hours)
    def calculate_pay(self): return self.rate * self.hours
    def to_csv_row(self): return ["Hourly", self.name, self.id, self.rate, self.hours]

class SalariedEmployee(Employee):
    def __init__(self, name, id, salary):
        super().__init__(name, id)
        self.salary = float(salary)
    def calculate_pay(self): return self.salary / 12
    def to_csv_row(self): return ["Salaried", self.name, self.id, self.salary, 0]

class CommissionEmployee(Employee):
    def __init__(self, name, id, base, sales, rate):
        super().__init__(name, id)
        self.base, self.sales, self.rate = float(base), float(sales), float(rate)
    def calculate_pay(self): return self.base + (self.sales * self.rate)
    def to_csv_row(self): return ["Commission", self.name, self.id, self.base, self.sales, self.rate]

system = []
while True:
    opt = input("\n1.Add 2.Save 3.Load 4.Report 5.Exit: ")
    if opt == "1":
        t = input("1:Hourly 2:Salaried 3:Commission: ")
        n, i = input("Name: "), input("ID: ")
        if t=="1": system.append(HourlyEmployee(n, i, input("Rate: "), input("Hours: ")))
        elif t=="2": system.append(SalariedEmployee(n, i, input("Annual Salary: ")))
        elif t=="3": system.append(CommissionEmployee(n, i, input("Base: "), input("Sales: "), input("Rate: ")))
    elif opt == "2":
        with open("employees.csv", "w", newline="") as f:
            csv.writer(f).writerows([e.to_csv_row() for e in system])
    elif opt == "3":
        system = []
        with open("employees.csv", "r") as f:
            for r in csv.reader(f):
                if r[0]=="Hourly": system.append(HourlyEmployee(r[1], r[2], r[3], r[4]))
                elif r[0]=="Salaried": system.append(SalariedEmployee(r[1], r[2], r[3]))
                elif r[0]=="Commission": system.append(CommissionEmployee(r[1], r[2], r[3], r[4], r[5]))
    elif opt == "4":
        for e in system: print(f"{e.name} - Pay: ${round(e.calculate_pay(), 2)}")
    elif opt == "5": break
