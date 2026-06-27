import React from 'react';

const ScoreCard = ({ score, total }) => {
  const calculatePercentage = () => {
    return ((score / total) * 100).toFixed(2);
  };

  const getVerdictLabel = (percentage) => {
    if (percentage >= 90) return 'Excellent';
    if (percentage >= 75) return 'Good';
    if (percentage >= 50) return 'Average';
    return 'Needs Improvement';
  };

  const percentage = calculatePercentage();
  const verdict = getVerdictLabel(percentage);

  return (
    <div className="score-card">
      <h2>Score: {score} / {total}</h2>
      <p>Percentage: {percentage}%</p>
      <p>Verdict: {verdict}</p>
    </div>
  );
};

export default ScoreCard;