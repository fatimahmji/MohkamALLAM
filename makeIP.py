# Import necessary libraries
import os
from ibm_watsonx_ai.foundation_models import Model

# Model and parameter configuration
model_id = "sdaia/allam-1-13b-instruct"
parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 650,
    "repetition_penalty": 1.19
}

# Set up project ID
project_id = "f5266780-6418-4e00-9410-950393001fe6"

# Initialize the model
model = Model(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=project_id
)

# Collect user input for the query
query = input("Enter your query: ")

# Combine the query with a general instructional prompt
combined_prompt = f"""
أنت مختص في القانون في المملكة العربية السعودية وذو خبرة كبيرة في مجال حقوق الملكية الفكرية. بناءً على نظام حقوق الملكية الفكرية السعودي، عليك كتابة مسودة حقوق الملكية الفكرية تتضمن تفاصيل الحماية والمخالفات والجزاءات المرتبطة بالمصنفات الفكرية. 

إليك الاستفسار:

"{query}"
 يرجى تقديم الرد بما يتناسب مع المعايير النظامية المذكورة، وتحديد المصنفات، مدة الحماية، وأهم المخالفات والجزاءات وفقًا للأنظمة السعودية. لاتخرج عن مجال حقوق المؤلف وعليك ارفاق رقم المادة لكل جزئية.
 
هذا مثال لتتعلم منه:

حقوق الملكية الفكرية للمغني محمد محفوظة وفقًا لنظام حماية حقوق المؤلف السعودي.
المصنفات التي يحميها النظام وشروط حمايتها تشمل:

المصنف الموسيقي: يشمل الأغاني والموسيقى والكلمات والألحان وغيرها من الأعمال الموسيقية.
الأداء العلني: يشمل العروض المباشرة والحفلات والتسجيلات الصوتية والمرئية للأغاني والموسيقى التي يقدمها المغني .
التسجيل الصوتي: يشمل تسجيلات الصوت للأغاني والموسيقى التي ينتجها المغني .

شروط الحماية: يجب أن يكون المصنف أصليًا ويظهر فيه إبداع المغني محمد. (المادة الثانية)

مدة الحماية: تكون حماية حق المؤلف في المصنف مدى حياة المؤلف ولمدة خمسين سنة بعد وفاته. (المادة التاسعة عشرة)

أهم المخالفات والجزاءات المترتبة على انتهاك حقوق المؤلف بناء على  (المادة الثانية والعشرون) تشمل:

نسخ أو توزيع المصنفات بدون إذن من المغني محمد أو من يمثله.
استخدام المصنفات بطرق غير قانونية، مثل عرضها على الإنترنت بدون إذن.
تعديل أو تحوير المصنفات بطرق تغير معناها أو قيمتها الأدبية.
استخدام المصنفات في الإعلانات أو الترويج بدون إذن من المغني محمد أو من يمثله.
استخدام المصنفات في الأعمال التجارية بدون إذن من المغني محمد أو من يمثله.

اكتب حقوق الملكية الفكرية للمؤلف
"""

# Generate the response using the combined prompt
print(query)
print("Submitting generation request...")
generated_response = model.generate_text(prompt=combined_prompt, guardrails=False)
print("\nGenerated Document:")
print(generated_response)
