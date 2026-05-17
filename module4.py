# Module 4 - Risk Classification

def classify_risk(area, perimeter):
    if area > 80000 and perimeter > 1500:
        return "DANGEROUS"
    elif area > 40000:
        return "ALERT"
    else:
        return "SAFE"


# Example feature values (from Module 3 output)
area = int(input("Enter extracted body area: "))
perimeter = int(input("Enter extracted body perimeter: "))

risk = classify_risk(area, perimeter)

print("\n--- RISK ANALYSIS RESULT ---")
print("Risk Level:", risk)
