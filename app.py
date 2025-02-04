from flask import Flask, render_template, request, redirect, jsonify
import json

app = Flask(__name__)

# Cargar preguntas desde el archivo JSON
def load_questions():
    try:
        with open('questions.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Si el archivo no existe, devolvemos una lista vacía
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON. Verifica el formato.")
        return []

# Guardar preguntas en el archivo JSON
def save_questions(questions):
    try:
        with open('questions.json', 'w') as file:
            json.dump(questions, file, indent=4)
    except Exception as e:
        print(f"Error al guardar las preguntas: {e}")

# Ruta principal del quiz
@app.route('/')
def index():
    try:
        questions = load_questions()
        if not isinstance(questions, list):  # Asegúrate de que sea una lista
            questions = []
    except Exception as e:
        print(f"Error al cargar preguntas: {e}")
        questions = []

    return render_template('quiz.html', questions=questions)

# Ruta para obtener preguntas en formato JSON
@app.route('/get_questions')
def get_questions():
    questions = load_questions()
    return jsonify(questions)

# Ruta para agregar una nueva pregunta
@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        # Obtener datos del formulario
        question_text = request.form.get('question', '').strip()
        option_a = request.form.get('option_a', '').strip()
        option_b = request.form.get('option_b', '').strip()
        option_c = request.form.get('option_c', '').strip()
        option_d = request.form.get('option_d', '').strip()
        option_e = request.form.get('option_e', '').strip()
        correct_option = request.form.get('correct_option', '').strip()

        # Validar que todos los campos estén completos
        if not (question_text and option_a and option_b and option_c and option_d and option_e and correct_option):
            return "Todos los campos son obligatorios. Vuelve e intenta de nuevo.", 400

        # Validar que la respuesta correcta sea una de las opciones válidas
        if correct_option not in ['a', 'b', 'c', 'd', 'e']:
            return "La respuesta correcta debe ser una de las opciones: a, b, c, d, e.", 400

        # Cargar preguntas existentes
        questions = load_questions()

        # Crear la nueva pregunta
        new_question = {
            "id": len(questions) + 1,
            "question": question_text,
            "options": {
                "a": option_a,
                "b": option_b,
                "c": option_c,
                "d": option_d,
                "e": option_e
            },
            "correct": correct_option
        }

        # Agregar la nueva pregunta y guardar
        questions.append(new_question)
        save_questions(questions)

        # Redirigir al quiz después de agregar
        return redirect('/')

    # Renderizar el formulario si el método es GET
    return render_template('add_question.html')

if __name__ == '__main__':
    app.run(debug=True)
