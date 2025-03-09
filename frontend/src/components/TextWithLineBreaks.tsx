import React from "react";

const TextWithLineBreaks: React.FC<{ text: string; className: string }> = ({
  text,
  className,
}) => {
  return (
    <div className={className}>
      {text.split("\n").map((line, index) => (
        <React.Fragment key={index}>
          {line}
          {index < text.split("\n").length - 1 && <br />}
        </React.Fragment>
      ))}
    </div>
  );
};

export default TextWithLineBreaks;
