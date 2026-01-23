#include <App/ExpressionParser.h>

int main()
{
    const char* expr = "1 + 2 * 3";

    for (int i = 0; i < 1'000'000; ++i)
    {
        // LEAK proposital
        Expression* e = App::ExpressionParser::parse(nullptr, expr);

        // força alguma avaliação
        e->getValueAsAny();

        // delete e;  <-- propositalmente comentado
    }

    return 0;
}
