import { useEffect, useState } from "react";
import Header from "./components/Header";
import ReviewForm from "./components/ReviewForm";
import AnalysisResult from "./components/AnalysisResult";
import ReviewsList from "./components/ReviewsList";
import { fetchReviewsAPI, analyzeReviewAPI } from "./utils/api";

function App() {
  const [reviews, setReviews] = useState([]);
  const [loadingReviews, setLoadingReviews] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const fetchReviews = async () => {
    setLoadingReviews(true);
    const data = await fetchReviewsAPI();
    if (data.success) setReviews(data.reviews);
    setLoadingReviews(false);
  };

  useEffect(() => {
    fetchReviews();
  }, []);

  const handleSubmit = async (productName, reviewText) => {
    setLoading(true);
    setError("");
    setResult(null);

    const data = await analyzeReviewAPI(productName, reviewText);
    if (data.success) {
      setResult(data);
      fetchReviews();
    } else {
      setError(data.error || "Something went wrong.");
    }
    setLoading(false);
  };

  return (
    <div className="app">
      <Header />

      <main className="main-content">
        <section className="form-section">
          <ReviewForm onSubmit={handleSubmit} loading={loading} error={error} />
          <AnalysisResult result={result} />
        </section>

        <section className="reviews-section">
          <div className="section-header">
            <h2>Recent Reviews</h2>
            <span className="count">{reviews.length} total</span>
          </div>

          <ReviewsList reviews={reviews} loading={loadingReviews} />
        </section>
      </main>
    </div>
  );
}

export default App;
