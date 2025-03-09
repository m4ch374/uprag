import ChatTextBox from "@/components/ChatTextBox";
import React from "react";

const ChatPage: React.FC = () => {
  return (
    <div className="size-full flex justify-center items-center">
      <div className="w-full max-w-xl">
        <h1 className="text-4xl font-semibold text-center">
          What do you want to know?
        </h1>
        <ChatTextBox className="mt-4" />
      </div>
    </div>
  );
};

export default ChatPage;
