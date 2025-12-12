import { formatDate } from "../utils/formatDate";
import '../App.css';

const ReviewCard = ({ review }) => {
  const keyPoints = review.key_points;

  return (
    <div className="review-card">
      <div className="review-top">
        <h3>{review.product_name}</h3>
        <span className={`badge badge-${review.sentiment.toLowerCase()}`}>
          {review.sentiment}
        </span>
      </div>

      <p className="review-text">{review.review_text}</p>

      {/* Tambahkan Key Points Section */}
      {keyPoints && Array.isArray(keyPoints) && keyPoints.length > 0 && (
        <div className="key-points-section">
          <h4>Key Points:</h4>
          <ul className="key-points-list">
            {keyPoints.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="review-footer">
        <span>{formatDate(review.created_at)}</span>
        <span className="confidence">
          {(review.confidence * 100).toFixed(0)}%
        </span>
      </div>
    </div>
  );
};

export default ReviewCard;