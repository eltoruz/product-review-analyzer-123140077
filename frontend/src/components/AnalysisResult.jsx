import Insights from "./Insights";
import '../App.css';

const AnalysisResult = ({ result }) => {
  if (!result) return null;

  return (
    <div className="analysis-result">
      <div className="result-header">
        <h3>Analysis Complete</h3>
        <span className={`badge badge-${result.sentiment.toLowerCase()}`}>
          {result.sentiment}
        </span>
      </div>

      <p className="confidence-score">
        Confidence: <strong>{(result.confidence * 100).toFixed(1)}%</strong>
      </p>

      <Insights keyPoints={result.key_points} />
    </div>
  );
};

export default AnalysisResult;
