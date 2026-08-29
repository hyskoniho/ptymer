#! start
print("This block should be timed.")
name = "Charles"

if len(name) == 10:
    print(f"{name} has 10 characters.")
else:
    print(f"The length of the name is unknown.")
#! end

print("This block should not be timed.")

#! start
print("This block should be timed.")
names = ["david", "john", "Erick"]

for name in names:
    print("names")
#! end
