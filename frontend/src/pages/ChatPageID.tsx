import ChatTextBox from "@/components/ChatTextBox";
import React from "react";

const ChatPageID: React.FC = () => {
  return (
    <div className="pt-8 px-8 relative h-full flex flex-col justify-between">
      <div className="max-w-[75%] pb-20">
        <h1 className="text-4xl font-semibold">
          What is the whisttleblower act?
        </h1>
        <p className="mt-4 text-lg">
          The Whistleblower Act is a law in the United States that allows people
          to report illegal activities without fear of retaliation.
          <br />
          <br />
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non
          risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec,
          ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula
          massa, mattis quis, hendrerit ac, pharetra in, mi. Pellentesque
        </p>
      </div>

      <ChatTextBox className="sticky bottom-4 w-full left-1/2" />
    </div>
  );
};

export default ChatPageID;
