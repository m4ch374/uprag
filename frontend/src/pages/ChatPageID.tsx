import ChatTextBox from "@/components/ChatTextBox";
import TextWithLineBreaks from "@/components/TextWithLineBreaks";
import useToken from "@/lib/hooks/useToken.hooks";
import { useContinueChat, useGetChat } from "@/lib/services/chat.service";
import { useListKnowledge } from "@/lib/services/knowledge.service";
import { TChatGPTHistoryItem } from "@/lib/types/GlobalTypes";
import { prefixedWithMagic } from "@/lib/utils";
import { useQueryClient } from "@tanstack/react-query";
import { BookOpenText } from "lucide-react";
import React, { Fragment, useCallback, useEffect } from "react";
import { useParams } from "react-router";

const ChatPageID: React.FC = () => {
  const accessToken = useToken();
  const queryClient = useQueryClient();
  const { id } = useParams();

  const { data: chatData } = useGetChat(accessToken, id || "");
  const { data: knowledges } = useListKnowledge(accessToken);

  const continueChat = useContinueChat(accessToken, queryClient, id || "");

  const shouldDisplayItem = useCallback((item: TChatGPTHistoryItem) => {
    return (
      item.role !== "system" &&
      item.role !== "developer" &&
      !prefixedWithMagic(item.content)
    );
  }, []);

  useEffect(() => {
    console.log("chatData", chatData?.history);
  }, [chatData?.history]);

  return (
    <div className="pt-8 px-8 relative h-full flex flex-col justify-between">
      <div className="max-w-[75%] pb-20">
        {chatData?.history
          .filter(item => shouldDisplayItem(item))
          .map((item, index) => (
            <Fragment key={index}>
              {!!index && item.role === "user" && <hr className="my-6" />}
              {item.role === "user" ? (
                <h1 className="text-4xl font-semibold">{item.content}</h1>
              ) : (
                <>
                  <div className="flex items-center py-2 gap-2 font-semibold mt-5">
                    <BookOpenText className="stroke-emerald-500 mt-1" /> Answer
                  </div>
                  <TextWithLineBreaks text={item.content} className="text-lg" />
                </>
              )}
            </Fragment>
          ))}
      </div>
      <ChatTextBox
        className="sticky bottom-4 w-full left-1/2 shadow-lg"
        loading={!chatData || continueChat.isPending}
        onTextSubmission={(text, knowledges, e) => {
          e.preventDefault();
          continueChat.mutate({
            user_query: text,
            knowledge: knowledges.map(k => k.id),
          });
        }}
        defaultKnowledge={knowledges?.knowledges.filter(k =>
          chatData?.knowledge.find(s => s === k.id),
        )}
      />
    </div>
  );
};

export default ChatPageID;
