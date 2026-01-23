//como tentei rodar
g++ -fsanitize=address -g leak_parse.cpp \
    ExpressionParser.cpp \
    -o leak_parse