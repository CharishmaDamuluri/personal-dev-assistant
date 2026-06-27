import React from 'react';

function ScoreCard({ score }) {
  return (
    <div className="score-card">
      <h2>Score: {score}</h2>
      <div className="progress-ring">
        <svg
          className="progress-ring__svg"
          width="120"
          height="120"
          xmlns="http://www.w3.org/2000/svg"
        >
          <circle
            className="progress-ring__circle"
            stroke="blue"
            strokeWidth="4"
            fill="transparent"
            r="54"
            cx="60"
            cy="60"
          />
        </svg>
      </div>
    </div>
  );
}

export default ScoreCard;