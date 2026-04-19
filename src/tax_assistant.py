class TaxAssistant:
    def __init__(self):
        # Initialize tax brackets for South Africa (sample data)
        self.tax_brackets = [
            (0, 22600, 0.18),
            (22601, 35300, 0.26),
            (35301, 48800, 0.31),
            (48801, 65700, 0.36),
            (65701, 100000, 0.39),
            (100001, float('inf'), 0.41)
        ]

    def calculate_tax(self, income):
        tax = 0
        for lower, upper, rate in self.tax_brackets:
            if income > lower:
                taxable_income = min(income, upper) - lower
                tax += taxable_income * rate
            else:
                break
        return tax

    def get_tax_information(self):
        return "This assistant can help you with South African tax brackets and advice. Feel free to ask about any specific tax-related questions!"

# Example usage
if __name__ == '__main__':
    assistant = TaxAssistant()
    income = 50000  # Example income
    tax = assistant.calculate_tax(income)
    print(f'Tax to be paid on an income of {income} is: {tax}')