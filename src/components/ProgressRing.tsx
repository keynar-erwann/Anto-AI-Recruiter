import React from 'react';

interface ProgressRingProps {
  progress: number;
  size: number;
  strokeWidth: number;
  className?: string;
  color?: string;
}

const ProgressRing: React.FC<ProgressRingProps> = ({ 
  progress, 
  size, 
  strokeWidth, 
  className = '',
  color = 'stroke-indigo-600'
}) => {
  const normalizedProgress = Math.min(100, Math.max(0, progress));
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (normalizedProgress / 100) * circumference;
  
  return (
    <div className={`relative inline-flex items-center justify-center ${className}`}>
      <svg
        className="transform -rotate-90"
        width={size}
        height={size}
      >
        <circle
          className="stroke-gray-200"
          strokeWidth={strokeWidth}
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx={size / 2}
          cy={size / 2}
        />
        <circle
          className={`${color} transition-all duration-500 ease-out`}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx={size / 2}
          cy={size / 2}
        />
      </svg>
      <span className="absolute text-center font-semibold text-gray-800">
        {Math.round(normalizedProgress)}
      </span>
    </div>
  );
};

export default ProgressRing;