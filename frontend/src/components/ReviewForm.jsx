import { useState } from "react";
import '../App.css';

const ReviewForm = ({ onSubmit, loading, error }) => {
  const [productName, setProductName] = useState("");
  const [reviewText, setReviewText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(productName, reviewText);
    setProductName("");
    setReviewText("");
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
          />
        </div>

        <div className="input-group">
          <label>Your Review</label>
          <textarea
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            rows="5"
            required
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
