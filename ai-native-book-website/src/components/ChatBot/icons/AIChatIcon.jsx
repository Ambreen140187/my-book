import React from 'react';

const AIChatIcon = ({ size = 24, className = '', fill = 'currentColor' }) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <path
        d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.36 15.01 3.02 16.32L2 22L7.68 20.98C8.99 21.64 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C8.69 20 6 17.31 6 14C6 10.69 8.69 8 12 8C15.31 8 18 10.69 18 14C18 17.31 15.31 20 12 20Z"
        fill={fill}
      />
      <circle cx="9" cy="11" r="1" fill={fill} />
      <circle cx="15" cy="11" r="1" fill={fill} />
      <path
        d="M12 14C10.34 14 9 15.34 9 17C9 17.34 9.06 17.67 9.17 18H14.83C14.94 17.67 15 17.34 15 17C15 15.34 13.66 14 12 14Z"
        fill={fill}
      />
    </svg>
  );
};

export default AIChatIcon;