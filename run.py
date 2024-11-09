import json
from flask import Flask, render_template, request, jsonify
import warnings
from ibm_watsonx_ai.foundation_models import Model

# Suppress irrelevant warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)
warnings.filterwarnings(action='ignore', category=UserWarning)
warnings.filterwarnings(action='ignore', category=DeprecationWarning)

app = Flask(__name__)

# Function to get credentials
def get_credentials():
    return {
        "url": "https://eu-de.ml.cloud.ibm.com",
        "apikey": "Qp_xZRfMnSnXNEd51OywtfFNxiZaVvjtIpvUbE8FGLRY",
        "model_id": "sdaia/allam-1-13b-instruct",
        "project_id": "f5266780-6418-4e00-9410-950393001fe6"
    }

# Initialize the model instance only once
def create_model_instance():
    credentials = get_credentials()
    model_id = credentials["model_id"]
    project_id = credentials["project_id"]
    
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 650,
        "repetition_penalty": 1.19
    }
    
    model = Model(
        model_id=model_id,
        params=parameters,
        credentials=credentials,
        project_id=project_id
    )
    return model

# Create a single model instance for the app
model_instance = create_model_instance()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/ask_allam', methods=['GET', 'POST'])
def ask_model():
    if request.method == 'POST':
        user_input = request.json.get("input")
        
        # Log the input
        print("User Input:", repr(user_input))
        
        combined_prompt = f"""
        أنت مختص في القانون في المملكة العربية السعودية وذو خبرة كبيرة في مجال حقوق الملكية الفكرية...
        "{user_input}"
        """
        
        # Log the complete prompt
        print("Complete Prompt:", repr(combined_prompt))

        try:
            # Generate response from the model
            generated_response = model_instance.generate_text(prompt=combined_prompt, guardrails=False)
            
            # Detailed logging of raw response
            print("Raw Response Type:", type(generated_response))
            print("Raw Response (repr):", repr(generated_response))
            print("Raw Response (str):", str(generated_response))
            
            if isinstance(generated_response, str):
                allam_response = generated_response
            elif isinstance(generated_response, dict):
                # Log all available keys
                print("Available keys in response:", list(generated_response.keys()))
                
                if "results" in generated_response and generated_response["results"]:
                    allam_response = generated_response["results"][0]["generated_text"]
                elif "generated_text" in generated_response:
                    allam_response = generated_response["generated_text"]
                elif "text" in generated_response:
                    allam_response = generated_response["text"]
                else:
                    print("Full response structure:", json.dumps(generated_response, indent=2, ensure_ascii=False))
                    allam_response = "عذراً، حدث خطأ في معالجة الرد. الرجاء المحاولة مرة أخرى."
            else:
                print("Unknown response type:", type(generated_response))
                allam_response = "عذراً، حدث خطأ في معالجة الرد. الرجاء المحاولة مرة أخرى."
            
            # Log the final response before sending
            print("Final Response (repr):", repr(allam_response))
            
            return jsonify({
                "response": allam_response,  # Sending without any trimming
                "status": "success"
            })
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            print(f"Error type: {type(e)}")
            return jsonify({
                "response": "عذراً، حدث خطأ أثناء معالجة طلبك. الرجاء المحاولة مرة أخرى.",
                "status": "error",
                "error": str(e)
            }), 500
    
    return render_template('ask-model.html')

if __name__ == '__main__':
    app.run(debug=True)
