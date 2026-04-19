from flask import Flask, render_template, request, jsonify
from tax_assistant import TaxAssistant
import openai
import os

app = Flask(__name__)
tax_assistant = TaxAssistant()

# Configure OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('forms.html')

@app.route('/api/tax-advice', methods=['POST'])
def get_tax_advice():
    data = request.json
    user_query = data.get('query', '')
    income = data.get('income', 0)
    
    # Get tax information from assistant
    tax_info = tax_assistant.get_tax_information()
    calculated_tax = tax_assistant.calculate_tax(income) if income > 0 else 0
    
    # Create prompt for AI assistant
    prompt = f"""You are a South African tax expert assistant. 
    Current tax brackets: {tax_assistant.tax_brackets}
    User question: {user_query}
    User income: {income}
    Calculated tax: {calculated_tax}
    
    Provide helpful and accurate tax advice based on South African tax law."""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a South African tax expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        advice = response['choices'][0]['message']['content']
    except Exception as e:
        advice = f"Error getting AI advice: {str(e)}"
    
    return jsonify({
        'advice': advice,
        'calculated_tax': calculated_tax,
        'tax_info': tax_info
    })

@app.route('/api/submit-form', methods=['POST'])
def submit_form():
    data = request.json
    deadline = data.get('deadline')
    tax_tables = data.get('tax_tables', [])
    
    # Validate data
    if not deadline:
        return jsonify({'error': 'Deadline is required'}), 400
    
    # Process and store data (implement database storage as needed)
    return jsonify({
        'success': True,
        'message': f'Deadline {deadline} and {len(tax_tables)} tax tables submitted successfully'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)