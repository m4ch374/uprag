import ChatTextBox from "@/components/ChatTextBox";
import TextWithLineBreaks from "@/components/TextWithLineBreaks";
import useToken from "@/lib/hooks/useToken.hooks";
import { useGetChat } from "@/lib/services/chat.service";
import { TChatGPTHistoryItem } from "@/lib/types/GlobalTypes";
import { prefixedWithMagic } from "@/lib/utils";
import React, { Fragment, useCallback } from "react";
import { useParams } from "react-router";

const ChatPageID: React.FC = () => {
  const accessToken = useToken();
  const { id } = useParams();

  const { data: chatData } = useGetChat(accessToken, id || "");

  const shouldDisplayItem = useCallback((item: TChatGPTHistoryItem) => {
    return (
      item.role !== "system" &&
      item.role !== "developer" &&
      !prefixedWithMagic(item.content)
    );
  }, []);

  return (
    <div className="pt-8 px-8 relative h-full flex flex-col justify-between">
      <div className="max-w-[75%] pb-20">
        {chatData
          ?.filter(item => shouldDisplayItem(item))
          .map((item, index) => (
            <Fragment key={index}>
              {!!index && item.role === "user" && <hr />}
              {item.role === "user" ? (
                <h1 className="text-4xl font-semibold">{item.content}</h1>
              ) : (
                <TextWithLineBreaks
                  text={item.content}
                  className="mt-4 text-lg"
                />
              )}
            </Fragment>
          ))}
      </div>
      <ChatTextBox className="sticky bottom-4 w-full left-1/2 shadow-lg" />
    </div>
  );
};

export default ChatPageID;
