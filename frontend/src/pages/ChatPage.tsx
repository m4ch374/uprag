import ChatTextBox from "@/components/ChatTextBox";
import useToken from "@/lib/hooks/useToken.hooks";
import { useCreateChat } from "@/lib/services/chat.service";
import { useQueryClient } from "@tanstack/react-query";
import React from "react";
import { useNavigate } from "react-router";

const ChatPage: React.FC = () => {
  const navigate = useNavigate();

  const accessToken = useToken();
  const queryClient = useQueryClient();
  const createChat = useCreateChat(accessToken, queryClient);

  return (
    <div className="size-full flex justify-center items-center">
      <div className="w-full max-w-xl">
        <h1 className="text-4xl font-semibold text-center">
          What do you want to know?
        </h1>
        <ChatTextBox
          className="mt-4"
          loading={createChat.isPending}
          onTextSubmission={(text, e) => {
            e.preventDefault();
            createChat.mutate(
              {
                user_query: text,
              },
              {
                onSuccess: data => navigate(`/chat/${data.id}`),
              },
            );
          }}
        />
      </div>
    </div>
  );
};

export default ChatPage;
