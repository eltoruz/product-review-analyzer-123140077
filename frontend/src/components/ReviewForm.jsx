import { useState, useEffect } from "react";
import '../App.css';

const ReviewForm = ({ onSubmit, loading, error, shouldReset }) => {
  const [productName, setProductName] = useState("");
  const [reviewText, setReviewText] = useState("");

  // Reset form hanya ketika shouldReset menjadi true
  useEffect(() => {
    if (shouldReset) {
      setProductName("");
      setReviewText("");
    }
  }, [shouldReset]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(productName, reviewText);
    // JANGAN reset di sini lagi
  };

  return (
    <div className="card">
      <h2>New Review</h2>

      {error && (
        <div className="alert alert-error">
          <span>⚠️</span>
          <p>{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label>Product Name</label>
          <input
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            required
            disabled={loading} // Disable saat loading
          />
        </div>

        <div className="input-group">
          <label>Your Review</label>
          <textarea
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            rows="5"
            required
            disabled={loading} // Disable saat loading
          />
        </div>

        <button className="btn-submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Review"}
        </button>
      </form>
    </div>
  );
};

export default ReviewForm;