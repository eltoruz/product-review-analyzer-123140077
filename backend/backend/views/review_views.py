from pyramid.view import view_config
from pyramid.response import Response
import requests
import google.generativeai as genai
import json
from ..models.review import Review
import os
from dotenv import load_dotenv


# Load .env file
load_dotenv()


# Konfigurasi API Keys
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Debugging: Cek apakah Key terbaca
if HUGGINGFACE_API_KEY:
    print(f"✅ HuggingFace Token Loaded: {HUGGINGFACE_API_KEY[:5]}...")
else:
    print("❌ HuggingFace Token is MISSING in .env file!")

if GEMINI_API_KEY:
    print(f"✅ Gemini Key Loaded: {GEMINI_API_KEY[:5]}...")
else:
    print("❌ Gemini Key is MISSING in .env file!")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Update Hugging Face URL - Menggunakan model yang lebih baik untuk sentiment
HF_API_URL = "https://router.huggingface.co/hf-inference/models/cardiffnlp/twitter-xlm-roberta-base-sentiment"


# ============================================
# OPTIONS HANDLERS (untuk CORS preflight)
# ============================================

@view_config(route_name='analyze_review', request_method='OPTIONS')
def analyze_review_options(request):
    """Handle CORS preflight for analyze_review"""
    return Response(status=200)


@view_config(route_name='get_reviews', request_method='OPTIONS')
def get_reviews_options(request):
    """Handle CORS preflight for get_reviews"""
    return Response(status=200)


# ============================================
# MAIN ENDPOINTS
# ============================================

@view_config(route_name='analyze_review', request_method='POST', renderer='json')
def analyze_review(request):
    """Analyze product review with AI"""
    try:
        data = request.json_body
        product_name = data.get('product_name', '').strip()
        review_text = data.get('review_text', '').strip()
        
        # Validasi input
        if not product_name or not review_text:
            request.response.status = 400
            return {
                'success': False,
                'error': 'Product name and review text are required'
            }
        
        # Step 1: Sentiment Analysis (Hugging Face)
        print(f"Analyzing sentiment for: {product_name}")
        sentiment_result = call_huggingface_sentiment(review_text)
        print(f"Sentiment result: {sentiment_result}")
        
        # Step 2: Extract key points (Gemini)
        print("Extracting key points with Gemini...")
        key_points = extract_key_points_gemini(review_text, product_name)
        print(f"Key points extracted: {key_points}")
        
        # Step 3: Save to database
        review = Review(
            product_name=product_name,
            review_text=review_text,
            sentiment=sentiment_result['label'],
            confidence=sentiment_result['score'],
            key_points=json.dumps(key_points)
        )
        request.dbsession.add(review)
        request.dbsession.flush()  # Flush untuk mendapatkan ID
        
        print(f"Review saved with ID: {review.id}")
        
        return {
            'success': True,
            'id': review.id,
            'product_name': product_name,
            'sentiment': sentiment_result['label'],
            'confidence': sentiment_result['score'],
            'key_points': key_points
        }
        
    except Exception as e:
        print(f"❌ Error in analyze_review: {str(e)}")
        import traceback
        traceback.print_exc()
        request.response.status = 500
        return {
            'success': False,
            'error': str(e)
        }


@view_config(route_name='get_reviews', request_method='GET', renderer='json')
def get_reviews(request):
    """Get all reviews from database"""
    try:
        reviews = request.dbsession.query(Review).order_by(Review.created_at.desc()).all()
        
        reviews_list = []
        for review in reviews:
            review_dict = review.to_dict()
            # Parse key_points dari JSON string
            if review_dict.get('key_points'):
                try:
                    review_dict['key_points'] = json.loads(review_dict['key_points'])
                except:
                    review_dict['key_points'] = {}
            else:
                review_dict['key_points'] = {}
                
            reviews_list.append(review_dict)
        
        print(f"Returning {len(reviews_list)} reviews")
        
        return {
            'success': True,
            'reviews': reviews_list,
            'count': len(reviews_list)
        }
        
    except Exception as e:
        print(f"❌ Error in get_reviews: {str(e)}")
        import traceback
        traceback.print_exc()
        request.response.status = 500
        return {
            'success': False,
            'error': str(e)
        }


# ============================================
# HELPER FUNCTIONS
# ============================================

def call_huggingface_sentiment(text):
    """
    Call Hugging Face Router API for sentiment analysis.
    Using 'twitter-roberta-base-sentiment-latest' for better Positive/Neutral/Negative detection.
    """
    try:
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {"inputs": text}

        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()

            # Handling structure for Roberta models
            # Structure: [[{'label': 'positive', 'score': 0.9}, ...]] atau [{'label': 'positive', 'score': 0.9}, ...]
            if isinstance(result, list) and len(result) > 0:
                # Kadang result dibungkus list lagi [[...]]
                predictions = result[0] if isinstance(result[0], list) else result
                
                # Cari prediction dengan score tertinggi
                top_prediction = max(predictions, key=lambda x: x['score'])
                
                label = top_prediction['label'].upper()  # Convert ke uppercase untuk konsistensi
                score = top_prediction['score']
                
                return {
                    "label": label,
                    "score": round(score, 4)
                }
            else:
                raise Exception("Unexpected response format")

        print(f"⚠️ HF API error ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"⚠️ HF API exception: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Default jika API gagal
    return {
        "label": "NEUTRAL",
        "score": 0.5
    }


def extract_key_points_gemini(text, product_name):
    """Use Gemini to extract key points"""
    if not GEMINI_API_KEY:
        print("❌ SKIPPING Key Points: No valid API Key")
        return ["Analysis unavailable (Missing API Key)"]
    
    try:
        # Gunakan gemini-pro untuk lebih stabil
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""Extract 3-5 key points from this review about {product_name}.
Focus on the main topics, features, or aspects mentioned in the review.

Review: "{text}"

Return ONLY a JSON array of strings. Example: ["Good battery life", "Screen quality issues", "Fast charging"]

Only return the JSON array, no additional text or explanation.
"""
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Bersihkan markdown code block jika ada
        if result_text.startswith('```json'):
            result_text = result_text[7:]
        if result_text.startswith('```'):
            result_text = result_text[3:]
        if result_text.endswith('```'):
            result_text = result_text[:-3]
        
        result_text = result_text.strip()
        
        # Parse JSON
        key_points = json.loads(result_text)
        
        # Validasi structure - harus list
        if isinstance(key_points, list):
            return key_points[:5]  # Batasi maksimal 5 poin
        else:
            # Jika bukan list, coba convert ke list
            return [str(key_points)]
        
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON Parse Error: {str(e)}")
        # Fallback: split by newline dan ambil yang penting
        try:
            lines = result_text.split('\n')
            key_points = [line.strip("- *[]\"'") for line in lines if line.strip() and len(line.strip()) > 5]
            return key_points[:5] if key_points else ["Unable to extract key points"]
        except:
            return ["Unable to extract key points"]
        
    except Exception as e:
        print(f"⚠️ Error in extract_key_points_gemini: {str(e)}")
        
        # Cek pesan error spesifik
        if "API_KEY_INVALID" in str(e):
            print("💡 TIP: Check your GEMINI_API_KEY in .env file!")
        
        # Return default jika gagal
        return ["Unable to extract key points"]