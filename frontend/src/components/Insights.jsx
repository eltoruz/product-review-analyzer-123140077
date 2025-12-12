const Insights = ({ keyPoints }) => {
  if (!keyPoints) return null;

  if (Array.isArray(keyPoints) && keyPoints.length > 0) {
    return (
      <div className="insights">
        <h4>Key Points</h4>
        <ul>
          {keyPoints.map((p, i) => (
            <li key={i}>{p}</li>
          ))}
        </ul>
      </div>
    );
  }

  return (
    <div className="insights">
      {keyPoints.positive?.length > 0 && (
        <div className="insight-section">
          <h4>Positive Highlights</h4>
          <ul>
            {keyPoints.positive.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </div>
      )}

      {keyPoints.negative?.length > 0 && (
        <div className="insight-section">
          <h4>Areas of Concern</h4>
          <ul>
            {keyPoints.negative.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </div>
      )}

      {keyPoints.suggestions?.length > 0 && (
        <div className="insight-section">
          <h4>Recommendations</h4>
          <ul>
            {keyPoints.suggestions.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Insights;
