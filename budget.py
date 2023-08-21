class Category:

    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, budget_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {budget_category.category}")
            budget_category.deposit(amount, f"Transfer from {self.category}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        output = f"{self.category.center(30, '*')}\n"
        for item in self.ledger:
            desc = item["description"][:23].ljust(23)
            amt = format(item["amount"], ".2f").rjust(30 - len(desc))
            output += f"{desc}{amt}\n"
        output += f"Total: {format(self.get_balance(), '.2f')}"
        return output

def create_spend_chart(categories):
    chart = "Percentage spent by category\n"
    spendings = [(category.category, sum(item["amount"] for item in category.ledger if item["amount"] < 0)) for category in categories]
    total_spent = sum(amount for _, amount in spendings)
    percentages = [(int((amount / total_spent) * 100 // 10) * 10) for _, amount in spendings]

    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + "| "
        for percentage in percentages:
            chart += "o" if percentage >= i else " "
            chart += "  "
        chart += "\n"

    chart += "    -" + "---" * len(categories) + "\n"

    max_len = max(len(category.category) for category in categories)
    category_names = [category.category.ljust(max_len) for category in categories]

    for i in range(max_len):
        chart += "     "
        for name in category_names:
            chart += name[i] + "  "
        chart += "\n"

    return chart.rstrip()

# Test the Category class
food_category = Category("Food")
clothing_category = Category("Clothing")
entertainment_category = Category("Entertainment")

food_category.deposit(1000, "initial deposit")
food_category.withdraw(10.15, "groceries")
food_category.withdraw(15.89, "restaurant and more foo")
food_category.transfer(50, clothing_category)

clothing_category.deposit(500, "initial deposit")
clothing_category.withdraw(25.55, "shirt")
clothing_category.transfer(50, food_category)

entertainment_category.deposit(200, "initial deposit")
entertainment_category.withdraw(15, "movie")
entertainment_category.withdraw(45, "concert")

print(food_category)
print(clothing_category)
print(entertainment_category)

# Test the create_spend_chart function
print(create_spend_chart([food_category, clothing_category, entertainment_category]))
