import ReviewCard from "./ReviewCard";
import '../App.css';

const ReviewsList = ({ reviews, loading }) => {
  if (loading) return <div className="loader">Loading...</div>;

  if (reviews.length === 0)
    return (
      <div className="empty-message">
        <p>No reviews yet. Submit the first one!</p>
      </div>
    );

  return (
    <div className="reviews-grid">
      {reviews.map((r) => (
        <ReviewCard review={r} key={r.id} />
      ))}
    </div>
  );
};

export default ReviewsList;

