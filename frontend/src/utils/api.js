const API_BASE_URL = "http://127.0.0.1:6542/api";

export const fetchReviewsAPI = async () => {
  const res = await fetch(`${API_BASE_URL}/reviews`);
  return res.json();
};

export const analyzeReviewAPI = async (productName, reviewText) => {
  const res = await fetch(`${API_BASE_URL}/analyze-review`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_name: productName, review_text: reviewText }),
  });
  return res.json();
};
