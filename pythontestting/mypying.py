from mypy import api

result = api.run(["my_script.py"])
print("Output:", result[0])
print("Errors:", result[1])
print("Exit Status:", result[2])