import functions

functions.load_train_data('en', 100)
functions.load_train_data('ru', 100)

print(functions.detect_language('My name is John Doe', 50))
print(functions.detect_language('Меня зовут Иван', 50))
