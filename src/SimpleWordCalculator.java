import javax.swing.JOptionPane;
import java.util.Stack;

public class SimpleWordCalculator {

    public static void main(String[] args) {
        while (true) {
            String userInput = JOptionPane.showInputDialog(null, "İşlem giriniz (örneğin: 3 topla 5 çarp 2). Çıkmak için 'exit' yazın:");

            if (userInput == null || userInput.equalsIgnoreCase("exit")) {
                break;
            }

            try {
                double result = evaluateExpression(userInput);
                JOptionPane.showMessageDialog(null, "Sonuç: " + result);
            } catch (Exception e) {
                JOptionPane.showMessageDialog(null, "Hata: " + e.getMessage(), "Hata", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    public static double evaluateExpression(String expression) throws Exception {
        String trimmedExpression = expression.replaceAll("\\s+", " ").trim();
        return evaluate(trimmedExpression);
    }

    public static double evaluate(String expression) throws Exception {
        Stack<Double> numbers = new Stack<>();
        Stack<String> operators = new Stack<>();

        String[] tokens = expression.split(" ");

        for (String token : tokens) {
            if (isNumeric(token)) {
                numbers.push(Double.parseDouble(token));
            } else if (token.equals("topla") || token.equals("çıkar") || token.equals("çarp") || token.equals("böl")) {
                operators.push(token);
            } else {
                throw new IllegalArgumentException("Geçersiz işlem: " + token);
            }
        }

        while (!operators.isEmpty()) {
            applyOperation(numbers, operators);
        }

        return numbers.pop();
    }

    private static void applyOperation(Stack<Double> numbers, Stack<String> operators) {
        String operator = operators.pop();
        double b = numbers.pop();
        double a = numbers.pop();
        double result;
        switch (operator) {
            case "topla":
                result = a + b;
                break;
            case "çıkar":
                result = a - b;
                break;
            case "çarp":
                result = a * b;
                break;
            case "böl":
                if (b == 0) {
                    throw new ArithmeticException("Sıfıra bölme hatası");
                }
                result = a / b;
                break;
            default:
                throw new IllegalArgumentException("Geçersiz operatör: " + operator);
        }
        numbers.push(result);
    }

    private static boolean isNumeric(String str) {
        try {
            Double.parseDouble(str);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }
}